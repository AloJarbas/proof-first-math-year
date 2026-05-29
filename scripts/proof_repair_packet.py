from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from proof_scaffold_ladder import PROBLEMS, STEP_LABELS


PROBLEM_BY_KEY = {problem.key: problem for problem in PROBLEMS}
STEP_ORDER = {step: index for index, step in enumerate(STEP_LABELS, start=1)}


@dataclass(frozen=True)
class ProofRepairCase:
    key: str
    title: str
    problem_key: str
    primary_step: str
    bad_line: str
    diagnosis: str
    repair_prompt: str
    repaired_line: str
    transfer_check: str


CASES: tuple[ProofRepairCase, ...] = (
    ProofRepairCase(
        key='subset-arbitrary-object',
        title='Subset chains still need a first element',
        problem_key='subset-chain',
        primary_step='arbitrary-object',
        bad_line='Since B ⊆ C, anything in B is in C.',
        diagnosis='That sentence starts in the middle. The proof never chooses an arbitrary x ∈ A, so the inclusion A ⊆ B never gets used on the same object.',
        repair_prompt='Restart from one arbitrary x in A, then push that exact x through both inclusions.',
        repaired_line='Let x be arbitrary with x ∈ A. Since A ⊆ B, we have x ∈ B; since B ⊆ C, we have x ∈ C. Therefore A ⊆ C.',
        transfer_check='If the claim were A ∩ B ⊆ A, what is the first arbitrary object you would choose?',
    ),
    ProofRepairCase(
        key='divisibility-witness',
        title='Divisibility needs an actual witness',
        problem_key='divisibility-sum',
        primary_step='witness-or-coefficients',
        bad_line='Both b and c have a factor a, so b + c does too.',
        diagnosis='That is only a slogan. The integers witnessing a | b and a | c are still hidden, so the new witness for b + c never appears on the page.',
        repair_prompt='Name b = am and c = an first, then use m + n as the new witness instead of waving at a common factor.',
        repaired_line='Since a | b and a | c, there exist integers m and n with b = am and c = an. Then b + c = a(m + n), so a | (b + c).',
        transfer_check='If the claim were a | (b − c), which witness changes and which part of the proof stays the same?',
    ),
    ProofRepairCase(
        key='kernel-closure-split',
        title='A subspace proof cannot hide behind “by linearity”',
        problem_key='kernel-subspace',
        primary_step='closure-or-split',
        bad_line='Ker(T) is closed under addition and scalar multiplication by linearity.',
        diagnosis='That skips the whole structure. A kernel subspace proof still owes three visible checkpoints: zero vector, additive closure, and scalar closure.',
        repair_prompt='Write the three checkpoints separately and compute T(u + v) and T(αu) instead of summarizing them with one vague sentence.',
        repaired_line='First T(0) = 0, so 0 ∈ Ker(T). If u, v ∈ Ker(T), then T(u + v) = T(u) + T(v) = 0, so u + v ∈ Ker(T). If α is a scalar and u ∈ Ker(T), then T(αu) = αT(u) = 0, so αu ∈ Ker(T). Therefore Ker(T) is a subspace of V.',
        transfer_check='If you were proving Im(T) is a subspace, which checkpoint would need a new witness and which two would stay the same?',
    ),
    ProofRepairCase(
        key='rotation-components',
        title='A picture is not the contradiction',
        problem_key='rotation-no-real-line',
        primary_step='algebra-or-components',
        bad_line='A 60° rotation changes the direction, so no nonzero real line can stay invariant.',
        diagnosis='The intuition is fine, but the proof never turns “same line” into Ru = λu and never squeezes a contradiction out of the coordinate equations.',
        repair_prompt='Take u = (x, y) ≠ 0, assume Ru = λu for some real λ, and force the two rotated coordinates to agree with one real scalar.',
        repaired_line='Let u = (x, y) ≠ 0 and assume Ru = λu with λ ∈ ℝ. Then (x/2 − √3 y/2, √3 x/2 + y/2) = (λx, λy). From the two coordinates we get √3 y = (1 − 2λ)x and √3 x = (2λ − 1)y. Multiplying gives 3xy = −(2λ − 1)^2 xy, impossible when xy ≠ 0; if x = 0 or y = 0, the equations force the other coordinate to vanish too. Contradiction. Therefore no nonzero real invariant line exists.',
        transfer_check='For a 90° rotation, which real-scalar equation would fail first if you tried the same Ru = λu setup?',
    ),
    ProofRepairCase(
        key='independence-contradiction',
        title='Old independence cannot be used too early',
        problem_key='independent-extension',
        primary_step='contradiction-pivot',
        bad_line='Because v₁, …, v_k are linearly independent, all coefficients are zero.',
        diagnosis='Not yet. The old independence only applies after the new coefficient β has been forced to zero. Until then, the relation still contains the extra vector v.',
        repair_prompt='Start from one generic linear relation, isolate the β ≠ 0 branch, and use it to push v back into the old span before invoking the old independence.',
        repaired_line='Assume α₁v₁ + ··· + α_kv_k + βv = 0. If β ≠ 0, then v = −(α₁/β)v₁ − ··· − (α_k/β)v_k, so v lies in span(v₁, …, v_k), contradiction. Hence β = 0. Then α₁v₁ + ··· + α_kv_k = 0, so the old independence forces α₁ = ··· = α_k = 0. Therefore v₁, …, v_k, v are linearly independent.',
        transfer_check='In a basis-extension proof, which coefficient has to be isolated before the old independence becomes legal to use?',
    ),
    ProofRepairCase(
        key='image-kernel-close-claim',
        title='The computation is not the full inclusion',
        problem_key='square-zero-image-kernel',
        primary_step='close-the-claim',
        bad_line='So T(y) = 0.',
        diagnosis='That line only computes the kernel condition. The proof still has to say y ∈ Ker(T) and then cash the arbitrary choice of y out into Im(T) ⊆ Ker(T).',
        repair_prompt='After the computation, restate the membership fact and close the arbitrary-element argument as an inclusion sentence.',
        repaired_line='Take y ∈ Im(T). Then y = T(x) for some x ∈ V. Hence T(y) = T(T(x)) = T²(x) = 0, so y ∈ Ker(T). Because y was arbitrary in Im(T), we conclude Im(T) ⊆ Ker(T).',
        transfer_check='If you prove every y ∈ Y lies in Z, what closing sentence turns that pointwise fact into Y ⊆ Z?',
    ),
)


def ordered_cases(cases: Iterable[ProofRepairCase] = CASES) -> tuple[ProofRepairCase, ...]:
    return tuple(sorted(cases, key=lambda case: (STEP_ORDER[case.primary_step], case.key)))


def covered_steps(cases: Iterable[ProofRepairCase] = CASES) -> tuple[str, ...]:
    return tuple(case.primary_step for case in ordered_cases(cases))


def case_rows(cases: Iterable[ProofRepairCase] = CASES) -> tuple[dict[str, str], ...]:
    rows = []
    for case in ordered_cases(cases):
        problem = PROBLEM_BY_KEY[case.problem_key]
        rows.append(
            {
                'key': case.key,
                'title': case.title,
                'problem_key': case.problem_key,
                'problem_title': problem.title,
                'problem_stage': problem.stage,
                'problem_method': problem.method,
                'primary_step': case.primary_step,
                'primary_step_label': STEP_LABELS[case.primary_step],
                'bad_line': case.bad_line,
                'diagnosis': case.diagnosis,
                'repair_prompt': case.repair_prompt,
                'repaired_line': case.repaired_line,
                'transfer_check': case.transfer_check,
            }
        )
    return tuple(rows)
