#!/usr/bin/env python3
"""Read the numbered environments in the pinned self-contained STOC manuscript.

This is an inventory check, not a LaTeX interpreter or a mathematical verifier.
The source uses one section-local theorem counter shared by the listed aliases,
resets it for the embedded full paper, and prefixes that paper's sections by F.
Reject unsupported numbering changes instead of silently reusing an old ledger.
"""
from __future__ import annotations

import re

KINDS = 'theorem|lemma|proposition|corollary|definition|remark|procedure|claim'
TOKEN = re.compile(r'\\section(\*)?\s*\{|\\appendix\b|\\begin\{(' + KINDS + r')\}')


def mask_comments(source: str) -> str:
    """Keep source offsets and line numbers while removing ordinary TeX comments."""
    return re.sub(r'(?<!\\)%[^\n]*', lambda m: ' ' * len(m[0]), source)


def optional_title(source: str, start: int) -> str:
    while start < len(source) and source[start].isspace():
        start += 1
    if source[start:start + 1] != '[':
        return ''
    depth, braces = 1, 0
    for end in range(start + 1, len(source)):
        char = source[end]
        if end > 0 and source[end - 1] == '\\':
            continue
        if char == '{':
            braces += 1
        elif char == '}':
            braces -= 1
        elif braces == 0:
            if char == '[':
                depth += 1
            elif char == ']':
                depth -= 1
                if depth == 0:
                    return source[start + 1:end]
    raise ValueError('Unclosed manuscript statement title')


def numbered_environments(source: str) -> list[dict]:
    marker = '% BEGIN FULL PAPER'
    if source.count(marker) != 1:
        raise ValueError('Expected exactly one embedded full paper')
    boundary = source.index(marker)
    if r'\renewcommand{\thesection}{F.\arabic{section}}' not in source[:boundary]:
        raise ValueError('Unsupported full-paper section numbering')
    if r'\renewcommand{\thesection}{F.\Alph{section}}' not in source[boundary:]:
        raise ValueError('Unsupported full-paper appendix numbering')
    clean = mask_comments(source)
    section = counter = 0
    full = appendix = False
    rows = []
    for match in TOKEN.finditer(clean):
        if match.start() > boundary and not full:
            full, section, counter = True, 0, 0
        if match[0].startswith(r'\appendix'):
            appendix, section, counter = True, 0, 0
        elif match[0].startswith(r'\section'):
            if match[1] is None:
                section += 1
                counter = 0
        else:
            counter += 1
            kind = match[2]
            end = clean.find(r'\end{' + kind + '}', match.end())
            if end < 0:
                raise ValueError('Unclosed manuscript statement: ' + kind)
            body = clean[match.end():end]
            refs = []
            for ref in re.finditer(r'\\(?:cref|Cref|eqref|ref|lemref)\{([^}]+)\}', body):
                refs.extend(label.strip() for label in ref[1].split(','))
            section_name = chr(64 + section) if appendix else str(section)
            rows.append({
                'number': ('F.' if full else '') + section_name + '.' + str(counter),
                'kind': kind,
                'title': optional_title(clean, match.end()),
                'source_line': source.count('\n', 0, match.start()) + 1,
                'labels': re.findall(r'\\label\{([^}]+)\}', body),
                'referenced_labels': refs,
                'source': 'manuscript/paper.tex',
                'source_part': 'full' if full else 'short',
            })
    return rows


def correspondence_issues(source: str, ledger: list[dict]) -> list[str]:
    actual = numbered_environments(source)
    issues = []
    if len(actual) != len(ledger):
        issues.append(f'Manuscript has {len(actual)} numbered environments; ledger has {len(ledger)}')
    for expected, row in zip(actual, ledger):
        for key, value in expected.items():
            if row.get(key) != value:
                issues.append(f'Manuscript correspondence mismatch for {expected["number"]}: {key}')
    return issues
