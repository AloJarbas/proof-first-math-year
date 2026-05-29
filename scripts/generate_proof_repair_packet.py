#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from html import escape
from pathlib import Path
import shutil
import subprocess
import tempfile

from proof_repair_packet import PROBLEM_BY_KEY, case_rows, ordered_cases
from proof_scaffold_ladder import STEP_LABELS

REPO = Path(__file__).resolve().parents[1]
ASSET_SVG = REPO / 'assets' / 'proof-repair-packet.svg'
ASSET_PNG = REPO / 'assets' / 'proof-repair-packet.png'
ASSET_CSV = REPO / 'assets' / 'proof-repair-packet.csv'
NOTEBOOK = REPO / 'notebooks' / 'proof_repair_packet.ipynb'

WIDTH = 1800
HEIGHT = 2020
STEP_COLORS = {
    'arbitrary-object': '#38bdf8',
    'witness-or-coefficients': '#f59e0b',
    'closure-or-split': '#22c55e',
    'algebra-or-components': '#a78bfa',
    'contradiction-pivot': '#f97316',
    'close-the-claim': '#f43f5e',
}
BADGE_LABELS = {
    'arbitrary-object': 'ARBITRARY OBJECT',
    'witness-or-coefficients': 'WITNESS / COEFFS',
    'closure-or-split': 'CLOSURE SPLIT',
    'algebra-or-components': 'ALGEBRA / COORDS',
    'contradiction-pivot': 'CONTRADICTION PIVOT',
    'close-the-claim': 'CLOSE THE CLAIM',
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
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=60)
        except subprocess.TimeoutExpired:
            if not png_path.exists():
                raise
    sips = shutil.which('sips')
    if sips is not None:
        subprocess.run([sips, '--setProperty', 'dpiWidth', '300', '--setProperty', 'dpiHeight', '300', str(png_path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def write_csv() -> None:
    rows = case_rows()
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
    cases = ordered_cases()
    cells: list[dict[str, object]] = []
    cells.append(notebook_markdown([
        '# Bad proof to repaired proof packet',
        '',
        'This notebook is for the moment after a proof attempt fails but before the learner has any idea how to rewrite it cleanly.',
        '',
        'Each case keeps one plausible weak line visible, diagnoses the missing structural move, and then rewrites the hinge instead of only showing a polished final proof.',
    ]))
    cells.append(notebook_markdown([
        '## How to use this packet',
        '',
        '- Start from a weak line that sounds familiar, not from the repaired version.',
        '- Name the missing step family before you read the repair sentence.',
        '- Rewrite the hinge yourself once with the source problem in view and once without the starter line.',
        '- Use the transfer question to make sure the repair generalizes instead of staying tied to one example.',
        '',
        'Best companion files:',
        '- `notes/bad-proof-to-repaired-proof-packet.md`',
        '- `notes/proof-scaffold-weekly-bundle.md`',
        '- `notes/proof-scaffold-ladder.md`',
    ]))
    cells.append(notebook_code([
        'STEP_LABELS = {',
        *[f"    {step!r}: {label!r}," for step, label in STEP_LABELS.items()],
        '}',
        'cases = [',
        *[
            '    {' +
            f"'key': {case.key!r}, 'title': {case.title!r}, 'step': {case.primary_step!r}, "
            f"'problem': {PROBLEM_BY_KEY[case.problem_key].title!r}" +
            '},'
            for case in cases
        ],
        ']',
        'cases',
    ]))

    for case in cases:
        problem = PROBLEM_BY_KEY[case.problem_key]
        step_label = STEP_LABELS[case.primary_step]
        cells.append(notebook_markdown([
            f'## {case.title}',
            '',
            f'**Source problem:** {problem.title}  ',
            f'**Primary step family:** {step_label}  ',
            f'**Method:** {problem.method}  ',
            f'**Prompt:** {problem.prompt}',
            '',
            '### The weak line',
            f'> {case.bad_line}',
            '',
            '### Why it fails',
            case.diagnosis,
            '',
            '### Repair cue',
            case.repair_prompt,
        ]))
        cells.append(notebook_markdown([
            '### Working page',
            '',
            f'- Starter line from the source problem: {problem.starter}',
            '- Your diagnosis in one sentence:',
            '- Your rewrite before looking at the repaired hinge:',
            '- Which word or phrase was doing fake work in the bad line?',
            '',
            '**Answer-check prompts from the source problem**',
            *[f'- {check}' for check in problem.answer_checks],
            '',
            '**Repaired hinge**',
            f'- {case.repaired_line}',
            '',
            '**Transfer check**',
            f'- {case.transfer_check}',
            '',
            '**One more rewrite**',
            '- Hide the starter line and rewrite the same hinge again in fewer sentences.',
        ]))

    cells.append(notebook_markdown([
        '## Follow-through',
        '',
        'If one step family keeps recurring, go back to the weekly bundle and build the next repair session around that family instead of opening a brand new topic.',
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
    cases = ordered_cases()
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
        '    .body { font: 500 19px Helvetica, Arial, sans-serif; fill: #c8d4e0; }',
        '    .small { font: 500 15px Helvetica, Arial, sans-serif; fill: #a8bacd; }',
        '    .tiny { font: 500 16px Helvetica, Arial, sans-serif; fill: #9cb0c4; }',
        '    .micro { font: 700 11px Helvetica, Arial, sans-serif; fill: #071018; }',
        '  </style>',
        '</defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>',
        text(60, 72, 'Bad proof to repaired proof', 'title'),
        block(60, 108, [
            'A repair packet for the moment after the proof breaks but before the learner knows how to rewrite the hinge.',
            'Each row keeps one plausible bad line on the page, names the missing structural move, and then shows the repair sentence that actually closes the gap.',
        ], 'subtitle', line_step=24),
    ]

    svg.append(rect(60, 160, 1680, 140, '#122033', stroke='#32485f', rx=28.0))
    svg.append(text(84, 198, 'Use it in four moves', 'label'))
    instructions = [
        '1. Match your weak proof to the row whose bad line sounds dangerously familiar.',
        '2. Name the missing step family before reading the repair sentence.',
        '3. Rewrite the hinge once with the source prompt visible and once without the starter line.',
        '4. Use the transfer check so the repair survives outside the original example.',
    ]
    y_cursor = 228.0
    for line in instructions:
        wrapped = wrap(line, 80)
        svg.append(block(90, y_cursor, wrapped, 'body', line_step=21))
        y_cursor += 21 * len(wrapped) + 10

    left = 60.0
    card_w = 1680.0
    top = 340.0
    card_h = 242.0
    gap = 24.0
    for index, case in enumerate(cases):
        y = top + index * (card_h + gap)
        problem = PROBLEM_BY_KEY[case.problem_key]
        color = STEP_COLORS[case.primary_step]
        svg.append(rect(left, y, card_w, card_h, '#122033', stroke='#32485f', rx=28.0))
        svg.append(rect(left + 24, y + 20, 268, 34, color, stroke=color, rx=16.0, stroke_width=0.0))
        svg.append(text(left + 158, y + 43, BADGE_LABELS[case.primary_step], 'micro', anchor='middle'))
        svg.append(text(left + 314, y + 47, case.title, 'label'))
        svg.append(text(left + 1638, y + 47, problem.title, 'small', anchor='end'))

        svg.append(text(left + 34, y + 88, 'Bad line', 'small', fill='#fca5a5'))
        svg.append(block(left + 34, y + 114, wrap(case.bad_line, 54), 'body', line_step=22, fill='#fee2e2'))
        svg.append(text(left + 34, y + 172, 'Why it fails', 'small', fill='#93c5fd'))
        svg.append(block(left + 34, y + 198, wrap(case.diagnosis, 60), 'tiny', line_step=21))

        svg.append(text(left + 720, y + 88, 'Repair cue', 'small', fill='#fde68a'))
        svg.append(block(left + 720, y + 114, wrap(case.repair_prompt, 58), 'body', line_step=22, fill='#fef3c7'))
        svg.append(text(left + 720, y + 172, 'Repaired hinge', 'small', fill='#86efac'))
        svg.append(block(left + 720, y + 198, wrap(case.repaired_line, 82), 'tiny', line_step=21, fill='#dcfce7'))

        svg.append(text(left + 1450, y + 88, 'Transfer check', 'small', fill='#c4b5fd'))
        svg.append(block(left + 1450, y + 114, wrap(case.transfer_check, 27), 'body', line_step=22, fill='#ede9fe'))

    footer_y = HEIGHT - 92.0
    svg.append(rect(60, footer_y, 1680, 58, '#122033', stroke='#32485f', rx=24.0))
    svg.append(text(84, footer_y + 34, 'Companion files: notes/bad-proof-to-repaired-proof-packet.md · notebooks/proof_repair_packet.ipynb · assets/proof-repair-packet.csv', 'small'))
    svg.append(text(1740, HEIGHT - 24, 'Generated by scripts/generate_proof_repair_packet.py', 'tiny', anchor='end'))
    svg.append('</svg>')

    ASSET_SVG.write_text('\n'.join(svg))
    export_png(ASSET_SVG, ASSET_PNG)
    write_csv()
    write_notebook()


if __name__ == '__main__':
    main()
