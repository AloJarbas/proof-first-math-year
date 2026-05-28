from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from proof_scaffold_ladder import PROBLEMS, STEP_LABELS


PROBLEM_BY_KEY = {problem.key: problem for problem in PROBLEMS}


@dataclass(frozen=True)
class WeeklyBundleSession:
    key: str
    label: str
    title: str
    minutes: int
    problem_keys: tuple[str, ...]
    focus_steps: tuple[str, ...]
    deliverables: tuple[str, ...]
    exit_gate: str
    reflection_prompt: str
    adaptive: bool = False
    repair_pool: tuple[str, ...] = ()


SESSIONS: tuple[WeeklyBundleSession, ...] = (
    WeeklyBundleSession(
        key='day-1-proof-reset',
        label='Day 1',
        title='Proof fluency reset',
        minutes=35,
        problem_keys=('subset-chain', 'divisibility-sum'),
        focus_steps=('arbitrary-object', 'witness-or-coefficients', 'close-the-claim'),
        deliverables=(
            'Write both proofs cold before looking at the starter line.',
            'After the first draft, use the answer-check prompts and replace the first vague sentence with a real structural sentence.',
            'Log every missed step family in the tally before moving on.',
        ),
        exit_gate='Each proof starts from the right object or witness and ends with the full claim, not only the last symbolic line.',
        reflection_prompt='Which skipped move felt harmless until you had to write it out?',
    ),
    WeeklyBundleSession(
        key='day-2-linear-map-discipline',
        label='Day 2',
        title='Linear-map closure discipline',
        minutes=45,
        problem_keys=('kernel-subspace', 'square-zero-image-kernel'),
        focus_steps=('closure-or-split', 'witness-or-coefficients', 'close-the-claim'),
        deliverables=(
            'For the kernel proof, keep zero vector, additivity, and scalar closure as three visible checkpoints.',
            'For the image-inside-kernel proof, name the hidden preimage before using T² = 0.',
            'Do one clean rewrite of the weaker proof with the starter hidden.',
        ),
        exit_gate='No line says “closure holds” or “clearly” where a computation or subset sentence should appear.',
        reflection_prompt='Which proof step was easiest to remember in your head but easiest to skip on paper?',
    ),
    WeeklyBundleSession(
        key='day-3-contradiction-bridge',
        label='Day 3',
        title='Contradiction pivot under pressure',
        minutes=35,
        problem_keys=('independent-extension',),
        focus_steps=('witness-or-coefficients', 'contradiction-pivot', 'close-the-claim'),
        deliverables=(
            'Write one full contradiction proof for adjoining a vector outside the old span.',
            'Then restart the same proof from scratch in five minutes with no starter line.',
            'Mark whether you tried to use the old independence before forcing β = 0.',
        ),
        exit_gate='The proof only counts if β ≠ 0 is the pivot that forces v into the old span before the original independence appears.',
        reflection_prompt='Did the contradiction arrive from the right branch, or did you jump to the old theorem too early?',
    ),
    WeeklyBundleSession(
        key='day-4-geometry-pressure',
        label='Day 4',
        title='Geometry without slogan memory',
        minutes=40,
        problem_keys=('rotation-no-real-line',),
        focus_steps=('arbitrary-object', 'algebra-or-components', 'contradiction-pivot', 'close-the-claim'),
        deliverables=(
            'Turn the invariant-line picture back into coordinates for one nonzero vector and one real scalar λ.',
            'Write the contradiction from the coordinate equations, not from a picture caption.',
            'Finish by ruling out every nonzero real invariant line, not only the sample vector.',
        ),
        exit_gate='The contradiction has to come from the coordinate comparison itself, not from visual intuition alone.',
        reflection_prompt='Which part still wanted to hide inside the diagram instead of the algebra?',
    ),
    WeeklyBundleSession(
        key='day-5-repair-loop',
        label='Day 5',
        title='Repair loop and final rewrite',
        minutes=30,
        problem_keys=(),
        focus_steps=tuple(STEP_LABELS),
        deliverables=(
            'Pick the two most frequent missed step families from the tally.',
            'Choose one earlier problem for each family and rewrite it with no starter line.',
            'End with a three-sentence audit: what failed early, what changed, and what still needs work next week.',
        ),
        exit_gate='The week only counts if the final rewrites replace the old vague hinge with a visible structural move.',
        reflection_prompt='Which structural move still collapses first under light time pressure?',
        adaptive=True,
        repair_pool=tuple(problem.key for problem in PROBLEMS),
    ),
)


def ordered_sessions(sessions: Iterable[WeeklyBundleSession] = SESSIONS) -> tuple[WeeklyBundleSession, ...]:
    return tuple(sorted(sessions, key=lambda session: int(session.label.split()[-1])))


def all_problem_keys(sessions: Iterable[WeeklyBundleSession] = SESSIONS) -> tuple[str, ...]:
    seen: list[str] = []
    for session in ordered_sessions(sessions):
        for key in session.problem_keys:
            if key not in seen:
                seen.append(key)
    return tuple(seen)


def covered_focus_steps(sessions: Iterable[WeeklyBundleSession] = SESSIONS) -> tuple[str, ...]:
    seen: list[str] = []
    for session in ordered_sessions(sessions):
        for step in session.focus_steps:
            if step not in seen:
                seen.append(step)
    return tuple(seen)


def session_rows(sessions: Iterable[WeeklyBundleSession] = SESSIONS) -> tuple[dict[str, str], ...]:
    rows = []
    for session in ordered_sessions(sessions):
        titles = [PROBLEM_BY_KEY[key].title for key in session.problem_keys]
        rows.append(
            {
                'key': session.key,
                'label': session.label,
                'title': session.title,
                'minutes': str(session.minutes),
                'problem_keys': '; '.join(session.problem_keys),
                'problem_titles': '; '.join(titles),
                'focus_steps': '; '.join(session.focus_steps),
                'focus_labels': '; '.join(STEP_LABELS[step] for step in session.focus_steps),
                'deliverables': ' | '.join(session.deliverables),
                'exit_gate': session.exit_gate,
                'reflection_prompt': session.reflection_prompt,
                'adaptive': 'yes' if session.adaptive else 'no',
            }
        )
    return tuple(rows)
