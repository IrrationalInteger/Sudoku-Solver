from itertools import combinations
from typing import List, cast
from pysat.formula import CNF  # type: ignore
from pysat.solvers import Glucose3  # type: ignore
from sudoku.sudoku import Sudoku
from sudoku.sudoku_iterator import SudokuIterator


def x(row: int, col: int, val: int, size: int) -> int:
    return row * size * size + col * size + val


def at_most_one(variables: List[int], cnf: CNF) -> None:
    for v1, v2 in combinations(variables, 2):
        cnf.append([-v1, -v2])


def append_single_cell_constraints(iterator: SudokuIterator, cnf: CNF) -> None:
    n = len(iterator.grid)
    for row in iterator.iter_rows():
        for r, c in row:
            if iterator.grid[r][c] is not None:
                cnf.append([x(r, c, cast(int, iterator.grid[r][c]), n)])
            else:
                cnf.append([x(r, c, v, n) for v in range(1, n + 1)])
                variables = [x(r, c, v, n) for v in range(1, n + 1)]
                at_most_one(variables, cnf)


def append_row_column_constraints(iterator: SudokuIterator, cnf: CNF) -> None:
    size = len(iterator.grid)
    for row in iterator.iter_rows():
        for v in range(1, size + 1):
            variables = [x(r, c, v, size) for r, c in row]
            at_most_one(variables, cnf)

    for col in iterator.iter_cols():
        for v in range(1, size + 1):
            variables = [x(r, c, v, size) for r, c in col]
            at_most_one(variables, cnf)


def append_subgrid_constraints(iterator: SudokuIterator, cnf: CNF) -> None:
    n = len(iterator.grid)
    for cell_group in iterator.iter_cells():
        for v in range(1, n + 1):
            variables = [x(r, c, v, n) for r, c in cell_group]
            at_most_one(variables, cnf)


def encode_sat(sudoku: Sudoku) -> CNF:
    cnf: CNF = CNF()
    iterator = SudokuIterator(sudoku.grid)
    append_single_cell_constraints(iterator, cnf)
    append_row_column_constraints(iterator, cnf)
    append_subgrid_constraints(iterator, cnf)
    return cnf


def solve_sat(cnf: CNF, size: int) -> list[list[int]]:
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
