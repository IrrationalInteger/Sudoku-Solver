from typing import Tuple
from cpmpy import Model, intvar, AllDifferent  # type: ignore
from cpmpy.expressions.variables import _IntVarImpl  # type: ignore
from sudoku.sudoku import Sudoku


def append_single_cell_constraints(
    sudoku: Sudoku, model: Model, x: list[list[_IntVarImpl]]
) -> None:
    for r in range(sudoku.n):
        for c in range(sudoku.n):
            if sudoku.grid[r][c] is not None:
                model += [x[r][c] == sudoku.grid[r][c]]


def append_row_column_constraints(
    sudoku: Sudoku, model: Model, x: list[list[_IntVarImpl]]
) -> None:
    for r in range(sudoku.n):
        model += [AllDifferent(x[r])]

    for c in range(sudoku.n):
        model += [AllDifferent([x[r][c] for r in range(sudoku.n)])]


def append_subgrid_constraints(
    sudoku: Sudoku, model: Model, x: list[list[_IntVarImpl]]
) -> None:
    subgrid_size: int = int(sudoku.n**0.5)
    for br in range(subgrid_size):
        for bc in range(subgrid_size):
            cells = [
                x[br * subgrid_size + r][bc * subgrid_size + c]
                for r in range(subgrid_size)
                for c in range(subgrid_size)
            ]
            model += [AllDifferent(cells)]


def encode_const(sudoku: Sudoku) -> Tuple[Model, list[list[_IntVarImpl]]]:
    x = [
        [intvar(1, sudoku.n) for _ in range(sudoku.n)] for _ in range(sudoku.n)
    ]

    model = Model()

    append_single_cell_constraints(sudoku, model, x)
    append_row_column_constraints(sudoku, model, x)
    append_subgrid_constraints(sudoku, model, x)

    return model, x


def solve_const(
    sudoku: Sudoku, model: Model, x: list[list[_IntVarImpl]]
) -> list[list[int]]:
    solved_grid = [[0] * sudoku.n for _ in range(sudoku.n)]
    if model.solve():
        solved_grid = [
            [x[r][c].value() for c in range(sudoku.n)] for r in range(sudoku.n)
        ]
    return solved_grid
