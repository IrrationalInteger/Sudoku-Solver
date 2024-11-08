import argparse
from argparse import ArgumentParser
from dataclasses import dataclass
from pathlib import Path
from typing import List, cast
from pysat.solvers import Glucose3  # type: ignore
from pysat.formula import CNF  # type: ignore
from config import TEST_DATA


@dataclass
class Sudoku:
    grid: List[List[int | None]]

    @staticmethod
    def read_sudoku(path: Path) -> "Sudoku":
        grid: List[List[int | None]] = []
        with open(path) as file:
            for index, line in enumerate(
                file
            ):  # Use enumerate to get the index of each line
                split: List[str] = line.split()
                row: List[int | None] = [int(x) if x.isdigit() else None for x in split]
                if len(row) < 9:
                    print(
                        f"Row {index + 1} is shorter than 9 elements, appending {9 - len(row)} None values."
                    )
                    row += [None] * (9 - len(row))
                grid.append(row)

        if len(grid) < 9:
            print("Grid has fewer than 9 rows, appending rows of 9 None values.")
            grid += [[None] * 9] * (9 - len(grid))
        return Sudoku(grid)

    def write_sudoku(self, path: Path) -> None:
        with open(path, "w") as file:
            for row in self.grid:
                print(
                    " ".join(str(x) if x is not None else "_" for x in row), file=file
                )

    def check_solution(self) -> bool:
        def has_no_duplicates(numbers: List[int | None]) -> bool:
            numbers = [x for x in numbers if x is not None]
            return len(numbers) == len(set(numbers))

        for row in self.grid:
            if not has_no_duplicates(row):
                return False

        for col in range(9):
            column: List[int | None] = [self.grid[row][col] for row in range(9)]
            if not has_no_duplicates(column):
                return False

        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                subgrid: List[int | None] = []
                for r in range(start_row, start_row + 3):
                    for c in range(start_col, start_col + 3):
                        subgrid.append(self.grid[r][c])
                if not has_no_duplicates(subgrid):
                    return False
        return True

    @staticmethod
    def encode_sat(grid: List[List[int | None]]) -> CNF:
        cnf: CNF = CNF()

        def x(row: int, col: int, val: int) -> int:
            return row * 81 + col * 9 + val

        for r in range(9):
            for c in range(9):
                if grid[r][c] is not None:
                    cnf.append([x(r, c, cast(int, (grid[r][c])))])
                else:
                    cnf.append([x(r, c, v) for v in range(1, 10)])
                    for v1 in range(1, 10):
                        for v2 in range(v1 + 1, 10):
                            cnf.append([-x(r, c, v1), -x(r, c, v2)])

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

        for block_row in range(3):
            for block_col in range(3):
                for v in range(1, 10):
                    for r1 in range(3):
                        for c1 in range(3):
                            for r2 in range(3):
                                for c2 in range(3):
                                    if (r1, c1) < (r2, c2):
                                        cnf.append(
                                            [
                                                -x(
                                                    block_row * 3 + r1,
                                                    block_col * 3 + c1,
                                                    v,
                                                ),
                                                -x(
                                                    block_row * 3 + r2,
                                                    block_col * 3 + c2,
                                                    v,
                                                ),
                                            ]
                                        )
        return cnf

    @staticmethod
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


def main() -> None:
    parser: ArgumentParser = argparse.ArgumentParser(
        prog="Sudoku Solver",
        description="This is a sudoko solver that reads problems from an input txt and checks if they are solvable",
    )
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
        cnf: CNF = Sudoku.encode_sat(sudoku.grid)
        print("Solving Sudoku puzzle using SAT solver...")

        def print_matrix(matrix):
            for row in matrix:
                print(" ".join(map(str, row)))

        print(Sudoku.solve_sat(cnf))
    else:
        print("The Sudoku puzzle solution is incorrect.")


if __name__ == "__main__":
    main()
