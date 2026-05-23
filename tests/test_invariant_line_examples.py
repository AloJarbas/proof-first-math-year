from __future__ import annotations

import csv
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO / 'scripts' / 'invariant_line_examples.py'
SPEC = importlib.util.spec_from_file_location('invariant_line_examples', MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class InvariantLineExampleTests(unittest.TestCase):
    def test_real_invariant_line_counts_match_the_three_cases(self) -> None:
        counts = {example.key: MODULE.real_invariant_line_count(example.matrix) for example in MODULE.EXAMPLES}
        self.assertEqual(counts['diagonal'], 2)
        self.assertEqual(counts['rotation'], 0)
        self.assertEqual(counts['jordan'], 1)

    def test_rotation_has_negative_discriminant(self) -> None:
        rotation = next(example for example in MODULE.EXAMPLES if example.key == 'rotation')
        self.assertLess(MODULE.discriminant(rotation.matrix), 0.0)

    def test_jordan_keeps_only_the_x_axis_closed(self) -> None:
        jordan = next(example for example in MODULE.EXAMPLES if example.key == 'jordan')
        directions = MODULE.real_invariant_line_directions(jordan.matrix)
        self.assertEqual(len(directions), 1)
        self.assertAlmostEqual(directions[0][0], 1.0, places=6)
        self.assertAlmostEqual(directions[0][1], 0.0, places=6)

    def test_summary_rows_write_clean_csv(self) -> None:
        rows = MODULE.example_rows()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / 'rows.csv'
            with path.open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator='\n')
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
            with path.open() as handle:
                loaded = list(csv.DictReader(handle))
        self.assertEqual([row['key'] for row in loaded], ['diagonal', 'rotation', 'jordan'])


if __name__ == '__main__':
    unittest.main()
