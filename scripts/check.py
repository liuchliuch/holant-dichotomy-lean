#!/usr/bin/env python3
"""Check release sources and the types/axioms of all required public statements.

Run scripts/build.sh first. This checker does not build libraries. Generated
Lean source, diagnostic output and the JSON result stay under ignored .lake/.
The comparator reference challenge is checked structurally, never imported into
the proof environment. Run scripts/comparator.py for its independent comparison.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
STANDARD_AXIOMS = {"propext", "Classical.choice", "Quot.sound"}
IMPORT = re.compile(r'^\s*(?:(?:public|meta)\s+)*import\s+(.+)$', re.M)
IDENTIFIER = re.compile(r"«[^»]*»|[\w][\w']*", re.UNICODE)
FORBIDDEN = {'sorry', 'admit', 'sorryAx', 'unsafe', 'native_decide',
             'native_decide_only', 'ofReduceBool', 'ofReduceNat', 'ofReduceInt',
             'ofReduceChar', 'ofReduceString', 'ofReduce', 'addDeclCore', 'axiomDecl'}
CHALLENGE = 'Verification.Challenge'
SOLUTION = 'Verification.Solution'
CJK = re.compile('[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]')
# Construct the patterns without embedding an actual private path in this file.
PRIVATE_PATH = re.compile('/' + r'(?:Users|home)/[^/\s]+|[A-Za-z]:\\Users\\')
IGNORED = {'.lake', '.git', '.tools'}
FORBIDDEN_NAMES = {'__pycache__', '.DS_Store', 'logs', 'node_modules', '.venv',
                   'venv', '.pytest_cache', '.mypy_cache', 'target', 'dist'}
BINARY_SUFFIXES = {'.pdf', '.png', '.jpg', '.jpeg', '.gif', '.zip', '.gz'}
ARTIFACT_SUFFIXES = {'.olean', '.ilean', '.ir', '.o', '.pyc', '.log', '.aux',
                     '.out', '.toc', '.synctex', '.trace', '.bak', '.tmp'}

def mask_lean(text: str) -> tuple[str, list[tuple[int, str]]]:
    """Mask comments/literals, retaining offsets, newlines, and interpolation code.

    Lean block comments nest. Escaped quotes, raw r#"..."# strings, character
    literals, and quoted identifiers cannot accidentally start comments.
    Expressions inside s!/m!/f! strings remain executable and are inspected.
    """
    out = list(text)
    problems: list[tuple[int, str]] = []
    n = len(text)

    def mask(a: int, b: int) -> None:
        for k in range(a, min(b, n)):
            if text[k] != '\n':
                out[k] = ' '

    def string(i: int, interpolated: bool) -> int:
        start = i
        mask(i, i + 1)
        i += 1
        while i < n:
            if text[i] == '\\':
                mask(i, i + 2)
                i += 2
            elif text[i] == '"':
                mask(i, i + 1)
                return i + 1
            elif interpolated and text[i:i + 2] in ('{{', '}}'):
                mask(i, i + 2)
                i += 2
            elif interpolated and text[i] == '{':
                mask(i, i + 1)
                i = code(i + 1, True)
            else:
                mask(i, i + 1)
                i += 1
        problems.append((start, 'unterminated string literal'))
        return n

    def code(i: int, interpolation: bool = False) -> int:
        braces = 1 if interpolation else 0
        while i < n:
            pair = text[i:i + 2]
            if pair == '/-':
                start, depth = i, 1
                i += 2
                while i < n and depth:
                    if text[i:i + 2] == '/-':
                        depth += 1
                        i += 2
                    elif text[i:i + 2] == '-/':
                        depth -= 1
                        i += 2
                    else:
                        i += 1
                mask(start, i)
                if depth:
                    problems.append((start, 'unterminated block comment'))
            elif pair == '--':
                end = text.find('\n', i)
                end = n if end < 0 else end
                mask(i, end)
                i = end
            elif text[i] == '«':
                # Contents are one identifier, not comment/string syntax.
                end = text.find('»', i + 1)
                if end < 0:
                    problems.append((i, 'unterminated quoted identifier'))
                    return n
                i = end + 1
            elif text[i] == 'r' and (i == 0 or not (text[i - 1].isalnum() or text[i - 1] in "_'")):
                raw = re.match(r'r(#+)?"', text[i:])
                if raw:
                    hashes = raw.group(1) or ''
                    end = text.find('"' + hashes, i + raw.end())
                    if end < 0:
                        problems.append((i, 'unterminated raw string literal'))
                        mask(i, n)
                        return n
                    end += 1 + len(hashes)
                    mask(i, end)
                    i = end
                else:
                    i += 1
            elif text[i] == '"':
                i = string(i, text[max(0, i - 2):i] in ('s!', 'm!', 'f!'))
            elif text[i] == "'":
                char = re.match(r"'(?:[^'\\\n]|\\(?:u\{[^}\n]+\}|[^\n]))'", text[i:])
                if char:
                    mask(i, i + char.end())
                    i += char.end()
                else:
                    i += 1  # Apostrophes are also legal identifier suffixes.
            elif interpolation and text[i] == '{':
                braces += 1
                i += 1
            elif interpolation and text[i] == '}':
                braces -= 1
                if braces == 0:
                    mask(i, i + 1)
                    return i + 1
                i += 1
            else:
                i += 1
        if interpolation:
            problems.append((n, 'unterminated string interpolation'))
        return n

    code(0)
    return ''.join(out), problems


def imports_of(clean: str) -> list[str]:
    result: list[str] = []
    for match in IMPORT.finditer(clean):
        result.extend(name for name in match[1].split() if name != 'all')
    return result


def executable_findings(clean: str) -> list[tuple[int, str]]:
    result = []
    for token in IDENTIFIER.finditer(clean):
        name = token[0]
        identifier = name[1:-1] if name.startswith('«') else name
        if identifier in FORBIDDEN:
            result.append((token.start(), 'forbidden executable token: ' + identifier))
        if name == 'axiom':
            result.append((token.start(), 'new explicit axiom declaration'))
    for match in re.finditer(r'\bset_option\s+(«[^»]+»|[\w.]+)\s+(true|false|[0-9]+)\b', clean):
        option = match[1].removeprefix('«').removesuffix('»')
        if option == 'debug.skipKernelTC' and match[2] == 'true':
            result.append((match.start(), 'kernel checking disabled'))
        if option in ('trustLevel', 'kernel.trustLevel') and match[2].isdigit() and int(match[2]) > 0:
            result.append((match.start(), 'nonzero kernel trust level'))
    return result


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            sha.update(block)
    return sha.hexdigest()


def release_files() -> list[Path]:
    result = []
    for directory, directories, files in os.walk(ROOT, followlinks=False):
        parent = Path(directory)
        directories[:] = sorted(d for d in directories if d not in IGNORED)
        for name in directories + files:
            path = parent / name
            if path.is_symlink():
                raise ValueError(f'Release contains a symlink: {path.relative_to(ROOT)}')
        result.extend(parent / name for name in sorted(files))
    return sorted(result)


def source_snapshot(paths: list[Path]) -> dict[str, str]:
    return {str(path.relative_to(ROOT)): digest(path) for path in paths}


def check_sources() -> tuple[dict, list[str], dict[str, Path]]:
    files, issues, modules, graph = release_files(), [], {}, {}
    for path in files:
        rel = str(path.relative_to(ROOT))
        if set(path.relative_to(ROOT).parts) & FORBIDDEN_NAMES or path.suffix in ARTIFACT_SUFFIXES:
            issues.append(f'Generated or unnecessary release file: {rel}')
        if path.suffix in BINARY_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeError:
            issues.append(f'Unrecognized binary file: {rel}')
            continue
        if CJK.search(text):
            issues.append(f'Non-English CJK text: {rel}')
        if PRIVATE_PATH.search(text):
            issues.append(f'Private absolute path: {rel}')
        if path.suffix != '.lean':
            continue
        module = '.'.join(path.relative_to(ROOT).with_suffix('').parts)
        modules[module] = path
        clean, lex_errors = mask_lean(text)
        issues.extend(f'{rel}:{text.count(chr(10), 0, offset) + 1}: {msg}'
                      for offset, msg in lex_errors)
        findings = executable_findings(clean)
        if module == CHALLENGE:
            holes = [(offset, msg) for offset, msg in findings
                     if msg == 'forbidden executable token: sorry']
            if len(holes) != 3:
                issues.append(f'{rel}: expected exactly three reference sorry terms')
            findings = [entry for entry in findings if entry not in holes]
        issues.extend(f'{rel}:{text.count(chr(10), 0, offset) + 1}: {msg}'
                      for offset, msg in findings)
        if re.search(r'#\s*(?:print|check|eval)\b', clean):
            issues.append(f'{rel}: diagnostic command belongs in the generated check')
        graph[module] = imports_of(clean)

    def closure(root: str) -> set[str]:
        seen, active = set(), set()
        def visit(name: str) -> None:
            if name in active:
                raise ValueError(f'Import cycle involving {name}')
            if name in seen:
                return
            if name not in modules:
                if name.split('.')[0] in {'Paper2', 'Holant', 'Verification'}:
                    issues.append(f'Missing local import: {name}')
                return
            active.add(name)
            for dependency in graph[name]:
                visit(dependency)
            active.remove(name)
            seen.add(name)
        visit(root)
        return seen

    public = closure('Paper2')
    solution = closure(SOLUTION)
    challenge = closure(CHALLENGE)
    retained = {name for name in modules if name.split('.')[0] in {'Paper2', 'Holant'}}
    if retained != public:
        issues.append('Unreachable retained proof modules: ' + ', '.join(sorted(retained - public)))
    if CHALLENGE in public | solution:
        issues.append('Reference challenge is reachable from a proof environment')
    if SOLUTION in challenge:
        issues.append('Reference challenge imports the solution')
    proof_imports = {name for name in challenge if name.startswith('Paper2.SourceFaithful.')
                     or name in {'Paper2', 'Paper2.PublicNativeClassification'}}
    if proof_imports:
        issues.append('Challenge imports classification proofs: ' + ', '.join(sorted(proof_imports)))
    if set(modules) - retained != {CHALLENGE, SOLUTION}:
        issues.append('Unexpected verification or unrelated Lean module')
    provenance = json.loads((ROOT / 'manuscript/provenance.json').read_text())
    if (provenance['arxiv_id'], provenance['version']) != ('2610.00081', 'v1'):
        issues.append('Manuscript provenance must identify arXiv 2610.00081v1')
    manuscript_files = provenance['files']
    if set(manuscript_files) != {'paper.tex', 'paper2-full-holant-dichotomy.bib', 'paper.pdf'}:
        issues.append('Expected the pinned manuscript TeX, bibliography and PDF')
    for name, expected in manuscript_files.items():
        path = (ROOT / 'manuscript' / name).resolve()
        if not path.is_relative_to(ROOT / 'manuscript') or not path.is_file():
            issues.append(f'Invalid manuscript path: {name}')
        elif digest(path) != expected:
            issues.append(f'Manuscript checksum mismatch: {name}')
    rows = json.loads((ROOT / 'docs/STATEMENT_LEDGER.json').read_text())
    required = [row for row in rows if row['scope'] == 'required']
    scopes = Counter(row['scope'] for row in rows)
    if len(rows) != 99 or len({row['number'] for row in rows}) != 99:
        issues.append('Expected 99 distinct manuscript rows')
    if scopes != {'required': 85, 'expository': 12, 'deferred': 2}:
        issues.append('Expected 85 required, 12 expository and two deferred rows')
    if sum(row['kind'] == 'definition' for row in required) != 5:
        issues.append('Expected five required definitions and 80 mathematical results')
    if {row['number'] for row in rows if row['scope'] == 'deferred'} != {'2.16', '2.17'}:
        issues.append('Only external results 2.16 and 2.17 are deferred')
    names = []
    for row in required:
        if not row.get('lean_declarations') or not row.get('lean_files'):
            issues.append(f'Missing declaration or file mapping for {row["number"]}')
        names.extend(row.get('lean_declarations', []))
        for name in row.get('lean_declarations', []):
            if not re.fullmatch(r'[A-Za-z_][\w]*(?:\.[A-Za-z_][\w]*)*', name):
                issues.append(f'Invalid declaration name: {name}')
        for source in row.get('lean_files', []):
            module = source.removesuffix('.lean').replace('/', '.')
            if module not in public:
                issues.append(f'Ledger file outside public closure: {source}')
    if len(names) != 196 or len(set(names)) != 176:
        issues.append('Expected 196 mappings covering 176 distinct required declarations')
    config = json.loads((ROOT / 'Verification/comparator.json').read_text())
    if config['challenge_module'] != CHALLENGE or config['solution_module'] != SOLUTION:
        issues.append('Unexpected comparator modules')
    if set(config['permitted_axioms']) != STANDARD_AXIOMS:
        issues.append('Comparator permits nonstandard axioms')
    if len(config['theorem_names']) != 3 or len(set(config['theorem_names'])) != 3:
        issues.append('Comparator must name exactly three distinct contracts')
    for name in config['theorem_names']:
        if not re.fullmatch(r'Paper2\.Verification\.Theorems\.[A-Za-z_][\w]*', name):
            issues.append(f'Invalid comparator declaration name: {name}')
    names = sorted(set(names) | set(config['theorem_names']))
    report = {
        'scope': 'Public Paper2 import closure and separately loaded comparator solution',
        'source_files': len(files),
        'public_modules': dict(Counter(name.split('.')[0] for name in public)),
        'verification_modules': 2,
        'ledger_rows': len(rows), 'required_rows': len(required),
        'required_declaration_mappings': sum(len(row['lean_declarations']) for row in required),
        'required_declarations': len(set(name for row in required for name in row['lean_declarations'])),
        'comparator_contracts': len(config['theorem_names']),
        'issues': issues,
        'source_snapshot_sha256': hashlib.sha256(json.dumps(source_snapshot(files), sort_keys=True).encode()).hexdigest(),
        'ledger_sha256': digest(ROOT / 'docs/STATEMENT_LEDGER.json'),
        'manuscript_files_verified': len(manuscript_files),
    }
    return report, names, {name: modules[name] for name in public | solution}


def inspect_output(output: str, expected: list[str]) -> dict:
    records = list(re.finditer(
        r"^'([^'\n]+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",
        output, re.M))
    axioms = Counter(match[1] for match in records)
    headers = Counter(re.findall(r'^(\w+(?:\.\w+)*)(?=\.\{|\s|:|\(|\{|$)', output, re.M))
    expected_counts = Counter(expected)
    # pp.universes prints the standard polymorphic axioms with one parameter.
    # Strip only a complete identifier-valued suffix, never arbitrary decoration.
    extra_axioms = {match[1]: sorted(set(re.sub(r'\.\{[A-Za-z_]\w*\}$', '', a.strip())
                                        for a in (match[2] or '').split(',') if a.strip())
                                    - STANDARD_AXIOMS) for match in records}
    extra_axioms = {name: values for name, values in extra_axioms.items() if values}
    diagnostics = [line for line in output.splitlines() if re.search(r'\b(?:error|warning):', line)]
    return {'expected': len(expected), 'type_records': sum(headers.values()),
            'axiom_records': sum(axioms.values()),
            'types_exactly_once': headers == expected_counts,
            'axioms_exactly_once': axioms == expected_counts,
            'unexpected_axioms': extra_axioms, 'diagnostics': diagnostics,
            'passed': headers == expected_counts and axioms == expected_counts
                      and not extra_axioms and not diagnostics}


def compiled_artifacts(proof_sources: dict[str, Path]) -> list[Path]:
    artifacts = []
    for module, source in proof_sources.items():
        obj = ROOT / '.lake/build/lib/lean' / (module.replace('.', '/') + '.olean')
        if not obj.is_file():
            raise ValueError(f'Missing compiled module {module}; run scripts/build.sh')
        artifacts.append(obj)
        for suffix in ('.private', '.server'):
            sidecar = obj.with_name(obj.name + suffix)
            if sidecar.is_file():
                artifacts.append(sidecar)
    return sorted(artifacts)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--static', '--static-only', action='store_true',
                        help='Inspect release sources without invoking Lean.')
    args = parser.parse_args()
    output_dir = ROOT / '.lake/verification'
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / 'check.json'
    report = {'status': 'failed', 'mode': 'static' if args.static else 'kernel'}
    report_path.write_text(json.dumps(report, indent=2) + '\n')
    try:
        report['static'], names, proof_sources = check_sources()
        if report['static']['issues']:
            raise ValueError('Static source checks failed')
        if not args.static:
            env = os.environ.copy()
            env.pop('LEAN_PATH', None)
            env.pop('LEAN_SRC_PATH', None)
            clt = Path('/Library/Developer/CommandLineTools')
            if sys.platform == 'darwin' and clt.is_dir():
                env['DEVELOPER_DIR'] = str(clt)
                env['PATH'] = str(clt / 'usr/bin') + os.pathsep + env.get('PATH', '')
            # Ask Lake to rehash build inputs and validate its dependency traces.
            # File timestamps alone are unreliable after copying sources.
            freshness_command = ['lake', '--rehash', '--no-build', 'build', 'Paper2', 'Verification']
            freshness = subprocess.run(freshness_command, cwd=ROOT, env=env, text=True,
                                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            freshness_log = output_dir / 'BuildFreshness.log'
            freshness_log.write_text(freshness.stdout)
            report['build_freshness'] = {'command': freshness_command,
                                         'exit_code': freshness.returncode,
                                         'log_sha256': digest(freshness_log)}
            if freshness.returncode:
                raise ValueError('Build outputs are not current; run scripts/build.sh')
            artifacts = compiled_artifacts(proof_sources)
            # Hash the actual local objects as well as source/configuration files.
            files = release_files()
            before = source_snapshot(files + sorted(artifacts))
            probe = output_dir / 'ExportCheck.lean'
            lines = ['import Paper2', 'import Verification.Solution',
                     'set_option pp.universes true', 'set_option pp.fullNames true', '']
            for name in names:
                lines += ['#check ' + name, '#print axioms ' + name]
            probe.write_text('\n'.join(lines) + '\n')
            command = ['lake', 'env', 'lean', str(probe.relative_to(ROOT))]
            process = subprocess.run(command, cwd=ROOT, env=env, text=True,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            log = output_dir / 'ExportCheck.log'
            log.write_text(process.stdout)
            report['kernel'] = inspect_output(process.stdout, names)
            report['kernel'].update({'command': command, 'exit_code': process.returncode,
                                     'probe_sha256': digest(probe), 'log_sha256': digest(log),
                                     'prebuilt_local_modules': len(proof_sources),
                                     'compiled_artifacts': len(artifacts)})
            after = source_snapshot(release_files() + compiled_artifacts(proof_sources))
            if before != after:
                raise ValueError('Sources, configuration or compiled objects changed during the probe')
            if process.returncode != 0 or not report['kernel']['passed']:
                raise ValueError('Kernel export check failed; see .lake/verification/ExportCheck.log')
            report['kernel']['source_and_object_snapshot_sha256'] = hashlib.sha256(
                json.dumps(before, sort_keys=True).encode()).hexdigest()
        report['status'] = 'passed'
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        report['error'] = str(error)
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
