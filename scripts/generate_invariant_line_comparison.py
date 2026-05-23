#!/usr/bin/env python3
from __future__ import annotations

import csv
from html import escape
from pathlib import Path
import shutil
import subprocess
import tempfile

from invariant_line_examples import EXAMPLES, apply_matrix, example_rows, real_invariant_line_directions, sample_rays, transformed_unit_circle


REPO = Path(__file__).resolve().parents[1]
ASSET_SVG = REPO / "assets" / "invariant-line-comparison.svg"
ASSET_PNG = REPO / "assets" / "invariant-line-comparison.png"
ASSET_CSV = REPO / "assets" / "invariant-line-comparison.csv"

WIDTH = 1700
HEIGHT = 1380


def rect(x: float, y: float, w: float, h: float, fill: str, *, stroke: str = "#334155", rx: float = 24.0, stroke_width: float = 2.0) -> str:
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_width:.1f}"/>'


def line(x1: float, y1: float, x2: float, y2: float, stroke: str, *, width: float = 2.0, dash: str | None = None, opacity: float = 1.0) -> str:
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{width:.1f}" stroke-linecap="round" opacity="{opacity:.2f}"{dash_attr}/>'


def polyline(points: list[tuple[float, float]], stroke: str, *, width: float = 3.5, fill: str = "none", opacity: float = 1.0) -> str:
    encoded = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
    return f'<polyline points="{encoded}" fill="{fill}" stroke="{stroke}" stroke-width="{width:.1f}" stroke-linecap="round" stroke-linejoin="round" opacity="{opacity:.2f}"/>'


def text(x: float, y: float, value: str, cls: str, *, anchor: str = "start") -> str:
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{escape(value)}</text>'


def block(x: float, y: float, lines: list[str], cls: str, *, anchor: str = "start", line_step: int = 22) -> str:
    tspans = []
    for index, value in enumerate(lines):
        dy = 0 if index == 0 else line_step
        tspans.append(f'<tspan x="{x:.1f}" dy="{dy}">{escape(value)}</tspan>')
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{"".join(tspans)}</text>'


def wrap(text_value: str, width: int) -> list[str]:
    words = text_value.split()
    if not words:
        return [""]
    lines = [words[0]]
    for word in words[1:]:
        candidate = f"{lines[-1]} {word}"
        if len(candidate) <= width:
            lines[-1] = candidate
        else:
            lines.append(word)
    return lines


def arrowhead(x: float, y: float, dx: float, dy: float, color: str) -> str:
    length = (dx * dx + dy * dy) ** 0.5
    if length == 0.0:
        return ""
    ux = dx / length
    uy = dy / length
    left_x = x - 12 * ux + 6 * uy
    left_y = y - 12 * uy - 6 * ux
    right_x = x - 12 * ux - 6 * uy
    right_y = y - 12 * uy + 6 * ux
    points = f"{x:.1f},{y:.1f} {left_x:.1f},{left_y:.1f} {right_x:.1f},{right_y:.1f}"
    return f'<polygon points="{points}" fill="{color}"/>'


def map_point(x: float, y: float, *, left: float, top: float, size: float, scale: float) -> tuple[float, float]:
    center_x = left + size / 2.0
    center_y = top + size / 2.0
    return center_x + x * scale, center_y - y * scale


