from typing import List, Optional
from pysat.formula import CNF  # type: ignore
from sudoku.sudoku import Sudoku
from sudoku.sudoku_constraint import encode_const, solve_const
from sudoku.sudoku_integer import encode_int, solve_int
from sudoku.sudoku_sat import encode_sat, solve_sat

from pathlib import Path
TEST_DATA = Path(__file__).parent / "test_data"


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
    solved_grid: List[List[int]] | None = solve_sat(cnf, len(s.grid))
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
    solved_grid = solve_sat(cnf, len(s.grid))
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
    s = Sudoku.read_sudoku(TEST_DATA / "test_input3.txt")
    cnf = encode_sat(s)
    solved_grid = solve_sat(cnf, len(s.grid))
    assert solved_grid == [
        [10, 13, 15, 8, 9, 3, 2, 4, 16, 11, 7, 6, 12, 14, 5, 1],
        [4, 12, 2, 6, 15, 7, 11, 8, 1, 9, 14, 5, 13, 10, 16, 3],
        [11, 14, 16, 7, 1, 6, 10, 5, 4, 12, 13, 3, 8, 15, 2, 9],
        [5, 1, 3, 9, 14, 16, 12, 13, 8, 10, 15, 2, 4, 11, 7, 6],
        [16, 5, 4, 1, 11, 9, 15, 7, 13, 14, 6, 8, 3, 2, 12, 10],
        [13, 6, 7, 11, 8, 10, 1, 2, 3, 16, 9, 12, 5, 4, 15, 14],
        [12, 15, 10, 14, 6, 4, 16, 3, 5, 2, 1, 7, 11, 8, 9, 13],
        [9, 3, 8, 2, 13, 12, 5, 14, 11, 15, 4, 10, 6, 7, 1, 16],
        [1, 2, 6, 3, 10, 8, 9, 11, 15, 5, 12, 13, 14, 16, 4, 7],
        [7, 9, 5, 4, 12, 14, 13, 16, 10, 6, 11, 1, 15, 3, 8, 2],
        [15, 16, 14, 10, 5, 2, 7, 6, 9, 8, 3, 4, 1, 12, 13, 11],
        [8, 11, 13, 12, 3, 15, 4, 1, 14, 7, 2, 16, 9, 6, 10, 5],
        [2, 4, 9, 13, 7, 11, 6, 15, 12, 1, 10, 14, 16, 5, 3, 8],
        [6, 7, 1, 15, 16, 5, 3, 9, 2, 4, 8, 11, 10, 13, 14, 12],
        [14, 10, 11, 5, 4, 13, 8, 12, 7, 3, 16, 9, 2, 1, 6, 15],
        [3, 8, 12, 16, 2, 1, 14, 10, 6, 13, 5, 15, 7, 9, 11, 4],
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

    s = Sudoku.read_sudoku(TEST_DATA / "test_input3.txt")
    int_encoding, x = encode_int(s)
    solved_grid = solve_int(s, int_encoding, x)

    assert solved_grid == [
        [10, 13, 15, 8, 9, 3, 2, 4, 16, 11, 7, 6, 12, 14, 5, 1],
        [4, 12, 2, 6, 15, 7, 11, 8, 1, 9, 14, 5, 13, 10, 16, 3],
        [11, 14, 16, 7, 1, 6, 10, 5, 4, 12, 13, 3, 8, 15, 2, 9],
        [5, 1, 3, 9, 14, 16, 12, 13, 8, 10, 15, 2, 4, 11, 7, 6],
        [16, 5, 4, 1, 11, 9, 15, 7, 13, 14, 6, 8, 3, 2, 12, 10],
        [13, 6, 7, 11, 8, 10, 1, 2, 3, 16, 9, 12, 5, 4, 15, 14],
        [12, 15, 10, 14, 6, 4, 16, 3, 5, 2, 1, 7, 11, 8, 9, 13],
        [9, 3, 8, 2, 13, 12, 5, 14, 11, 15, 4, 10, 6, 7, 1, 16],
        [1, 2, 6, 3, 10, 8, 9, 11, 15, 5, 12, 13, 14, 16, 4, 7],
        [7, 9, 5, 4, 12, 14, 13, 16, 10, 6, 11, 1, 15, 3, 8, 2],
        [15, 16, 14, 10, 5, 2, 7, 6, 9, 8, 3, 4, 1, 12, 13, 11],
        [8, 11, 13, 12, 3, 15, 4, 1, 14, 7, 2, 16, 9, 6, 10, 5],
        [2, 4, 9, 13, 7, 11, 6, 15, 12, 1, 10, 14, 16, 5, 3, 8],
        [6, 7, 1, 15, 16, 5, 3, 9, 2, 4, 8, 11, 10, 13, 14, 12],
        [14, 10, 11, 5, 4, 13, 8, 12, 7, 3, 16, 9, 2, 1, 6, 15],
        [3, 8, 12, 16, 2, 1, 14, 10, 6, 13, 5, 15, 7, 9, 11, 4],
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

    s = Sudoku.read_sudoku(TEST_DATA / "test_input3.txt")
    model, x = encode_const(s)
    solved_grid = solve_const(s, model, x)

    assert solved_grid == [
        [10, 13, 15, 8, 9, 3, 2, 4, 16, 11, 7, 6, 12, 14, 5, 1],
        [4, 12, 2, 6, 15, 7, 11, 8, 1, 9, 14, 5, 13, 10, 16, 3],
        [11, 14, 16, 7, 1, 6, 10, 5, 4, 12, 13, 3, 8, 15, 2, 9],
        [5, 1, 3, 9, 14, 16, 12, 13, 8, 10, 15, 2, 4, 11, 7, 6],
        [16, 5, 4, 1, 11, 9, 15, 7, 13, 14, 6, 8, 3, 2, 12, 10],
        [13, 6, 7, 11, 8, 10, 1, 2, 3, 16, 9, 12, 5, 4, 15, 14],
        [12, 15, 10, 14, 6, 4, 16, 3, 5, 2, 1, 7, 11, 8, 9, 13],
        [9, 3, 8, 2, 13, 12, 5, 14, 11, 15, 4, 10, 6, 7, 1, 16],
        [1, 2, 6, 3, 10, 8, 9, 11, 15, 5, 12, 13, 14, 16, 4, 7],
        [7, 9, 5, 4, 12, 14, 13, 16, 10, 6, 11, 1, 15, 3, 8, 2],
        [15, 16, 14, 10, 5, 2, 7, 6, 9, 8, 3, 4, 1, 12, 13, 11],
        [8, 11, 13, 12, 3, 15, 4, 1, 14, 7, 2, 16, 9, 6, 10, 5],
        [2, 4, 9, 13, 7, 11, 6, 15, 12, 1, 10, 14, 16, 5, 3, 8],
        [6, 7, 1, 15, 16, 5, 3, 9, 2, 4, 8, 11, 10, 13, 14, 12],
        [14, 10, 11, 5, 4, 13, 8, 12, 7, 3, 16, 9, 2, 1, 6, 15],
        [3, 8, 12, 16, 2, 1, 14, 10, 6, 13, 5, 15, 7, 9, 11, 4],
    ]
