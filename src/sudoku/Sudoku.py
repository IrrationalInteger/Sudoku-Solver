import argparse
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Sudoku:
    grid: List[List[Optional[int]]]

    def __init__(self):
        pass

    def read_sudoku(self,path: str) -> None:
        grid = []
        file = open(path)
        for line in file:
            split = line.split()
            row = [int(x) if x.isdigit() else None for x in split]
            grid.append(row)
        self.grid = grid
        
    def write_sudoku(self,path: str) -> None:
        file = open(path, "w")
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
            column = [self.grid[row][col] for row in range(9)]
            if not has_duplicates(column):
                return False

        for start_row in range(0, 9, 3):
            for start_col in range(0, 9, 3):
                subgrid = []
                for r in range(start_row, start_row + 3):
                    for c in range(start_col, start_col + 3):
                        subgrid.append(self.grid[r][c])
                if not has_duplicates(subgrid):
                    return False
        return True





