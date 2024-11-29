from typing import Tuple
from attr import dataclass
from pysat.formula import CNF  # type: ignore
from .sudoku import Sudoku  # type: ignore
from .sudoku_constraint import encode_const, solve_const  # type: ignore
from .sudoku_integer import encode_int, solve_int  # type: ignore
from .sudoku_sat import encode_sat, solve_sat  # type: ignore

Matrix = list[list[int]]


@dataclass
class SudokuSolver:
    @staticmethod
    def solve_with_sat(sudoku: Sudoku) -> Matrix:
        cnf: CNF = encode_sat(sudoku)
        return solve_sat(cnf, sudoku.n)

    @staticmethod
    def solve_with_integer_programming(sudoku: Sudoku) -> Matrix:
        int_encoding, x = encode_int(sudoku)
        return solve_int(sudoku, int_encoding, x)

    @staticmethod
    def solve_with_constraint_programming(sudoku: Sudoku) -> Matrix:
        model, x = encode_const(sudoku)
        return solve_const(sudoku, model, x)

    @staticmethod
    def solve_all_methods(sudoku: Sudoku) -> Tuple[Matrix, Matrix, Matrix]:
        sat_solution = SudokuSolver.solve_with_sat(sudoku)
        ip_solution = SudokuSolver.solve_with_integer_programming(sudoku)
        cp_solution = SudokuSolver.solve_with_constraint_programming(sudoku)
        return sat_solution, ip_solution, cp_solution
