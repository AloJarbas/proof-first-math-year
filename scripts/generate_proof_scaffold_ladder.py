#!/usr/bin/env python3
from __future__ import annotations

import csv
from html import escape
from pathlib import Path
import shutil
import subprocess
import tempfile

from proof_scaffold_ladder import PROBLEMS, STEP_LABELS, ordered_problems, problem_rows

REPO = Path(__file__).resolve().parents[1]
ASSET_SVG = REPO / 'assets' / 'proof-scaffold-ladder.svg'
ASSET_PNG = REPO / 'assets' / 'proof-scaffold-ladder.png'
ASSET_CSV = REPO / 'assets' / 'proof-scaffold-ladder.csv'

WIDTH = 1780
HEIGHT = 1600
STAGE_COLORS = {
    'proof fluency': '#38bdf8',
    'linear algebra bridge': '#a78bfa',
    'geometry follow-up': '#f97316',
}
STEP_ORDER = tuple(STEP_LABELS)
STEP_SHORT_LABELS = {
    'arbitrary-object': 'arbitrary\nobject',
    'witness-or-coefficients': 'witness\nor coeffs',
    'closure-or-split': 'closure\nsplit',
    'algebra-or-components': 'algebra\ncleanup',
    'contradiction-pivot': 'contradiction\npivot',
    'close-the-claim': 'close\nclaim',
}


def rect(x: float, y: float, w: float, h: float, fill: str, *, stroke: str = '#334155', rx: float = 22.0, stroke_width: float = 2.0) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'


