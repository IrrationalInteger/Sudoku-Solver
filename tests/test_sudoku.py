from typing import List, Optional
from pysat.formula import CNF  # type: ignore
from src.sudoku.sudoku import Sudoku
from src.sudoku.sudoku_constraint import encode_const, solve_const
from src.sudoku.sudoku_integer import encode_int, solve_int
from src.sudoku.sudoku_sat import encode_sat, solve_sat
from config import TEST_DATA


def test_read_sudoku() -> None:
    s: Sudoku = Sudoku.read_sudoku(TEST_DATA / "test_input.txt")
    assert s.grid != []
    assert len(s.grid) == 9
    assert len(s.grid[0]) == 9


def test_write_sudoku() -> None:
    grid: List[List[Optional[int]]] = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, None],
    ]
    s: Sudoku = Sudoku(grid)
    s.write_sudoku(TEST_DATA / "test_output.txt")
    new_grid: List[List[Optional[int]]] = []
    file = open(TEST_DATA / "test_output.txt")
    for line in file:
        split: List[str] = line.split()
        row: List[Optional[int]] = [
            int(x) if x.isdigit() else None for x in split
        ]
        new_grid.append(row)
    assert grid == new_grid


def test_valid_sudoku_solution() -> None:
    grid: List[List[Optional[int]]] = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]
    s: Sudoku = Sudoku(grid)
    assert s.check_solution() is True

    grid = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, None, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, None],
    ]
    s = Sudoku(grid)
    assert s.check_solution() is True


def test_invalid_sudoku_solution() -> None:
    grid: List[List[Optional[int]]] = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 1],  # This last cell should be 9 instead of 1
    ]
    s: Sudoku = Sudoku(grid)
    assert not s.check_solution()
    grid = [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 9, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 5],
    ]
    s = Sudoku(grid)
    assert not s.check_solution()


def test_sat_solver() -> None:
    s: Sudoku = Sudoku.read_sudoku(TEST_DATA / "test_input.txt")
    cnf: CNF = encode_sat(s)
    solved_grid: List[List[int]] | None = solve_sat(cnf)
    assert solved_grid == [
        [2, 1, 4, 9, 7, 8, 3, 6, 5],
        [3, 6, 5, 1, 4, 2, 8, 9, 7],
        [8, 9, 7, 6, 5, 3, 2, 1, 4],
        [6, 4, 2, 3, 1, 5, 9, 7, 8],
        [5, 3, 1, 7, 8, 9, 6, 4, 2],
        [9, 7, 8, 4, 2, 6, 5, 3, 1],
        [1, 2, 3, 8, 9, 7, 4, 5, 6],
        [4, 5, 6, 2, 3, 1, 7, 8, 9],
        [7, 8, 9, 5, 6, 4, 1, 2, 3],
    ]
    s = Sudoku.read_sudoku(TEST_DATA / "test_input2.txt")
    cnf = encode_sat(s)
    solved_grid = solve_sat(cnf)
    assert solved_grid == [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]


def test_int_solver() -> None:
    s: Sudoku = Sudoku.read_sudoku(TEST_DATA / "test_input.txt")

    int_encoding, x = encode_int(s)
    solved_grid: List[List[int]] | None = solve_int(s, int_encoding, x)

    assert solved_grid == [
        [2, 1, 4, 9, 7, 8, 3, 6, 5],
        [3, 6, 5, 1, 4, 2, 8, 9, 7],
        [8, 9, 7, 6, 5, 3, 2, 1, 4],
        [6, 4, 2, 3, 1, 5, 9, 7, 8],
        [5, 3, 1, 7, 8, 9, 6, 4, 2],
        [9, 7, 8, 4, 2, 6, 5, 3, 1],
        [1, 2, 3, 8, 9, 7, 4, 5, 6],
        [4, 5, 6, 2, 3, 1, 7, 8, 9],
        [7, 8, 9, 5, 6, 4, 1, 2, 3],
    ]

    s = Sudoku.read_sudoku(TEST_DATA / "test_input2.txt")
    int_encoding, x = encode_int(s)
    solved_grid = solve_int(s, int_encoding, x)

    assert solved_grid == [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]


def test_const_solver() -> None:
    s: Sudoku = Sudoku.read_sudoku(TEST_DATA / "test_input.txt")

    model, x = encode_const(s)
    solved_grid: List[List[int]] | None = solve_const(s, model, x)

    assert solved_grid == [
        [2, 1, 4, 9, 7, 8, 3, 6, 5],
        [3, 6, 5, 1, 4, 2, 8, 9, 7],
        [8, 9, 7, 6, 5, 3, 2, 1, 4],
        [6, 4, 2, 3, 1, 5, 9, 7, 8],
        [5, 3, 1, 7, 8, 9, 6, 4, 2],
        [9, 7, 8, 4, 2, 6, 5, 3, 1],
        [1, 2, 3, 8, 9, 7, 4, 5, 6],
        [4, 5, 6, 2, 3, 1, 7, 8, 9],
        [7, 8, 9, 5, 6, 4, 1, 2, 3],
    ]

    s = Sudoku.read_sudoku(TEST_DATA / "test_input2.txt")
    model, x = encode_const(s)
    solved_grid = solve_const(s, model, x)

    assert solved_grid == [
        [5, 3, 4, 6, 7, 8, 9, 1, 2],
        [6, 7, 2, 1, 9, 5, 3, 4, 8],
        [1, 9, 8, 3, 4, 2, 5, 6, 7],
        [8, 5, 9, 7, 6, 1, 4, 2, 3],
        [4, 2, 6, 8, 5, 3, 7, 9, 1],
        [7, 1, 3, 9, 2, 4, 8, 5, 6],
        [9, 6, 1, 5, 3, 7, 2, 8, 4],
        [2, 8, 7, 4, 1, 9, 6, 3, 5],
        [3, 4, 5, 2, 8, 6, 1, 7, 9],
    ]
