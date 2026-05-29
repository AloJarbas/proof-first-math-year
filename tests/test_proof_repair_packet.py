from __future__ import annotations

import csv
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
LADDER_PATH = REPO / 'scripts' / 'proof_scaffold_ladder.py'
LADDER_SPEC = importlib.util.spec_from_file_location('proof_scaffold_ladder', LADDER_PATH)
LADDER = importlib.util.module_from_spec(LADDER_SPEC)
assert LADDER_SPEC is not None and LADDER_SPEC.loader is not None
sys.modules[LADDER_SPEC.name] = LADDER
LADDER_SPEC.loader.exec_module(LADDER)

MODULE_PATH = REPO / 'scripts' / 'proof_repair_packet.py'
SPEC = importlib.util.spec_from_file_location('proof_repair_packet', MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ProofRepairPacketTests(unittest.TestCase):
    def test_step_coverage_matches_scaffold_families(self) -> None:
        self.assertEqual(set(MODULE.covered_steps()), set(LADDER.STEP_LABELS))
        self.assertEqual(len(MODULE.ordered_cases()), len(LADDER.STEP_LABELS))

    def test_every_case_points_to_real_problem_and_step(self) -> None:
        problem_keys = {problem.key for problem in LADDER.PROBLEMS}
        for case in MODULE.ordered_cases():
            self.assertIn(case.problem_key, problem_keys)
            self.assertIn(case.primary_step, LADDER.STEP_LABELS)
            self.assertTrue(case.bad_line)
            self.assertTrue(case.repaired_line)
            self.assertTrue(case.transfer_check.endswith('?'))

    def test_case_order_follows_step_order(self) -> None:
        expected = list(LADDER.STEP_LABELS)
        observed = [case.primary_step for case in MODULE.ordered_cases()]
        self.assertEqual(observed, expected)

    def test_case_rows_round_trip_to_csv(self) -> None:
        rows = MODULE.case_rows()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / 'repairs.csv'
            with path.open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator='\n')
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
            with path.open() as handle:
                loaded = list(csv.DictReader(handle))
        self.assertEqual([row['key'] for row in loaded], [case.key for case in MODULE.ordered_cases()])
        self.assertEqual(loaded[0]['primary_step'], 'arbitrary-object')
        self.assertEqual(loaded[-1]['primary_step'], 'close-the-claim')


if __name__ == '__main__':
    unittest.main()
