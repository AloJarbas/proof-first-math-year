#!/usr/bin/env python3
from __future__ import annotations

from html import escape
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "assets/proof-dependency-roadmap.svg"

WIDTH = 1600
HEIGHT = 1060


def rect(x: float, y: float, w: float, h: float, fill: str, stroke: str = "#5e7fa3") -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def text(x: float, y: float, value: str, cls: str, anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>'


def text_block(x: float, y: float, lines: list[str], cls: str, *, anchor: str = "start", line_step: int = 22) -> str:
    tspans = []
    for idx, line in enumerate(lines):
        dy = 0 if idx == 0 else line_step
        tspans.append(f'<tspan x="{x:.1f}" dy="{dy}">{escape(line)}</tspan>')
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{"".join(tspans)}</text>'


def line(x1: float, y1: float, x2: float, y2: float, stroke: str = "#7dd3fc", width: float = 3.0, dash: str | None = None) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width}" stroke-linecap="round"{dash_attr}/>'


def arrowhead(x: float, y: float, direction: str, fill: str = "#7dd3fc") -> str:
    if direction == "right":
        points = [(x, y), (x - 12, y - 8), (x - 12, y + 8)]
    elif direction == "down":
        points = [(x, y), (x - 8, y - 12), (x + 8, y - 12)]
    else:
        raise ValueError(direction)
    point_text = " ".join(f"{px:.1f},{py:.1f}" for px, py in points)
    return f'<polygon points="{point_text}" fill="{fill}"/>'


def node(svg: list[str], x: float, y: float, w: float, h: float, *, title_lines: list[str], subtitle_lines: list[str], bullets: list[str], fill: str) -> None:
    svg.append(rect(x, y, w, h, fill))
    svg.append(text_block(x + 22, y + 36, title_lines, 'label', line_step=22))
    subtitle_y = y + 68 + max(0, len(title_lines) - 1) * 22
    svg.append(text_block(x + 22, subtitle_y, subtitle_lines, 'small', line_step=20))
    bullet_y = subtitle_y + 38 + max(0, len(subtitle_lines) - 1) * 20
    for idx, item in enumerate(bullets):
        svg.append(text(x + 24, bullet_y + idx * 24, f'• {item}', 'small'))


def main() -> None:
    svg: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<defs>',
        '  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '    <stop offset="0%" stop-color="#071018"/>',
        '    <stop offset="100%" stop-color="#0f1d2b"/>',
        '  </linearGradient>',
        '  <style>',
        '    .title { font: 700 36px Helvetica, Arial, sans-serif; fill: #e6edf3; }',
        '    .subtitle { font: 500 18px Helvetica, Arial, sans-serif; fill: #9fb3c8; }',
        '    .label { font: 700 22px Helvetica, Arial, sans-serif; fill: #dce7f3; }',
        '    .small { font: 500 15px Helvetica, Arial, sans-serif; fill: #c6d3e1; }',
        '    .tiny { font: 500 13px Helvetica, Arial, sans-serif; fill: #90a4ba; }',
        '  </style>',
        '</defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>',
        text(60, 64, 'Proof-first dependency roadmap', 'title'),
        text_block(60, 96, [
            'A study map for deciding what unlocks what, and when a new stream should stay light',
            'instead of taking over.'
        ], 'subtitle', line_step=22),
    ]

    node(svg, 90, 180, 350, 250,
         title_lines=['1. Proof foundations'],
         subtitle_lines=['The non-negotiable bottleneck.'],
         bullets=['logic, sets, functions', 'direct proof, contradiction, contrapositive', 'induction, definitions, clean notation', 'proof journal + error tags + weekly review'],
         fill='#1b2c3d')

    node(svg, 500, 180, 350, 250,
         title_lines=['2. Calculus spine'],
         subtitle_lines=['Bring back computation without', 'dropping proof work.'],
         bullets=['keep proof sessions alive', 'use problem volume for fluency', 'do not let procedure replace writing', 'good secondary stream once proofs are holding'],
         fill='#183544')

    node(svg, 910, 180, 350, 250,
         title_lines=['3. Discrete reinforcement'],
         subtitle_lines=['Formal structure that pays back', 'into proof style.'],
         bullets=['relations, counting, recurrence, induction', 'definition handling gets sharper', 'best added after proof habit is real', 'keep it lighter than the main spine'],
         fill='#19354a')

    node(svg, 90, 500, 350, 250,
         title_lines=['Operating rule'],
         subtitle_lines=['Do not run four equal-intensity', 'courses at once.'],
         bullets=['proof stays primary until it stops fragmenting', 'new streams begin as controlled additions', 'review and rewrite count as real study', 'narrowing the load is design, not failure'],
         fill='#3a2f27')

    node(svg, 500, 500, 350, 250,
         title_lines=['4. Linear algebra'],
         subtitle_lines=['Preview early, then study honestly', 'once the language is stable.'],
         bullets=['start with systems, geometry, eigenideas', 'then move toward vector spaces and maps', 'works better after proof language settles', 'use a preview before a full heavy block'],
         fill='#25314b')

    node(svg, 910, 500, 350, 250,
         title_lines=['5. Real analysis'],
         subtitle_lines=['The maturity core waiting on', 'prepared ground.'],
         bullets=['limits, continuity, approximation, convergence', 'forces clean hypothesis control', 'best after proof + algebra + calculus fluency', 'where mathematical precision starts to feel adult'],
         fill='#2a3050')

    node(svg, 1300, 500, 220, 250,
         title_lines=['6. Probability'],
         subtitle_lines=['Stronger when it lands on a', 'mature base.'],
         bullets=['conditioning', 'random variables', 'expectation + variance', 'model before calculation'],
         fill='#2b2b4e')

    node(svg, 500, 840, 620, 140,
         title_lines=['7. Consolidation and integration'],
         subtitle_lines=['Rewrite weak proofs, revisit hard topics without notes,', 'and tie the year back to scientific work.'],
         bullets=[],
         fill='#1f3b3d')

    svg.extend([
        line(440, 305, 500, 305), arrowhead(500, 305, 'right'),
        line(850, 305, 910, 305), arrowhead(910, 305, 'right'),
        line(675, 430, 675, 500), arrowhead(675, 500, 'down'),
        line(1085, 430, 1085, 500), arrowhead(1085, 500, 'down'),
        line(850, 625, 910, 625), arrowhead(910, 625, 'right'),
        line(1410, 750, 1410, 840, dash='8 10'), arrowhead(1410, 840, 'down'),
        line(675, 750, 675, 840), arrowhead(675, 840, 'down'),
        line(1085, 750, 1000, 840), arrowhead(1000, 840, 'right'),
    ])

    svg.extend([
        line(265, 430, 265, 500, stroke='#f97316'), arrowhead(265, 500, 'down', fill='#f97316'),
        line(440, 355, 500, 560, stroke='#f97316', dash='10 10'), arrowhead(500, 560, 'right', fill='#f97316'),
    ])

    svg.append(text(92, 936, 'Orange links mark load-management advice, not hard prerequisite edges.', 'tiny'))
    svg.append(text(92, 958, 'Blue links mark the main knowledge flow through the year.', 'tiny'))
    svg.append(text(60, 1018, 'Generated from scripts/generate_dependency_roadmap.py', 'tiny'))
    svg.append('</svg>')

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(svg) + '\n')
    print(f'WROTE {OUT}')


if __name__ == '__main__':
    main()
