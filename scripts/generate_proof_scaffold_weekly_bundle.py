#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from html import escape
from pathlib import Path
import shutil
import subprocess
import tempfile

from proof_scaffold_ladder import STEP_LABELS
from proof_scaffold_weekly_bundle import PROBLEM_BY_KEY, ordered_sessions, session_rows

REPO = Path(__file__).resolve().parents[1]
ASSET_SVG = REPO / 'assets' / 'proof-scaffold-weekly-bundle.svg'
ASSET_PNG = REPO / 'assets' / 'proof-scaffold-weekly-bundle.png'
ASSET_CSV = REPO / 'assets' / 'proof-scaffold-weekly-bundle.csv'
NOTEBOOK = REPO / 'notebooks' / 'proof_scaffold_weekly_bundle.ipynb'

WIDTH = 1800
HEIGHT = 1540
DAY_COLORS = {
    'Day 1': '#38bdf8',
    'Day 2': '#22c55e',
    'Day 3': '#a78bfa',
    'Day 4': '#f97316',
    'Day 5': '#facc15',
}


def rect(x: float, y: float, w: float, h: float, fill: str, *, stroke: str = '#334155', rx: float = 22.0, stroke_width: float = 2.0) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'


def text(x: float, y: float, value: str, cls: str, *, anchor: str = 'start', fill: str | None = None) -> str:
    fill_attr = f' fill="{fill}"' if fill is not None else ''
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{fill_attr}>{escape(value)}</text>'


def block(x: float, y: float, lines: list[str], cls: str, *, anchor: str = 'start', line_step: int = 22, fill: str | None = None) -> str:
    fill_attr = f' fill="{fill}"' if fill is not None else ''
    tspans = []
    for index, value in enumerate(lines):
        dy = 0 if index == 0 else line_step
        tspans.append(f'<tspan x="{x:.1f}" dy="{dy}">{escape(value)}</tspan>')
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}"{fill_attr}>{"".join(tspans)}</text>'


def wrap(text_value: str, width: int) -> list[str]:
    words = text_value.split()
    if not words:
        return ['']
    lines = [words[0]]
    for word in words[1:]:
        candidate = f'{lines[-1]} {word}'
        if len(candidate) <= width:
            lines[-1] = candidate
        else:
            lines.append(word)
    return lines


