#!/usr/bin/env python3
"""Compare independent statements and replay the proved environment in Lean."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys

sys.dont_write_bytecode = True

from sandbox_check import check as check_sandbox, guard
from check import release_files, source_snapshot

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.lake/verification'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def snapshot():
    """Freeze all distributed sources, contracts, documentation and build inputs."""
    return source_snapshot(release_files())


def run(args, cwd=ROOT, env=None):
    subprocess.run(list(map(str, args)), cwd=cwd, env=env, check=True)


def checkout(spec, destination):
    if not destination.exists():
        run(['git', 'clone', '--no-checkout', spec['url'], destination])
        run(['git', 'checkout', '--detach', spec['revision']], cwd=destination)
    actual = subprocess.check_output(['git', 'rev-parse', 'HEAD'],
                                     cwd=destination, text=True).strip()
    if actual != spec['revision']:
        raise RuntimeError('Unexpected tool revision: ' + destination.name)
    origin = subprocess.check_output(['git', 'remote', 'get-url', 'origin'],
                                     cwd=destination, text=True).strip()
    if origin.removesuffix('.git') != spec['url'].removesuffix('.git'):
        raise RuntimeError('Unexpected tool origin: ' + destination.name)
    run(['git', 'diff', '--quiet', 'HEAD'], cwd=destination)
    untracked = subprocess.check_output(
        ['git', 'ls-files', '--others', '--exclude-standard'], cwd=destination, text=True)
    if untracked.strip():
        raise RuntimeError('Unexpected untracked tool source: ' + destination.name)


def setup(trusted_local):
    lock = json.loads((ROOT / 'Verification/tools.json').read_text())
    base = ROOT / '.tools'
    base.mkdir(exist_ok=True)
    comparator = base / 'comparator'
    checkout(lock['comparator'], comparator)
    toolchain = (ROOT / 'lean-toolchain').read_text().strip()
    # Compile both tools with this project's exact Lean version. Their upstream
    # source revision is fixed independently of the upstream default toolchain.
    run(['lake', '+' + toolchain, 'build', 'comparator', 'lean4export'], cwd=comparator)
    exporter = comparator / '.lake/packages/lean4export'
    checkout(lock['lean4export'], exporter)
    env = os.environ.copy()
    env['COMPARATOR_LEAN4EXPORT'] = str(exporter / '.lake/build/bin/lean4export')
    env.setdefault('LEAN_NUM_THREADS', '4')
    if trusted_local:
        env['COMPARATOR_LANDRUN'] = str(comparator / 'scripts/fake-landrun.sh')
        print('MODE: trusted local sources; no operating-system sandbox', flush=True)
    else:
        if platform.system() != 'Linux':
            raise RuntimeError('Sandboxed verification requires Linux; use --trusted-local only for trusted sources')
        landrun = base / 'landrun'
        checkout(lock['landrun'], landrun)
        run(['go', 'build', '-o', str(base / 'landrun-bin'), './cmd/landrun'], cwd=landrun)
        env['LANDRUN_EXECUTABLE'] = str(base / 'landrun-bin')
        env['COMPARATOR_LANDRUN'] = str(ROOT / 'scripts/landrun-runner.sh')
        check_sandbox(base / 'landrun-bin')
    return comparator / '.lake/build/bin/comparator', env


def invocation(binary, config, trusted_local):
    cmd = ['lake', 'env', str(binary), str(config)]
    if not trusted_local:
        cmd = guard() + ['-E', 'PATH', '-E', 'LEAN_NUM_THREADS', '-E', 'LANDRUN_EXECUTABLE',
                         '-E', 'COMPARATOR_LANDRUN', '-E', 'COMPARATOR_LEAN4EXPORT',
                         '--working-directory=' + str(ROOT), '--', *cmd]
    return cmd


def captured_run(binary, config, env, trusted_local, logfile):
    with logfile.open('w') as log:
        proc = subprocess.Popen(invocation(binary, config, trusted_local), cwd=ROOT,
                                env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT, text=True)
        assert proc.stdout is not None
        for line in proc.stdout:
            log.write(line)
            log.flush()
            print(line, end='', flush=True)
        code = proc.wait()
    return code, logfile.read_text()


def negative_tests(binary, env, trusted_local):
    """Reject a changed conclusion, an added premise and an extra axiom."""
    source = ROOT / 'Verification/ComparatorMismatch.lean'
    config = OUT / 'comparator-mismatch.json'
    if source.exists():
        raise RuntimeError('Refusing to replace an existing mismatch fixture')
    challenge = (ROOT / 'Verification/Challenge.lean').read_text()
    statement = challenge.split('theorem native_classification :', 1)[1].split(':= by', 1)[0]
    header = ('import Paper2.ExactInput.Recognition.NativeUniform\n'
              'namespace Paper2.Verification.Theorems\n'
              'open Paper2.Tractable Paper2.ExactInput Paper2.Problem\n'
              'noncomputable section\n')
    name = 'Paper2.Verification.Theorems.native_classification'
    mismatch = "Challenge and solution theorem statement do not match: '" + name + "'"
    cases = [
        ('different-statement', 'theorem native_classification : True := trivial\n', mismatch),
        ('added-premise', 'theorem native_classification (h : False) :' + statement +
         ':= False.elim h\n', mismatch),
        ('extra-axiom', 'axiom extraProof :' + statement + '\n'
         'theorem native_classification :' + statement + ':= extraProof\n',
         "Illegal axiom detected: 'Paper2.Verification.Theorems.extraProof'")]
    conf = json.loads((ROOT / 'Verification/comparator.json').read_text())
    conf.update(solution_module='Verification.ComparatorMismatch', theorem_names=[name])
    config.write_text(json.dumps(conf, indent=2) + '\n')
    results = []
    try:
        for label, body, rejection in cases:
            source.write_text(header + body + 'end\nend Paper2.Verification.Theorems\n')
            logfile = OUT / ('comparator-' + label + '.log')
            code, output = captured_run(binary, config, env, trusted_local, logfile)
            if code == 0 or rejection not in output:
                raise RuntimeError('Expected Comparator rejection missing: ' + label)
            results.append({'case': label, 'status': 'rejected_as_expected', 'exit_code': code,
                            'log': str(logfile.relative_to(ROOT)), 'log_sha256': digest(logfile)})
            print('COMPARATOR NEGATIVE TEST PASSED: ' + label, flush=True)
    finally:
        source.unlink(missing_ok=True)
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--trusted-local', action='store_true',
                        help='Use the upstream development shim for already trusted local sources')
    parser.add_argument('--setup-only', action='store_true')
    parser.add_argument('--negative-test', action='store_true')
    args = parser.parse_args()
    # Use the project's Lake environment without inheriting another checkout's
    # Lean search paths. On macOS prefer standalone Command Line Tools when present.
    for key in ('LEAN_PATH', 'LEAN_SRC_PATH'):
        os.environ.pop(key, None)
    if platform.system() == 'Darwin':
        clt = Path('/Library/Developer/CommandLineTools')
        if clt.is_dir():
            os.environ['DEVELOPER_DIR'] = str(clt)
            os.environ['PATH'] = str(clt / 'usr/bin') + os.pathsep + os.environ.get('PATH', '')
    os.environ['PATH'] = str(Path.home() / '.elan/bin') + os.pathsep + os.environ.get('PATH', '')
    OUT.mkdir(parents=True, exist_ok=True)
    receipt = OUT / ('comparator-setup.json' if args.setup_only else
                     'comparator-negative.json' if args.negative_test else 'comparator.json')
    report = {'status': 'started', 'at_utc': datetime.now(timezone.utc).isoformat(),
              'mode': 'trusted_local_without_os_sandbox' if args.trusted_local else 'linux_sandbox',
              'setup_only': args.setup_only, 'commit': os.environ.get('GITHUB_SHA')}
    receipt.write_text(json.dumps(report, indent=2) + '\n')
    before = snapshot()
    binary, env = setup(args.trusted_local)
    binaries = [binary, Path(env['COMPARATOR_LEAN4EXPORT'])]
    if not args.trusted_local:
        binaries.append(Path(env['LANDRUN_EXECUTABLE']))
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in binaries}
    if args.setup_only:
        report['status'] = 'tools_ready'
    elif args.negative_test:
        report['negative_tests'] = negative_tests(binary, env, args.trusted_local)
        report['status'] = 'passed'
    else:
        logfile = OUT / 'comparator.log'
        code, output = captured_run(binary, ROOT / 'Verification/comparator.json', env,
                                    args.trusted_local, logfile)
        if code or 'Lean default kernel accepts the solution' not in output or 'Your solution is okay!' not in output:
            raise RuntimeError('Comparator did not accept the solution: see ' + str(logfile))
        report.update(status='passed', exit_code=code,
                      kernel_replay='Lean default kernel accepts the solution',
                      log=str(logfile.relative_to(ROOT)), log_sha256=digest(logfile))
    if before != snapshot():
        raise RuntimeError('Source changed during comparison')
    if hashes != {str(p.relative_to(ROOT)): digest(p) for p in binaries}:
        raise RuntimeError('Verification binary changed during comparison')
    report.update(lean_toolchain=(ROOT / 'lean-toolchain').read_text().strip(),
                  config=json.loads((ROOT / 'Verification/comparator.json').read_text()),
                  source_files=len(before),
                  source_snapshot_sha256=hashlib.sha256(json.dumps(before, sort_keys=True).encode()).hexdigest(),
                  binary_sha256=hashes,
                  tools=json.loads((ROOT / 'Verification/tools.json').read_text()))
    receipt.write_text(json.dumps(report, indent=2) + '\n')
    print('COMPARATOR ' + report['status'].upper() + ': ' + str(receipt.relative_to(ROOT)))


if __name__ == '__main__':
    main()
