from typing import List, cast
from pysat.solvers import Glucose3  # type: ignore
from pysat.formula import CNF  # type: ignore

from src.sudoku.sudoku import Sudoku


def x(row: int, col: int, val: int) -> int:
    return row * 81 + col * 9 + val


def append_single_cell_constraints(
    grid: List[List[int | None]], cnf: CNF
) -> None:
    for r in range(9):
        for c in range(9):
            if grid[r][c] is not None:
                cnf.append([x(r, c, cast(int, (grid[r][c])))])
            else:
                cnf.append([x(r, c, v) for v in range(1, 10)])
                for v1 in range(1, 10):
                    for v2 in range(v1 + 1, 10):
                        cnf.append([-x(r, c, v1), -x(r, c, v2)])


def append_row_column_constraints(cnf: CNF) -> None:
    for r in range(9):
        for v in range(1, 10):
            for c1 in range(9):
                for c2 in range(c1 + 1, 9):
                    cnf.append([-x(r, c1, v), -x(r, c2, v)])

    for c in range(9):
        for v in range(1, 10):
            for r1 in range(9):
                for r2 in range(r1 + 1, 9):
                    cnf.append([-x(r1, c, v), -x(r2, c, v)])


def append_subgrid_constraints(cnf: CNF) -> None:
    for block_row in range(3):
        for block_col in range(3):
            for v in range(1, 10):
                cells = [
                    (block_row * 3 + r, block_col * 3 + c)
                    for r in range(3)
                    for c in range(3)
                ]
                for i, (r1, c1) in enumerate(cells):
                    for r2, c2 in cells[i + 1 :]:
                        cnf.append([-x(r1, c1, v), -x(r2, c2, v)])


def encode_sat(sudoku: Sudoku) -> CNF:
    cnf: CNF = CNF()

    append_single_cell_constraints(sudoku.grid, cnf)
    append_row_column_constraints(cnf)
    append_subgrid_constraints(cnf)

    return cnf


def solve_sat(cnf: CNF) -> List[List[int]] | None:
    solver = Glucose3()
    solver.append_formula(cnf)
    if solver.solve():
        model = solver.get_model()
        solved_grid = [[0 for _ in range(9)] for _ in range(9)]
        for value in model:
            if value > 0:
                r = (value - 1) // 81
                c = ((value - 1) // 9) % 9
                v = (value - 1) % 9 + 1
                solved_grid[r][c] = v
        return solved_grid
    else:
        print("This Sudoku is unsolvable.")
        return None
