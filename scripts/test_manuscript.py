#!/usr/bin/env python3
"""Negative controls for the source-to-ledger inventory (no Lean build)."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
from manuscript import correspondence_issues, numbered_environments

ROOT = Path(__file__).resolve().parents[1]


class ManuscriptInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = (ROOT / 'manuscript/paper.tex').read_text()
        cls.ledger = json.loads((ROOT / 'docs/STATEMENT_LEDGER.json').read_text())

    def test_complete_current_inventory(self):
        self.assertEqual(correspondence_issues(self.source, self.ledger), [])
        self.assertEqual(len(self.ledger), 94)
        self.assertEqual(self.ledger[-1]['number'], 'F.A.9')

    def test_stale_mapping_is_rejected(self):
        for field, stale in [('number', '9.2'), ('source_line', 5886),
                             ('labels', ['wrong:label']), ('title', 'Old title'),
                             ('referenced_labels', ['wrong:reference'])]:
            with self.subTest(field=field):
                rows = copy.deepcopy(self.ledger)
                rows[0][field] = stale
                self.assertTrue(correspondence_issues(self.source, rows))
        self.assertTrue(correspondence_issues(self.source, self.ledger[:-1]))

    def test_comments_do_not_add_theorems(self):
        fake = '% \\begin{theorem}[This is not a statement] \\end{theorem}\n'
        source = self.source + fake
        self.assertEqual(numbered_environments(source), numbered_environments(self.source))


if __name__ == '__main__':
    unittest.main()
