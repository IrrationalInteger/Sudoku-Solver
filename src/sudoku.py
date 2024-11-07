import argparse
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import List, Optional,TextIO

@dataclass
class Sudoku:
    grid: List[List[Optional[int]]]

    def __init__(self, grid:Optional[List[List[Optional[int]]]]=None):
        if grid is None:
            grid = []
        self.grid = grid

    def read_sudoku(self,path: str) -> None:
        grid:List[List[Optional[int]]] = []
        file:TextIO = open(path)
        for line in file:
            split:List[str] = line.split()
            row:List[Optional[int]] = [int(x) if x.isdigit() else None for x in split]
            grid.append(row)
        self.grid = grid

    def write_sudoku(self,path: str) -> None:
        file:TextIO = open(path, "w")
        for row in self.grid:
            file.write(' '.join(str(x) if x is not None else '_' for x in row))
            file.write("\n")

    def check_solution(self) -> bool:
        def has_duplicates(numbers: List[Optional[int]]) -> bool:
            numbers = [x for x in numbers if x is not None]
            return len(numbers) == len(set(numbers))

        for row in self.grid:
            if not has_duplicates(row):
                return False

        for col in range(9):
            column:List[Optional[int]] = [self.grid[row][col] for row in range(9)]
            if not has_duplicates(column):
                return False

        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                subgrid:List[Optional[int]] = []
                for r in range(start_row, start_row + 3):
                    for c in range(start_col, start_col + 3):
                        subgrid.append(self.grid[r][c])
                if not has_duplicates(subgrid):
                    return False
        return True


def main() -> None:
    parser:ArgumentParser = argparse.ArgumentParser(prog="Sudoku Solver", description="This is a sudoko solver that reads problems from an input txt and checks if they are solvable")
    parser.add_argument("input", type=str, help="Path to the input file with the Sudoku puzzle")
    parser.add_argument("output", type=str, help="Path to the output file to write the Sudoku puzzle")
    args:argparse.Namespace = parser.parse_args()

    sudoku:Sudoku = Sudoku()
    sudoku.read_sudoku(args.input)
    sudoku.write_sudoku(args.output)

    if sudoku.check_solution():
        print("The Sudoku puzzle is solved correctly or can be solved.")
    else:
        print("The Sudoku puzzle solution is incorrect.")

if __name__ == "__main__":
    main()


