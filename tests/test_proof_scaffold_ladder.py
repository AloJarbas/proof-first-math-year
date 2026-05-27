from __future__ import annotations

import csv
import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO / 'scripts' / 'proof_scaffold_ladder.py'
SPEC = importlib.util.spec_from_file_location('proof_scaffold_ladder', MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ProofScaffoldLadderTests(unittest.TestCase):
    def test_difficulty_climbs_with_stage_order(self) -> None:
        problems = MODULE.ordered_problems()
        stage_ranks = [MODULE.STAGE_ORDER[problem.stage] for problem in problems]
        self.assertEqual(stage_ranks, sorted(stage_ranks))
        for left, right in zip(problems, problems[1:]):
            if MODULE.STAGE_ORDER[left.stage] == MODULE.STAGE_ORDER[right.stage]:
                self.assertLessEqual(left.difficulty, right.difficulty)

    def test_every_problem_has_real_scaffold_pressure(self) -> None:
        for problem in MODULE.PROBLEMS:
            self.assertGreaterEqual(problem.omitted_count, 1)
            self.assertGreaterEqual(len(problem.answer_checks), 3)
            for step in problem.omitted_steps:
                self.assertIn(step, MODULE.STEP_LABELS)

    def test_rotation_problem_needs_contradiction_pivot(self) -> None:
        rotation = next(problem for problem in MODULE.PROBLEMS if problem.key == 'rotation-no-real-line')
        self.assertIn('contradiction-pivot', rotation.omitted_steps)
        self.assertIn('algebra-or-components', rotation.omitted_steps)
        self.assertEqual(rotation.stage, 'geometry follow-up')

    def test_problem_rows_round_trip_to_csv(self) -> None:
        rows = MODULE.problem_rows()
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / 'rows.csv'
            with path.open('w', newline='') as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator='\n')
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
            with path.open() as handle:
                loaded = list(csv.DictReader(handle))
        self.assertEqual([row['key'] for row in loaded], [problem.key for problem in MODULE.ordered_problems()])
        self.assertEqual([row['difficulty'] for row in loaded], [str(problem.difficulty) for problem in MODULE.ordered_problems()])


if __name__ == '__main__':
    unittest.main()
