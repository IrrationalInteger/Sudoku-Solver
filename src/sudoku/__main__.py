import argparse
from argparse import ArgumentParser
from pysat.formula import CNF  # type: ignore
from config import TEST_DATA
from src.sudoku.sudoku import Sudoku
from src.sudoku.sudoku_sat import encode_sat, solve_sat

if __name__ == "__main__":
    parser: ArgumentParser = argparse.ArgumentParser(
        prog="Sudoku Solver",
        description="This is a sudoko solver that reads problems from an input txt and checks if they are solvable",
    )
    # TODO: Refactor to use files
    parser.add_argument(
        "input", type=str, help="Path to the input file with the Sudoku puzzle"
    )
    parser.add_argument(
        "output", type=str, help="Path to the output file to write the Sudoku puzzle"
    )
    args: argparse.Namespace = parser.parse_args()

    sudoku: Sudoku = Sudoku.read_sudoku(TEST_DATA / args.input)
    sudoku.write_sudoku(TEST_DATA / args.output)

    if sudoku.check_solution():
        print("The Sudoku puzzle is solved correctly or can be solved.")
        cnf: CNF = encode_sat(sudoku.grid)
        print("Solving Sudoku puzzle using SAT solver...")

        def print_matrix(matrix):
            for row in matrix:
                print(" ".join(map(str, row)))

        print_matrix(solve_sat(cnf))
    else:
        print("The Sudoku puzzle solution is incorrect.")