def line(x1: float, y1: float, x2: float, y2: float, stroke: str, *, width: float = 2.0, dash: str | None = None, opacity: float = 1.0) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width:.1f}" stroke-linecap="round" opacity="{opacity:.2f}"{dash_attr}/>'


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
    rows = problem_rows()
    ASSET_CSV.parent.mkdir(parents=True, exist_ok=True)
    with ASSET_CSV.open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator='\n')
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    problems = ordered_problems()
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
        '    .micro { font: 600 12px Helvetica, Arial, sans-serif; fill: #dbeafe; }',
        '  </style>',
        '</defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>',
        text(62, 68, 'Proof scaffold ladder: fill the missing structural move', 'title'),
        block(62, 104, [
            'This packet is for the moment when a learner can follow a proof but still drops one crucial move.',
            'The ladder stays compact: six problems, one generated card, one notebook, and answer-check prompts that force the missing structure to be said out loud.',
        ], 'subtitle', line_step=24),
    ]

    left = 60.0
    top = 170.0
    main_w = 1080.0
    main_h = 980.0
    svg.append(rect(left, top, main_w, main_h, '#122033', stroke='#32485f', rx=28.0))
    svg.append(text(left + 24, top + 38, 'Six problems, six common missing moves', 'label'))
    svg.append(block(left + 24, top + 66, wrap('Rows get harder in a very specific way: more structure is omitted, so the learner has to name more of the proof instead of only recognizing it after the fact.', 86), 'small', line_step=20))

    title_x = left + 30
    grid_x = left + 480
    diff_x = left + 1020
    row_top = top + 138
    row_h = 126.0
    cell_w = 84.0

    svg.append(text(title_x, row_top - 22, 'problem', 'small'))
    for index, step in enumerate(STEP_ORDER):
        x = grid_x + index * cell_w
        svg.append(rect(x, row_top - 64, cell_w - 8, 54, '#0d1726', stroke='#2b3b52', rx=12.0, stroke_width=1.2))
        svg.append(block(x + (cell_w - 8) / 2.0, row_top - 44, STEP_SHORT_LABELS[step].split('\n'), 'tiny', anchor='middle', line_step=15))
    svg.append(text(diff_x, row_top - 22, 'level', 'small', anchor='middle'))

    for row_index, problem in enumerate(problems):
        y = row_top + row_index * row_h
        stage_color = STAGE_COLORS[problem.stage]
        svg.append(rect(title_x - 10, y, main_w - 70, row_h - 14, '#0d1726', stroke='#27384d', rx=18.0, stroke_width=1.5))
        svg.append(rect(title_x + 2, y + 12, 138, 28, stage_color, stroke=stage_color, rx=14.0, stroke_width=0.0))
        svg.append(text(title_x + 71, y + 31, problem.stage.upper(), 'micro', anchor='middle', fill='#04111f'))
        svg.append(text(title_x, y + 66, problem.title, 'label'))
        svg.append(block(title_x, y + 94, wrap(f'{problem.method} · {problem.topic} · {problem.structural_sentence}', 50), 'small', line_step=19))
        for index, step in enumerate(STEP_ORDER):
            x = grid_x + index * cell_w
            active = step in problem.omitted_steps
            fill = stage_color if active else '#122033'
            stroke = stage_color if active else '#334155'
            svg.append(rect(x, y + 24, cell_w - 8, 62, fill, stroke=stroke, rx=16.0, stroke_width=1.6))
            if active:
                svg.append(text(x + (cell_w - 8) / 2.0, y + 61, 'missing', 'body', anchor='middle', fill='#04111f'))
            else:
                svg.append(text(x + (cell_w - 8) / 2.0, y + 61, 'given', 'small', anchor='middle', fill='#7f93a8'))
        svg.append(rect(diff_x - 34, y + 22, 68, 66, '#10233a', stroke=stage_color, rx=18.0, stroke_width=2.0))
        svg.append(text(diff_x, y + 64, str(problem.difficulty), 'title', anchor='middle'))

    right_left = 1170.0
    right_w = 550.0
    right_top = 170.0
    svg.append(rect(right_left, right_top, right_w, 446, '#122033', stroke='#32485f', rx=28.0))
    svg.append(text(right_left + 24, right_top + 38, 'What the six columns mean', 'label'))
    legend_y = right_top + 90
    for step in STEP_ORDER:
        svg.append(rect(right_left + 24, legend_y - 18, 16, 16, '#dbeafe', stroke='#dbeafe', rx=4.0, stroke_width=0.0))
        svg.append(block(right_left + 52, legend_y - 2, wrap(STEP_LABELS[step], 36), 'body', line_step=20))
        legend_y += 62

    card_top = 650.0
    card_w = 550.0
    card_h = 484.0
    svg.append(rect(right_left, card_top, card_w, card_h, '#122033', stroke='#32485f', rx=28.0))
    svg.append(text(right_left + 24, card_top + 38, 'How to use the ladder', 'label'))
    bullet_y = card_top + 80
    bullets = [
        'Do one row at a time. Fill only the highlighted moves before checking anything else.',
        'After each proof, read the answer-check prompts and write one sentence fixing the first place your structure went soft.',
        'If a row collapses, drop one stage but keep the same answer-check habit. The point is to repair proof form, not to farm harder topics for damage.',
        'When a row becomes routine, move to the next row without changing the writing standard: arbitrary object, witness, closure split, contradiction pivot, close the claim.',
    ]
    for bullet in bullets:
        svg.append(block(right_left + 24, bullet_y, wrap(f'• {bullet}', 54), 'body', line_step=23))
        bullet_y += 102

    bottom_top = 1180.0
    bottom_w = 520.0
    gap = 30.0
    titles = ['What this packet protects', 'Companion notebook', 'Adversarial check']
    bodies = [
        [
            'It keeps “I know the theorem” separate from “I can actually write the proof skeleton.”',
            'That matters most at the linear-algebra handoff, where learners often know the right words but still skip the zero-vector or witness step.',
        ],
        [
            'Open notebooks/proof_scaffold_ladder.ipynb after reading the note.',
            'The notebook keeps the same six problems but adds starter lines, answer-check prompts, and short reflection questions so the learner has to say the missing move explicitly.',
        ],
        [
            'A learner can get the final theorem right while never naming the structural move that made it work.',
            'This packet is only useful if it forces that move back into the writing. If the learner still writes “clearly” or “obvious” where the missing move belongs, the ladder did not land yet.',
        ],
    ]
    for idx, (title_value, body_lines) in enumerate(zip(titles, bodies)):
        x = 60.0 + idx * (bottom_w + gap)
        svg.append(rect(x, bottom_top, bottom_w, 300, '#122033', stroke='#32485f', rx=24.0))
        svg.append(text(x + 24, bottom_top + 38, title_value, 'label'))
        y = bottom_top + 78
        for paragraph in body_lines:
            svg.append(block(x + 24, y, wrap(paragraph, 50), 'body', line_step=23))
            y += 106

    svg.append(text(62, 1560, 'Generated from scripts/generate_proof_scaffold_ladder.py and scripts/proof_scaffold_ladder.py', 'tiny'))
    svg.append('</svg>')

    ASSET_SVG.parent.mkdir(parents=True, exist_ok=True)
    ASSET_SVG.write_text('\n'.join(svg) + '\n')
    write_csv()
    export_png(ASSET_SVG, ASSET_PNG)
    print(f'WROTE {ASSET_SVG}, {ASSET_PNG}, and {ASSET_CSV}')


if __name__ == '__main__':
    main()