def export_png(svg_path: Path, png_path: Path) -> None:
    brave_candidates = [
        Path('/Applications/Brave Browser.app/Contents/MacOS/Brave Browser'),
        Path(shutil.which('brave-browser') or ''),
    ]
    browser = next((candidate for candidate in brave_candidates if candidate and candidate.exists()), None)
    if browser is None:
        raise FileNotFoundError('Brave Browser is required for PNG export in this repo')
    with tempfile.TemporaryDirectory() as tmpdir:
        wrapper = Path(tmpdir) / 'wrapper.html'
        wrapper.write_text(
            '<html><head><style>'
            f'html,body{{margin:0;padding:0;width:{WIDTH}px;height:{HEIGHT}px;overflow:hidden;background:#071018;}}'
            f'img{{display:block;width:{WIDTH}px;height:{HEIGHT}px;}}'
            '</style></head><body>'
            f"<img src='{svg_path.resolve().as_uri()}'/>"
            '</body></html>'
        )
        command = [
            str(browser),
            '--headless',
            '--disable-gpu',
            '--hide-scrollbars',
            '--run-all-compositor-stages-before-draw',
            '--virtual-time-budget=1000',
            f'--screenshot={png_path.resolve()}',
            f'--window-size={WIDTH},{HEIGHT}',
            wrapper.resolve().as_uri(),
        ]
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        except subprocess.TimeoutExpired:
            if not png_path.exists():
                raise
    sips = shutil.which('sips')
    if sips is not None:
        subprocess.run([sips, '--setProperty', 'dpiWidth', '300', '--setProperty', 'dpiHeight', '300', str(png_path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def write_csv() -> None:
    rows = session_rows()
    ASSET_CSV.parent.mkdir(parents=True, exist_ok=True)
    with ASSET_CSV.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def notebook_markdown(lines: list[str]) -> dict[str, object]:
    return {
        'cell_type': 'markdown',
        'metadata': {},
        'source': [line if line.endswith('\n') else f'{line}\n' for line in lines],
    }


def notebook_code(lines: list[str]) -> dict[str, object]:
    return {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': [line if line.endswith('\n') else f'{line}\n' for line in lines],
    }


def write_notebook() -> None:
    sessions = ordered_sessions()
    cells: list[dict[str, object]] = []
    cells.append(notebook_markdown([
        '# Proof scaffold weekly bundle',
        '',
        'This notebook turns the proof scaffold ladder into one bounded week of writing pressure.',
        '',
        'The point is not more topics. The point is to stop letting the same missing move stay invisible.',
    ]))
    cells.append(notebook_markdown([
        '## How to use this notebook',
        '',
        '- Write the first draft before you scroll to the answer-check prompts for that day.',
        '- After each proof, mark every missed structural move in the tally.',
        '- On Day 5, use the tally to choose the two step families that need repair work instead of guessing.',
        '',
        'Related note: `notes/proof-scaffold-weekly-bundle.md`',
        'Related ladder packet: `notes/proof-scaffold-ladder.md`',
    ]))
    cells.append(notebook_code([
        'STEP_LABELS = {',
        *[f"    {step!r}: {label!r}," for step, label in STEP_LABELS.items()],
        '}',
        '',
        'failure_tally = {step: 0 for step in STEP_LABELS}',
        '',
        'def rank_failures(tally):',
        '    return sorted(tally.items(), key=lambda item: (-item[1], item[0]))',
        '',
        'rank_failures(failure_tally)',
    ]))

    for session in sessions:
        color = DAY_COLORS[session.label]
        focus_labels = ', '.join(STEP_LABELS[step] for step in session.focus_steps)
        problem_lines = []
        if session.problem_keys:
            for key in session.problem_keys:
                problem = PROBLEM_BY_KEY[key]
                problem_lines.append(f'- **{problem.title}** (`{key}`): {problem.prompt}')
        else:
            pool = ', '.join(PROBLEM_BY_KEY[key].title for key in session.repair_pool)
            problem_lines.append(f'- Adaptive repair set: choose from {pool}.')
        cells.append(notebook_markdown([
            f'## {session.label}: {session.title}',
            '',
            f'**Time box:** {session.minutes} minutes  ',
            f'**Focus steps:** {focus_labels}',
            '',
            '### Problems',
            *problem_lines,
            '',
            '### Deliverables',
            *[f'- {item}' for item in session.deliverables],
            '',
            f'**Exit gate:** {session.exit_gate}',
            '',
            f'**Reflection prompt:** {session.reflection_prompt}',
        ]))

        template = [
            '### Working page',
            '',
            '> Write here before you look back at the ladder note or any old attempt.',
            '',
        ]
        if session.problem_keys:
            for key in session.problem_keys:
                problem = PROBLEM_BY_KEY[key]
                template.extend([
                    f'#### {problem.title}',
                    '',
                    f'- Prompt: {problem.prompt}',
                    f'- Starter line to reveal only if needed: {problem.starter}',
                    '- First draft:',
                    '- First vague sentence or skipped move:',
                    '- Rewrite after answer-check prompts:',
                    '- Missed step families to add to the tally:',
                    '',
                    '**Answer-check prompts**',
                    *[f'- {check}' for check in problem.answer_checks],
                    '',
                ])
        else:
            template.extend([
                '- Top two missed step families from the tally:',
                '- Chosen repair problem #1:',
                '- Chosen repair problem #2:',
                '- Starter-free rewrite #1:',
                '- Starter-free rewrite #2:',
                '- Three-sentence audit for next week:',
                '',
                '**Repair rule**',
                '- If the missed family was arbitrary-object or close-the-claim, choose a proof-fluency or image-inside-kernel row.',
                '- If the missed family was witness-or-coefficients or contradiction-pivot, choose divisibility or independent-extension.',
                '- If the missed family was algebra-or-components, choose the rotation row.',
                '- If the missed family was closure-or-split, choose the kernel-subspace row.',
            ])
        cells.append(notebook_markdown(template))

    cells.append(notebook_markdown([
        '## References and follow-through',
        '',
        '- `notes/proof-method-cue-card.md`',
        '- `notes/proof-scaffold-ladder.md`',
        '- `notes/linear-algebra-bridge-packet.md`',
        '- `notes/invariant-lines-rotation-and-defect.md`',
        '',
        'If the same step family is still breaking by the end of the week, keep the next week on the same packet instead of escaping to a new topic.',
    ]))

    notebook = {
        'cells': cells,
        'metadata': {
            'kernelspec': {
                'display_name': 'Python 3',
                'language': 'python',
                'name': 'python3',
            },
            'language_info': {
                'name': 'python',
                'version': '3.12',
            },
        },
        'nbformat': 4,
        'nbformat_minor': 5,
    }
    NOTEBOOK.parent.mkdir(parents=True, exist_ok=True)
    NOTEBOOK.write_text(json.dumps(notebook, indent=2) + '\n')


def main() -> None:
    sessions = ordered_sessions()
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<defs>',
        '  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '    <stop offset="0%" stop-color="#071018"/>',
        '    <stop offset="100%" stop-color="#10233a"/>',
        '  </linearGradient>',
        '  <style>',
        '    .title { font: 700 40px Helvetica, Arial, sans-serif; fill: #e5eef7; }',
        '    .subtitle { font: 500 19px Helvetica, Arial, sans-serif; fill: #b4c3d4; }',
        '    .label { font: 700 22px Helvetica, Arial, sans-serif; fill: #dde7f1; }',
        '    .body { font: 500 17px Helvetica, Arial, sans-serif; fill: #c8d4e0; }',
        '    .small { font: 500 15px Helvetica, Arial, sans-serif; fill: #9fb2c7; }',
        '    .tiny { font: 500 14px Helvetica, Arial, sans-serif; fill: #92a5ba; }',
        '    .micro { font: 700 12px Helvetica, Arial, sans-serif; fill: #04111f; }',
        '  </style>',
        '</defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>',
        text(62, 68, 'Proof scaffold weekly bundle', 'title'),
        block(62, 104, [
            'One bounded week that turns the scaffold ladder into repeatable writing pressure.',
            'The added pressure is simple: cold drafts first, answer-check prompts second, a missed-step tally all week, and a final repair loop chosen from the tally instead of gut feel.',
        ], 'subtitle', line_step=24),
    ]

    left = 60.0
    top = 170.0
    card_w = 1030.0
    card_h = 214.0
    gap = 22.0

    for index, session in enumerate(sessions):
        y = top + index * (card_h + gap)
        color = DAY_COLORS[session.label]
        svg.append(rect(left, y, card_w, card_h, '#122033', stroke='#32485f', rx=28.0))
        svg.append(rect(left + 22, y + 18, 116, 30, color, stroke=color, rx=15.0, stroke_width=0.0))
        svg.append(text(left + 80, y + 39, session.label.upper(), 'micro', anchor='middle'))
        svg.append(text(left + 158, y + 44, session.title, 'label'))
        svg.append(text(left + 980, y + 44, f'{session.minutes} min', 'small', anchor='end'))

        problems = 'Adaptive repair from tally' if session.adaptive else '; '.join(PROBLEM_BY_KEY[key].title for key in session.problem_keys)
        focus = ', '.join(STEP_LABELS[step] for step in session.focus_steps)
        svg.append(block(left + 24, y + 82, wrap(f'Problems: {problems}', 92), 'body', line_step=21))
        svg.append(block(left + 24, y + 122, wrap(f'Focus: {focus}', 92), 'small', line_step=20))
        svg.append(block(left + 24, y + 158, wrap(f'Exit gate: {session.exit_gate}', 90), 'small', line_step=20))

    right = 1140.0
    top_right = 170.0
    panel_w = 600.0
    svg.append(rect(right, top_right, panel_w, 360, '#122033', stroke='#32485f', rx=28.0))
    svg.append(text(right + 24, top_right + 38, 'Why this is deeper than one good card', 'label'))
    bullets = [
        'The week keeps the same six structural moves visible, but now they have to survive on paper across five separate sessions.',
        'Days 1 to 4 assign a bounded proof packet instead of a giant worksheet, so the learner still has to rewrite weak proofs rather than drown them in volume.',
        'Day 5 refuses the usual fake reflection. The repair work has to come from the failure tally, not from whatever felt memorable.',
        'The notebook adds starter-free rewrites, answer-check prompts, and a short audit sentence after every session.',
    ]
    bullet_y = top_right + 82
    for bullet in bullets:
        svg.append(block(right + 24, bullet_y, wrap(f'• {bullet}', 56), 'body', line_step=23))
        bullet_y += 74

    mid_top = 556.0
    svg.append(rect(right, mid_top, panel_w, 308, '#122033', stroke='#32485f', rx=28.0))
    svg.append(text(right + 24, mid_top + 38, 'Failure tally and repair rule', 'label'))
    svg.append(block(right + 24, mid_top + 78, wrap('Track misses by the same six step families used in the scaffold ladder. Do not invent new categories just because a proof felt messy.', 58), 'body', line_step=23))
    tally_y = mid_top + 162
    for step, label in STEP_LABELS.items():
        svg.append(rect(right + 24, tally_y - 16, 14, 14, '#dbeafe', stroke='#dbeafe', rx=4.0, stroke_width=0.0))
        svg.append(text(right + 52, tally_y - 2, label, 'small'))
        tally_y += 28

    bottom_top = 890.0
    svg.append(rect(right, bottom_top, panel_w, 328, '#122033', stroke='#32485f', rx=28.0))
    svg.append(text(right + 24, bottom_top + 38, 'Companion notebook', 'label'))
    notebook_bullets = [
        'notebooks/proof_scaffold_weekly_bundle.ipynb',
        'One working page per day with prompts, starter lines, answer-check cues, and blank space for rewrites.',
        'A small Python tally helper keeps the top missed step families easy to rank before the Day 5 repair loop.',
        'Use it after notes/proof-scaffold-weekly-bundle.md and notes/proof-scaffold-ladder.md, not instead of them.',
    ]
    y = bottom_top + 82
    for bullet in notebook_bullets:
        prefix = '• ' if not bullet.startswith('notebooks/') else ''
        svg.append(block(right + 24, y, wrap(f'{prefix}{bullet}', 56), 'body', line_step=23))
        y += 64

    footer_top = 1260.0
    footer_w = 1680.0
    svg.append(rect(60.0, footer_top, footer_w, 210, '#122033', stroke='#32485f', rx=24.0))
    svg.append(text(84, footer_top + 38, 'Session rhythm', 'label'))
    rhythm = [
        '1. Cold draft before any rescue line.',
        '2. Run the answer-check prompts and mark each missed structural move.',
        '3. Rewrite the first vague hinge in full sentences.',
        '4. Finish with one sentence saying exactly what the proof established.',
        '5. Let the tally choose the Day 5 repair proofs.',
    ]
    x_positions = [84, 418, 758, 1098, 1438]
    for x, item in zip(x_positions, rhythm):
        svg.append(block(x, footer_top + 88, wrap(item, 22), 'body', line_step=23))

    svg.append(text(62, 1510, 'Generated from scripts/generate_proof_scaffold_weekly_bundle.py, scripts/proof_scaffold_weekly_bundle.py, and scripts/proof_scaffold_ladder.py', 'tiny'))
    svg.append('</svg>')

    ASSET_SVG.parent.mkdir(parents=True, exist_ok=True)
    ASSET_SVG.write_text('\n'.join(svg) + '\n')
    write_csv()
    write_notebook()
    export_png(ASSET_SVG, ASSET_PNG)
    print(f'WROTE {ASSET_SVG}, {ASSET_PNG}, {ASSET_CSV}, and {NOTEBOOK}')


if __name__ == '__main__':
    main()