def export_png(svg_path: Path, png_path: Path) -> None:
    brave_candidates = [
        Path("/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"),
        Path(shutil.which("brave-browser") or ""),
    ]
    browser = next((candidate for candidate in brave_candidates if candidate and candidate.exists()), None)
    if browser is None:
        raise FileNotFoundError("Brave Browser is required for PNG export in this repo")
    with tempfile.TemporaryDirectory() as tmpdir:
        wrapper = Path(tmpdir) / "wrapper.html"
        wrapper.write_text(
            "<html><head><style>"
            f"html,body{{margin:0;padding:0;width:{WIDTH}px;height:{HEIGHT}px;overflow:hidden;background:#071018;}}"
            f"img{{display:block;width:{WIDTH}px;height:{HEIGHT}px;}}"
            "</style></head><body>"
            f"<img src='{svg_path.resolve().as_uri()}'/>"
            "</body></html>"
        )
        command = [
            str(browser),
            "--headless",
            "--disable-gpu",
            "--hide-scrollbars",
            "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=1000",
            f"--screenshot={png_path.resolve()}",
            f"--window-size={WIDTH},{HEIGHT}",
            wrapper.resolve().as_uri(),
        ]
        try:
            subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
        except subprocess.TimeoutExpired:
            if not png_path.exists():
                raise
    sips = shutil.which("sips")
    if sips is not None:
        subprocess.run([sips, "--setProperty", "dpiWidth", "300", "--setProperty", "dpiHeight", "300", str(png_path)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def write_csv() -> None:
    ASSET_CSV.parent.mkdir(parents=True, exist_ok=True)
    rows = example_rows()
    with ASSET_CSV.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> None:
    panel_width = 500.0
    plot_size = 300.0
    panel_lefts = [70.0, 600.0, 1130.0]
    panel_top = 220.0
    scale = 76.0

    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{HEIGHT}" viewBox="0 0 {WIDTH} {HEIGHT}">',
        '<defs>',
        '  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">',
        '    <stop offset="0%" stop-color="#071018"/>',
        '    <stop offset="100%" stop-color="#102033"/>',
        '  </linearGradient>',
        '  <style>',
        '    .title { font: 700 38px Helvetica, Arial, sans-serif; fill: #e5eef7; }',
        '    .subtitle { font: 500 19px Helvetica, Arial, sans-serif; fill: #b4c3d4; }',
        '    .label { font: 700 22px Helvetica, Arial, sans-serif; fill: #dde7f1; }',
        '    .body { font: 500 16px Helvetica, Arial, sans-serif; fill: #c8d4e0; }',
        '    .small { font: 500 14px Helvetica, Arial, sans-serif; fill: #9fb2c7; }',
        '    .tiny { font: 500 13px Helvetica, Arial, sans-serif; fill: #92a5ba; }',
        '  </style>',
        '</defs>',
        f'<rect width="{WIDTH}" height="{HEIGHT}" fill="url(#bg)"/>',
        text(62, 66, 'Invariant lines, real rotation, and defect', 'title'),
        block(62, 100, [
            'Three 2x2 maps can all preserve the plane while telling different diagonalization stories.',
            'The point is to keep “no real eigenline” separate from “one eigenline is not enough.”',
        ], 'subtitle', line_step=24),
    ]

    for left, example in zip(panel_lefts, EXAMPLES):
        svg.append(rect(left, panel_top, panel_width, 600, '#122033', stroke='#32485f', rx=28.0))
        svg.append(text(left + 24, panel_top + 38, example.title, 'label'))
        svg.append(block(left + 24, panel_top + 68, wrap(example.matrix_label, 28) + [example.preserved_space], 'small', line_step=20))
        plot_left = left + 100
        plot_top = panel_top + 110
        svg.append(rect(plot_left, plot_top, plot_size, plot_size, '#0b1524', stroke='#334155', rx=18.0, stroke_width=1.5))

        for frac in (0.25, 0.5, 0.75):
            x = plot_left + frac * plot_size
            y = plot_top + frac * plot_size
            svg.append(line(x, plot_top + 10, x, plot_top + plot_size - 10, '#223246', width=1.0, opacity=0.85))
            svg.append(line(plot_left + 10, y, plot_left + plot_size - 10, y, '#223246', width=1.0, opacity=0.85))
        cx = plot_left + plot_size / 2.0
        cy = plot_top + plot_size / 2.0
        svg.append(line(plot_left + 14, cy, plot_left + plot_size - 14, cy, '#4b647c', width=1.4))
        svg.append(line(cx, plot_top + 14, cx, plot_top + plot_size - 14, '#4b647c', width=1.4))

        unit_circle = [map_point(x, y, left=plot_left, top=plot_top, size=plot_size, scale=scale) for x, y in transformed_unit_circle(((1.0, 0.0), (0.0, 1.0)))]
        image_circle = [map_point(x, y, left=plot_left, top=plot_top, size=plot_size, scale=scale) for x, y in transformed_unit_circle(example.matrix)]
        svg.append(polyline(unit_circle, '#6b7280', width=2.0, opacity=0.75))
        svg.append(polyline(image_circle, example.color, width=4.2, opacity=0.95))

        for direction in real_invariant_line_directions(example.matrix):
            x1, y1 = map_point(-1.9 * direction[0], -1.9 * direction[1], left=plot_left, top=plot_top, size=plot_size, scale=scale)
            x2, y2 = map_point(1.9 * direction[0], 1.9 * direction[1], left=plot_left, top=plot_top, size=plot_size, scale=scale)
            svg.append(line(x1, y1, x2, y2, '#facc15', width=2.5, dash='10 10', opacity=0.9))

        for ray in sample_rays():
            x0, y0 = map_point(0.0, 0.0, left=plot_left, top=plot_top, size=plot_size, scale=scale)
            x1, y1 = map_point(ray[0], ray[1], left=plot_left, top=plot_top, size=plot_size, scale=scale)
            tx, ty = apply_matrix(example.matrix, ray)
            x2, y2 = map_point(tx, ty, left=plot_left, top=plot_top, size=plot_size, scale=scale)
            svg.append(line(x0, y0, x1, y1, '#61758a', width=1.3, opacity=0.7))
            svg.append(line(x0, y0, x2, y2, example.color, width=2.0, opacity=0.9))
            svg.append(arrowhead(x2, y2, x2 - x0, y2 - y0, example.color))

        svg.append(block(left + 24, panel_top + 470, wrap(example.line_story, 34), 'body', line_step=22))
        svg.append(block(left + 24, panel_top + 570, wrap(example.failure_story, 36), 'small', line_step=20))

    bottom_top = 860.0
    bottom_height = 390.0
    bottom_lefts = [70.0, 600.0, 1130.0]
    bottom_titles = ['How to read the three cases', 'What the comparison is protecting', 'Best next move']
    bottom_bullets = [
        [
            'Diagonal case: two real eigenlines span the plane.',
            'Rotation: the plane survives, but no real line does.',
            'Jordan block: one eigenline survives, but the second lane never closes.',
        ],
        [
            'Do not treat every failed diagonalization as one story.',
            'Rotation fails because there is no real invariant line.',
            'Jordan fails because one surviving line is not enough.',
        ],
        [
            'Use the note and notebook with this card, then write one structural sentence per case.',
            'Ask what the map preserves before reaching for a determinant.',
            'If this lands, the next move is worked proof sets, not more vocabulary.',
        ],
    ]
    for left, title_value, bullets in zip(bottom_lefts, bottom_titles, bottom_bullets):
        svg.append(rect(left, bottom_top, panel_width, bottom_height, '#122033', stroke='#32485f', rx=24.0))
        svg.append(text(left + 24, bottom_top + 38, title_value, 'label'))
        y = bottom_top + 74
        for bullet in bullets:
            svg.append(block(left + 24, y, wrap(f'• {bullet}', 36), 'body', line_step=22))
            y += 96

    svg.append(text(70, 1348, 'Generated from scripts/generate_invariant_line_comparison.py and scripts/invariant_line_examples.py', 'tiny'))
    svg.append('</svg>')

    ASSET_SVG.parent.mkdir(parents=True, exist_ok=True)
    ASSET_SVG.write_text('\n'.join(svg) + '\n')
    write_csv()
    export_png(ASSET_SVG, ASSET_PNG)
    print(f'WROTE {ASSET_SVG}, {ASSET_PNG}, and {ASSET_CSV}')


if __name__ == '__main__':
    main()
