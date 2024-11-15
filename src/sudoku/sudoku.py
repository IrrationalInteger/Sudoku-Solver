from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class Sudoku:
    grid: List[List[int | None]]
    n: int

    def __init__(self, grid: List[List[int | None]]) -> None:
        self.grid = grid
        self.n = len(grid)

    # TODO: Change all code to use n>9
    @staticmethod
    def read_sudoku(path: Path) -> "Sudoku":
        grid: List[List[int | None]] = []
        with open(path) as file:
            for index, line in enumerate(
                file
            ):  # Use enumerate to get the index of each line
                split: List[str] = line.split()
                row: List[int | None] = [
                    int(x) if x.isdigit() else None for x in split
                ]
                if len(row) < 9:
                    print(
                        f"Row {index + 1} is shorter than 9 elements, "
                        f"appending {9 - len(row)} None values."
                    )
                    row += [None] * (9 - len(row))
                grid.append(row)

        if len(grid) < 9:
            print(
                "Grid has fewer than 9 rows, appending rows of 9 None values."
            )
            grid += [[None] * 9] * (9 - len(grid))

        s: Sudoku = Sudoku(grid)
        return s

    def write_sudoku(self, path: Path) -> None:
        with open(path, "w") as file:
            for row in self.grid:
                print(
                    " ".join(str(x) if x is not None else "_" for x in row),
                    file=file,
                )

    def check_solution(self) -> bool:
        def has_no_duplicates(numbers: List[int | None]) -> bool:
            numbers = [x for x in numbers if x is not None]
            return len(numbers) == len(set(numbers))

        for row in self.grid:
            if not has_no_duplicates(row):
                return False

        for col in range(9):
            column: List[int | None] = [
                self.grid[row][col] for row in range(9)
            ]
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
