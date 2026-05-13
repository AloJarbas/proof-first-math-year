#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "assets/proof-dependency-roadmap.svg"

WIDTH = 1440
HEIGHT = 920


def rect(x: float, y: float, w: float, h: float, fill: str, stroke: str = "#5e7fa3") -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="20" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'


def text(x: float, y: float, value: str, cls: str, anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{value}</text>'


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


def bullet(x: float, y: float, items: list[str]) -> list[str]:
    parts: list[str] = []
    for idx, item in enumerate(items):
        yy = y + idx * 22
        parts.append(text(x, yy, f'• {item}', 'small'))
    return parts


def node(svg: list[str], x: float, y: float, w: float, h: float, *, title_value: str, subtitle: str, bullets: list[str], fill: str) -> None:
    svg.append(rect(x, y, w, h, fill))
    svg.append(text(x + 22, y + 36, title_value, 'label'))
    svg.append(text(x + 22, y + 62, subtitle, 'small'))
    svg.extend(bullet(x + 24, y + 98, bullets))


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
        text(60, 96, 'A study map for deciding what unlocks what, and when a new stream should stay light instead of taking over.', 'subtitle'),
    ]

    node(svg, 80, 160, 310, 220,
         title_value='1. Proof foundations',
         subtitle='The non-negotiable bottleneck.',
         bullets=['logic, sets, functions', 'direct proof, contradiction, contrapositive', 'induction, definitions, clean notation', 'proof journal + error tags + weekly review'],
         fill='#1b2c3d')

    node(svg, 470, 160, 300, 220,
         title_value='2. Calculus spine',
         subtitle='Bring back computation without dropping proof work.',
         bullets=['keep proof sessions alive', 'use problem volume for fluency', 'do not let procedure replace writing', 'good secondary stream once proofs are holding'],
         fill='#183544')

    node(svg, 850, 160, 300, 220,
         title_value='3. Discrete reinforcement',
         subtitle='Formal structure that pays back into proof style.',
         bullets=['relations, counting, recurrence, induction', 'definition handling gets sharper', 'best added after proof habit is real', 'keep it lighter than the main spine'],
         fill='#19354a')

    node(svg, 470, 470, 300, 220,
         title_value='4. Linear algebra',
         subtitle='Preview early, then study honestly once the language is stable.',
         bullets=['start with systems, geometry, eigenideas', 'then move toward vector spaces and maps', 'works better after proof language stops feeling foreign', 'use a preview before a full heavy block'],
         fill='#25314b')

    node(svg, 850, 470, 300, 220,
         title_value='5. Real analysis',
         subtitle='The maturity core waiting on prepared ground.',
         bullets=['limits, continuity, approximation, convergence', 'forces clean hypothesis control', 'best after proof + algebra structure + calculus fluency', 'where mathematical precision starts to feel adult'],
         fill='#2a3050')

    node(svg, 1170, 470, 200, 220,
         title_value='6. Probability',
         subtitle='Stronger when it lands on a mature base.',
         bullets=['conditioning', 'random variables', 'expectation + variance', 'model before calculation'],
         fill='#2b2b4e')

    node(svg, 470, 760, 420, 110,
         title_value='7. Consolidation and integration',
         subtitle='Rewrite weak proofs, revisit hard topics without notes, and tie the year back to scientific work.',
         bullets=[],
         fill='#1f3b3d')

    node(svg, 80, 470, 310, 220,
         title_value='Operating rule',
         subtitle='Do not run four equal-intensity courses at once.',
         bullets=['proof stays primary until it stops fragmenting', 'new streams begin as controlled additions', 'review and rewrite count as real study', 'narrowing the load is a sign of design, not failure'],
         fill='#3a2f27')

    # Main arrows
    svg.extend([
        line(390, 270, 470, 270), arrowhead(470, 270, 'right'),
        line(770, 270, 850, 270), arrowhead(850, 270, 'right'),
        line(620, 380, 620, 470), arrowhead(620, 470, 'down'),
        line(1000, 380, 1000, 470), arrowhead(1000, 470, 'down'),
        line(770, 580, 850, 580), arrowhead(850, 580, 'right'),
        line(1270, 690, 1270, 760, dash='8 10'),
        arrowhead(1270, 760, 'down'),
        line(680, 690, 680, 760), arrowhead(680, 760, 'down'),
        line(1000, 690, 860, 815), arrowhead(860, 815, 'right'),
    ])

    # Side guidance arrows
    svg.extend([
        line(235, 380, 235, 470, stroke='#f97316'), arrowhead(235, 470, 'down', fill='#f97316'),
        line(390, 320, 470, 530, stroke='#f97316', dash='10 10'),
        arrowhead(470, 530, 'right', fill='#f97316'),
    ])

    svg.append(text(92, 720, 'Orange links mark load-management advice, not hard prerequisite edges.', 'tiny'))
    svg.append(text(92, 742, 'Blue links mark the main knowledge flow through the year.', 'tiny'))
    svg.append(text(60, 892, 'Generated from scripts/generate_dependency_roadmap.py', 'tiny'))
    svg.append('</svg>')

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(svg) + '\n')
    print(f'WROTE {OUT}')


if __name__ == '__main__':
    main()
