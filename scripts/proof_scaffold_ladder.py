from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


STEP_LABELS = {
    'arbitrary-object': 'choose an arbitrary object',
    'witness-or-coefficients': 'name the hidden witness or coefficients',
    'closure-or-split': 'split the closure or case step cleanly',
    'algebra-or-components': 'finish the algebra or coordinate cleanup',
    'contradiction-pivot': 'turn the false branch into a contradiction',
    'close-the-claim': 'say exactly what was proved',
}

STAGE_ORDER = {
    'proof fluency': 1,
    'linear algebra bridge': 2,
    'geometry follow-up': 3,
}


@dataclass(frozen=True)
class ProofScaffoldProblem:
    key: str
    title: str
    stage: str
    topic: str
    method: str
    difficulty: int
    prompt: str
    starter: str
    structural_sentence: str
    omitted_steps: tuple[str, ...]
    answer_checks: tuple[str, ...]
    common_slip: str

    @property
    def omitted_count(self) -> int:
        return len(self.omitted_steps)


PROBLEMS: tuple[ProofScaffoldProblem, ...] = (
    ProofScaffoldProblem(
        key='subset-chain',
        title='Subset chain',
        stage='proof fluency',
        topic='sets',
        method='direct',
        difficulty=1,
        prompt='Given A ⊆ B and B ⊆ C, prove A ⊆ C.',
        starter='Let x be ________. Then x ∈ B because ________, and x ∈ C because ________.',
        structural_sentence='Choose one arbitrary element from the first set and walk it through both inclusions.',
        omitted_steps=('arbitrary-object',),
        answer_checks=(
            'Did you start with an arbitrary x ∈ A instead of a special element?',
            'Did you actually use both subset hypotheses?',
            'Did you end with “therefore A ⊆ C”, not just “x ∈ C”?',
        ),
        common_slip='Starting from x ∈ B or x ∈ C skips the only structural move that matters.',
    ),
    ProofScaffoldProblem(
        key='divisibility-sum',
        title='Divisibility under addition',
        stage='proof fluency',
        topic='integers',
        method='direct',
        difficulty=2,
        prompt='If a | b and a | c, prove a | (b + c).',
        starter='Write b = ________ and c = ________. Then b + c = ________.',
        structural_sentence='Name the two divisibility witnesses first, then recombine them into one new witness.',
        omitted_steps=('witness-or-coefficients', 'algebra-or-components'),
        answer_checks=(
            'Did you introduce two integers witnessing a | b and a | c?',
            'Did you factor out a after adding the two expansions?',
            'Did you identify the new witness, rather than just circling the factor a?',
        ),
        common_slip='Saying “both have a factor a” is not yet a proof unless one witness for b + c is written down.',
    ),
    ProofScaffoldProblem(
        key='kernel-subspace',
        title='Kernel is a subspace',
        stage='linear algebra bridge',
        topic='linear maps',
        method='subspace proof',
        difficulty=3,
        prompt='Let T: V → W be linear. Prove that Ker(T) is a subspace of V.',
        starter='Show three things: 0 ∈ Ker(T), then if u, v ∈ Ker(T) prove ________, and if α is a scalar prove ________.',
        structural_sentence='The subspace proof is not one sentence. It is zero vector, additivity, and scalar closure in that order.',
        omitted_steps=('arbitrary-object', 'closure-or-split', 'close-the-claim'),
        answer_checks=(
            'Did you verify the zero vector separately?',
            'Did you compute T(u + v) and T(αu) using linearity, not just say “closure holds”?',
            'Did you conclude that all three subspace conditions are satisfied?',
        ),
        common_slip='Writing “kernels are always subspaces” is a memory cue, not the proof.',
    ),
    ProofScaffoldProblem(
        key='square-zero-image-kernel',
        title='T² = 0 forces Im(T) ⊆ Ker(T)',
        stage='linear algebra bridge',
        topic='linear maps',
        method='direct',
        difficulty=3,
        prompt='Let T: V → V be linear and suppose T² = 0. Prove Im(T) ⊆ Ker(T).',
        starter='Take y ∈ Im(T). Then y = ________ for some x ∈ V. Now compute T(y) = ________.',
        structural_sentence='To prove image inside kernel, start from an arbitrary image element and expose the hidden preimage.',
        omitted_steps=('arbitrary-object', 'witness-or-coefficients', 'close-the-claim'),
        answer_checks=(
            'Did you choose y from Im(T), not from all of V?',
            'Did you name a preimage x with y = T(x)?',
            'Did you end by saying y ∈ Ker(T), so Im(T) ⊆ Ker(T)?',
        ),
        common_slip='If the hidden preimage never appears, the proof cannot use the hypothesis T² = 0 in the right place.',
    ),
    ProofScaffoldProblem(
        key='independent-extension',
        title='Adjoining a vector outside the span',
        stage='linear algebra bridge',
        topic='independence',
        method='contradiction / linear combination',
        difficulty=4,
        prompt='If v₁, …, v_k are linearly independent and v ∉ span(v₁, …, v_k), prove that v₁, …, v_k, v are linearly independent.',
        starter='Assume α₁v₁ + ··· + α_kv_k + βv = 0. What happens if β ≠ 0?',
        structural_sentence='The key pivot is to force v into the old span if the new coefficient is nonzero, then contradict the hypothesis.',
        omitted_steps=('witness-or-coefficients', 'contradiction-pivot', 'close-the-claim'),
        answer_checks=(
            'Did you start from one generic linear relation equal to zero?',
            'Did you split the proof into the β ≠ 0 and β = 0 possibilities implicitly or explicitly?',
            'Did you use the original independence only after forcing β = 0?',
        ),
        common_slip='Using the old independence too early misses the actual reason the new vector is safe to adjoin.',
    ),
    ProofScaffoldProblem(
        key='rotation-no-real-line',
        title='A real rotation has no nonzero invariant line',
        stage='geometry follow-up',
        topic='invariant subspaces',
        method='contradiction / components',
        difficulty=5,
        prompt='Let R be rotation by 60° in ℝ². Prove that there is no nonzero real vector u with Ru = λu for some real λ.',
        starter='Take a nonzero u = (x, y) and assume Ru = λu. Compare the two coordinates of Ru with λx and λy.',
        structural_sentence='Turn “invariant line” back into coordinates: if Ru stayed on the same real line, one real scalar λ would have to fit both rotated coordinates at once.',
        omitted_steps=('arbitrary-object', 'algebra-or-components', 'contradiction-pivot', 'close-the-claim'),
        answer_checks=(
            'Did you start from one nonzero vector u and one real scalar λ?',
            'Did you compare both coordinates instead of arguing from a picture alone?',
            'Did the contradiction rule out every nonzero real invariant line, not just one sample vector?',
        ),
        common_slip='Pointing at a picture of a rotated arrow is good intuition, but it is not yet the contradiction.',
    ),
)


def ordered_problems(problems: Iterable[ProofScaffoldProblem] = PROBLEMS) -> tuple[ProofScaffoldProblem, ...]:
    return tuple(sorted(problems, key=lambda problem: (STAGE_ORDER[problem.stage], problem.difficulty, problem.key)))


def problem_rows(problems: Iterable[ProofScaffoldProblem] = PROBLEMS) -> tuple[dict[str, str], ...]:
    rows = []
    for problem in ordered_problems(problems):
        rows.append(
            {
                'key': problem.key,
                'title': problem.title,
                'stage': problem.stage,
                'topic': problem.topic,
                'method': problem.method,
                'difficulty': str(problem.difficulty),
                'omitted_count': str(problem.omitted_count),
                'omitted_steps': '; '.join(problem.omitted_steps),
                'structural_sentence': problem.structural_sentence,
                'common_slip': problem.common_slip,
            }
        )
    return tuple(rows)
