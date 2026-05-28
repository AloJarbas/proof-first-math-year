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

MODULE_PATH = REPO / 'scripts' / 'proof_scaffold_weekly_bundle.py'
SPEC = importlib.util.spec_from_file_location('proof_scaffold_weekly_bundle', MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ProofScaffoldWeeklyBundleTests(unittest.TestCase):
    def test_fixed_days_cover_every_scaffold_problem(self) -> None:
        fixed_sessions = [session for session in MODULE.ordered_sessions() if not session.adaptive]
        covered = {key for session in fixed_sessions for key in session.problem_keys}
        self.assertEqual(covered, {problem.key for problem in LADDER.PROBLEMS})

    def test_focus_coverage_hits_every_step_family_by_day_five(self) -> None:
        self.assertEqual(set(MODULE.covered_focus_steps()), set(LADDER.STEP_LABELS))

    def test_day_five_is_adaptive_repair_from_existing_pool(self) -> None:
        last = MODULE.ordered_sessions()[-1]
        self.assertTrue(last.adaptive)
        self.assertEqual(set(last.repair_pool), {problem.key for problem in LADDER.PROBLEMS})
        self.assertFalse(last.problem_keys)

    def test_session_rows_round_trip_to_csv(self) -> None:
        rows = MODULE.session_rows()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / 'weekly.csv'
            with path.open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator='\n')
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
            with path.open() as handle:
                loaded = list(csv.DictReader(handle))
        self.assertEqual([row['key'] for row in loaded], [session.key for session in MODULE.ordered_sessions()])
        self.assertEqual(loaded[-1]['adaptive'], 'yes')


if __name__ == '__main__':
    unittest.main()
