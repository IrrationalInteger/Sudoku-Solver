import time
from typing import Any
from src.sudoku import SudokuSolver
from config import TEST_DATA
from src.sudoku.sudoku import Sudoku


def measure_time(func:Any, args:Any) -> tuple[Any, float]:
    start_time = time.time()
    result = func(*args)
    end_time = time.time()
    return result, end_time - start_time

def test_solver() -> tuple[float, float, float, int]:
    sudoku = Sudoku.read_sudoku(TEST_DATA/"test_performance_input.txt")
    s = sudoku.n
    print(f"Testing {s}x{s} Sudoku puzzle:")

    _, sat_t = measure_time(SudokuSolver.solve_with_sat, [sudoku])
    print(f"SAT approach took {sat_t:.4f} seconds.")

    _, int_t = measure_time(SudokuSolver.solve_with_integer_programming, [sudoku])
    print(f"Integer Programming approach took {int_t:.4f} seconds.")

    _, const_t = measure_time(SudokuSolver.solve_with_constraint_programming, [sudoku])
    print(f"Constraint Programming approach took {const_t:.4f} seconds.")

    return sat_t, int_t, const_t, s


if __name__ == "__main__":
    sat_time, int_time, const_time, size = test_solver()
    with open(TEST_DATA/"test_performance_output.txt", "a") as f:
        f.write(f"Performance for sudoku size {size}x{size}\n")
        f.write(f"SAT: {sat_time:.4f}\n")
        f.write(f"Integer: {int_time:.4f}\n")
        f.write(f"Constraint: {const_time:.4f}\n")
