from __future__ import annotations

from dataclasses import dataclass
import math
from typing import Iterable


Vector = tuple[float, float]
Matrix = tuple[tuple[float, float], tuple[float, float]]


@dataclass(frozen=True)
class LinearMapExample:
    key: str
    title: str
    matrix: Matrix
    color: str
    preserved_space: str
    line_story: str
    failure_story: str

    @property
    def matrix_label(self) -> str:
        (a, b), (c, d) = self.matrix
        return f"[[{a:g}, {b:g}], [{c:g}, {d:g}]]"


EXAMPLES: tuple[LinearMapExample, ...] = (
    LinearMapExample(
        key="diagonal",
        title="Diagonal scaling",
        matrix=((3.0, 0.0), (0.0, 0.5)),
        color="#38bdf8",
        preserved_space="two invariant lines",
        line_story="The x-axis and y-axis stay closed, so the plane splits into two independent lanes.",
        failure_story="No failure here. This is the clean diagonalizable case.",
    ),
    LinearMapExample(
        key="rotation",
        title="Real rotation",
        matrix=((0.5, -0.8660254037844386), (0.8660254037844386, 0.5)),
        color="#f97316",
        preserved_space="the whole plane only",
        line_story="Every nonzero vector gets turned off its own line, so there is no nontrivial real invariant line.",
        failure_story="Failure type: no real eigenline at all.",
    ),
    LinearMapExample(
        key="jordan",
        title="Defective Jordan block",
        matrix=((2.0, 1.0), (0.0, 2.0)),
        color="#a78bfa",
        preserved_space="one invariant line",
        line_story="The x-axis stays closed, but there is not a second independent eigenline to finish the split.",
        failure_story="Failure type: one eigenline is not enough to span the plane.",
    ),
)


def apply_matrix(matrix: Matrix, vector: Vector) -> Vector:
    (a, b), (c, d) = matrix
    x, y = vector
    return (a * x + b * y, c * x + d * y)


def trace(matrix: Matrix) -> float:
    return matrix[0][0] + matrix[1][1]


def determinant(matrix: Matrix) -> float:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def discriminant(matrix: Matrix) -> float:
    return trace(matrix) ** 2 - 4.0 * determinant(matrix)


def eigenvalues(matrix: Matrix) -> tuple[float, ...]:
    disc = discriminant(matrix)
    if disc < 0.0:
        return ()
    root = math.sqrt(max(0.0, disc))
    tr = trace(matrix)
    return ((tr - root) / 2.0, (tr + root) / 2.0)


def normalize_line_direction(vector: Vector) -> Vector:
    x, y = vector
    norm = math.hypot(x, y)
    if norm == 0.0:
        raise ValueError("zero vector does not define a line")
    x /= norm
    y /= norm
    if x < 0 or (abs(x) < 1e-12 and y < 0):
        x *= -1.0
        y *= -1.0
    return (x, y)


def direction_for_eigenvalue(matrix: Matrix, eigenvalue: float) -> Vector | None:
    (a, b), (c, d) = matrix
    if abs(b) > 1e-12 or abs(a - eigenvalue) > 1e-12:
        return normalize_line_direction((b, eigenvalue - a))
    if abs(c) > 1e-12 or abs(d - eigenvalue) > 1e-12:
        return normalize_line_direction((eigenvalue - d, c))
    return None


def real_invariant_line_directions(matrix: Matrix) -> tuple[Vector, ...]:
    directions: list[Vector] = []
    for eigenvalue in eigenvalues(matrix):
        direction = direction_for_eigenvalue(matrix, eigenvalue)
        if direction is None:
            continue
        if not any(abs(direction[0] - seen[0]) < 1e-9 and abs(direction[1] - seen[1]) < 1e-9 for seen in directions):
            directions.append(direction)
    return tuple(directions)


def real_invariant_line_count(matrix: Matrix) -> int:
    return len(real_invariant_line_directions(matrix))


def sample_unit_circle(count: int = 240) -> tuple[Vector, ...]:
    return tuple((math.cos(2.0 * math.pi * index / count), math.sin(2.0 * math.pi * index / count)) for index in range(count))


def transformed_unit_circle(matrix: Matrix, *, count: int = 240) -> tuple[Vector, ...]:
    return tuple(apply_matrix(matrix, point) for point in sample_unit_circle(count))


def sample_rays() -> tuple[Vector, ...]:
    base_angles = (-0.9, -0.3, 0.45, 1.2)
    return tuple((math.cos(angle), math.sin(angle)) for angle in base_angles)


def example_rows(examples: Iterable[LinearMapExample] = EXAMPLES) -> tuple[dict[str, str], ...]:
    rows = []
    for example in examples:
        rows.append(
            {
                "key": example.key,
                "title": example.title,
                "matrix": example.matrix_label,
                "trace": f"{trace(example.matrix):.6f}",
                "determinant": f"{determinant(example.matrix):.6f}",
                "discriminant": f"{discriminant(example.matrix):.6f}",
                "real_invariant_line_count": str(real_invariant_line_count(example.matrix)),
                "preserved_space": example.preserved_space,
                "failure_story": example.failure_story,
            }
        )
    return tuple(rows)
