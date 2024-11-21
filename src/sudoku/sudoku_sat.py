from typing import List, cast
from pysat.formula import CNF  # type: ignore
from pysat.solvers import Glucose3  # type: ignore
from src.sudoku.sudoku import Sudoku
from src.sudoku.sudoku_iterator import SudokuIterator


def x(row: int, col: int, val: int, size: int) -> int:
    return row * size * size + col * size + val


def append_single_cell_constraints(iterator: SudokuIterator, cnf: CNF) -> None:
    n = len(iterator.grid)
    for row in iterator.iter_rows():
        for r, c in row:
            if iterator.grid[r][c] is not None:
                cnf.append([x(r, c, cast(int, iterator.grid[r][c]), n)])
            else:
                cnf.append([x(r, c, v, n) for v in range(1, n + 1)])
                for v1 in range(1, n + 1):
                    for v2 in range(v1 + 1, n + 1):
                        cnf.append([-x(r, c, v1, n), -x(r, c, v2, n)])


def append_row_column_constraints(cnf: CNF, size: int) -> None:
    for v in range(1, size + 1):
        for i in range(size):
            for j1 in range(size):
                for j2 in range(j1 + 1, size):
                    cnf.append([-x(i, j1, v, size), -x(i, j2, v, size)])
                    cnf.append([-x(j1, i, v, size), -x(j2, i, v, size)])


def append_subgrid_constraints(iterator: SudokuIterator, cnf: CNF) -> None:
    n = len(iterator.grid)
    for cell_group in iterator.iter_cells():
        for v in range(1, n + 1):
            for i, (r1, c1) in enumerate(cell_group):
                for r2, c2 in cell_group[i + 1 :]:
                    cnf.append([-x(r1, c1, v, n), -x(r2, c2, v, n)])


def encode_sat(sudoku: Sudoku) -> CNF:
    cnf: CNF = CNF()
    iterator = SudokuIterator(sudoku.grid)
    append_single_cell_constraints(iterator, cnf)
    append_row_column_constraints(cnf, len(sudoku.grid))
    append_subgrid_constraints(iterator, cnf)
    return cnf


def solve_sat(cnf: CNF, size: int) -> List[List[int]]:
    solver = Glucose3()
    solver.append_formula(cnf)
    solved_grid = [[0 for _ in range(size)] for _ in range(size)]
    if solver.solve():
        model = solver.get_model()
        for value in model:
            if value > 0:
                r = (value - 1) // (size * size)
                c = ((value - 1) // size) % size
                v = (value - 1) % size + 1
                solved_grid[r][c] = v
    return solved_grid
