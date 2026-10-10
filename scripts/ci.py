#!/usr/bin/env python3
"""Verify a clean build or compare the same commit's checked build artifact."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
from check import ROOT, digest, release_files, source_snapshot

OUT = ROOT / '.lake/verification'


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def sources():
    return source_snapshot(release_files())


def dependencies():
    for package in json.loads((ROOT / 'lake-manifest.json').read_text())['packages']:
        path = ROOT / '.lake/packages' / package['name']
        for args, expected in [(['rev-parse', 'HEAD'], package['rev']),
                               (['remote', 'get-url', 'origin'], package['url'])]:
            actual = subprocess.check_output(['git', '-C', str(path), *args], text=True).strip()
            if actual != expected:
                raise RuntimeError('Pinned dependency mismatch: ' + package['name'])
        subprocess.run(['git', '-C', str(path), 'diff', '--quiet', 'HEAD'], check=True)


def objects():
    root = ROOT / '.lake/build'
    return {str(p.relative_to(root)): digest(p) for p in sorted(root.rglob('*'))
            if p.is_file() and not p.name.endswith('.setup.json')}


def verify_build(report):
    directory = OUT / 'ci/build'
    build = json.loads((directory / 'result.json').read_text())
    if build['status'] != 'passed' or not build['clean_project_build']:
        raise RuntimeError('A successful clean build is required')
    for key in ('commit', 'source_snapshot_sha256'):
        if build[key] != report[key]:
            raise RuntimeError('Build artifact does not match this ' + key)
    manifest = directory / 'objects.json'
    if digest(manifest) != build['object_manifest_sha256']:
        raise RuntimeError('Build object manifest changed')
    expected = json.loads(manifest.read_text())
    if not expected or objects() != expected:
        raise RuntimeError('Build objects differ from the checked artifact')
    report['verified_build_artifact'] = True
    report['object_manifest_sha256'] = build['object_manifest_sha256']


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('phase', choices=['build', 'comparator'])
    args = parser.parse_args()
    directory = OUT / 'ci' / args.phase
    directory.mkdir(parents=True, exist_ok=True)
    report = {'status': 'running', 'phase': args.phase,
              'commit': os.environ.get('GITHUB_SHA'),
              'started_utc': datetime.now(timezone.utc).isoformat(), 'commands': []}
    result = directory / 'result.json'

    def save():
        result.write_text(json.dumps(report, indent=2) + '\n')

    def run(name, command):
        log = directory / (name + '.log')
        metrics = directory / (name + '-resources.txt')
        measured = ['/usr/bin/time', '-v', '-o', str(metrics), *command]
        started = time.monotonic()
        print(name + ': running', flush=True)
        with log.open('w') as output:
            process = subprocess.Popen(measured, cwd=ROOT, stdout=output, stderr=subprocess.STDOUT)
            while True:
                try:
                    code = process.wait(timeout=60)
                    break
                except subprocess.TimeoutExpired:
                    print(f'{name}: running; {log.stat().st_size} log bytes', flush=True)
        report['commands'].append({'name': name, 'command': command, 'exit_code': code,
                                   'elapsed_seconds': round(time.monotonic() - started, 2),
                                   'log_sha256': digest(log), 'resources_sha256': digest(metrics)})
        save()
        if code:
            print(log.read_text(errors='replace')[-12000:], file=sys.stderr)
            raise RuntimeError(name + ' failed; see its artifact log')
        print(name + ': passed', flush=True)

    try:
        if sys.platform != 'linux' or not report['commit']:
            raise RuntimeError('This driver requires Linux CI and GITHUB_SHA')
        for key in ('LEAN_PATH', 'LEAN_SRC_PATH'):
            os.environ.pop(key, None)
        before = sources()
        report['source_snapshot_sha256'] = fingerprint(before)
        (directory / 'sources.json').write_text(json.dumps(before, indent=2) + '\n')
        save()
        dependencies()
        version = subprocess.check_output(['lean', '--version'], cwd=ROOT, text=True).strip()
        if 'version 4.34.1,' not in version:
            raise RuntimeError('Unexpected Lean version: ' + version)
        report['lean_version'] = version
        if args.phase == 'build':
            shutil.rmtree(ROOT / '.lake/build', ignore_errors=True)
            report['clean_project_build'] = True
            run('build', ['bash', 'scripts/build.sh'])
            run('declarations', [sys.executable, 'scripts/check.py'])
            audit = json.loads((OUT / 'check.json').read_text())
            if audit['status'] != 'passed' or not audit['kernel']['passed']:
                raise RuntimeError('The declaration audit did not pass')
            if audit['static']['source_snapshot_sha256'] != report['source_snapshot_sha256']:
                raise RuntimeError('The declaration audit used a different source snapshot')
            report['declaration_audit'] = audit['kernel']
            manifest = directory / 'objects.json'
            compiled = objects()
            if not compiled:
                raise RuntimeError('Clean build produced no objects')
            manifest.write_text(json.dumps(compiled, indent=2) + '\n')
            report['object_manifest_sha256'] = digest(manifest)
        else:
            verify_build(report)
            run('negative-controls', [sys.executable, 'scripts/comparator.py', '--negative-test'])
            run('comparator', [sys.executable, 'scripts/comparator.py'])
            positive = json.loads((OUT / 'comparator.json').read_text())
            negative = json.loads((OUT / 'comparator-negative.json').read_text())
            for receipt in (positive, negative):
                if (receipt['status'] != 'passed' or receipt['mode'] != 'linux_sandbox'
                        or receipt['setup_only'] or receipt['commit'] != report['commit']
                        or receipt['source_snapshot_sha256'] != report['source_snapshot_sha256']):
                    raise RuntimeError('Comparator receipt does not match this verification')
            controls = negative['negative_tests']
            if ({r['case'] for r in controls} != {'different-statement', 'added-premise', 'extra-axiom'}
                    or len(controls) != 3
                    or any(r['status'] != 'rejected_as_expected' or r['exit_code'] == 0 for r in controls)):
                raise RuntimeError('Comparator rejection controls incomplete')
            report['comparator'] = positive
            report['negative_controls'] = controls
        dependencies()
        if sources() != before:
            raise RuntimeError('Release sources changed during verification')
        report.update(status='passed', source_unchanged=True)
    except Exception as error:
        report.update(status='failed', error=str(error))
        print(str(error), file=sys.stderr)
    finally:
        report['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save()
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    sys.exit(main())
