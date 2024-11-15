import argparse
from argparse import ArgumentParser
from typing import List, cast

from pysat.formula import CNF  # type: ignore

from config import TEST_DATA
from src.sudoku.sudoku import Sudoku
from src.sudoku.sudoku_constraint import encode_const, solve_const
from src.sudoku.sudoku_integer import encode_int, solve_int
from src.sudoku.sudoku_sat import encode_sat, solve_sat

if __name__ == "__main__":
    parser: ArgumentParser = argparse.ArgumentParser(
        prog="Sudoku Solver",
        description="This is a sudoko solver that reads problems"
        " from an input txt and checks if they are solvable",
    )
    # TODO: Refactor to use files
    parser.add_argument(
        "input", type=str, help="Path to the input file with the Sudoku puzzle"
    )
    parser.add_argument(
        "output",
        type=str,
        help="Path to the output file to write the Sudoku puzzle",
    )
    args: argparse.Namespace = parser.parse_args()

    sudoku: Sudoku = Sudoku.read_sudoku(TEST_DATA / args.input)
    sudoku.write_sudoku(TEST_DATA / args.output)

    if sudoku.check_solution():
        print("The Sudoku puzzle is solved correctly or can be solved.")

        def print_matrix(matrix: List[List[int | None]]) -> None:
            for row in matrix:
                print(" ".join(map(str, row)))

        cnf: CNF = encode_sat(sudoku)
        print("Solving Sudoku puzzle using SAT solver...")
        print_matrix(cast(List[List[int | None]], solve_sat(cnf, sudoku.n)))

        int_encoding, x = encode_int(sudoku)
        print("Solving Sudoku puzzle using Integer Programming...")
        print_matrix(
            cast(List[List[int | None]], solve_int(sudoku, int_encoding, x))
        )

        model, x = encode_const(sudoku)
        print("Solving Sudoku puzzle using Constraint Programming...")
        print_matrix(
            cast(List[List[int | None]], solve_const(sudoku, model, x))
        )
    else:
        print("The Sudoku puzzle solution is incorrect.")
