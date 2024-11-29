import math
from dataclasses import dataclass
from pathlib import Path
from sudoku.sudoku_iterator import SudokuIterator


@dataclass
class Sudoku:
    grid: list[list[int | None]]
    n: int

    def __init__(self, grid: list[list[int | None]]) -> None:
        self.grid = grid
        self.n = len(grid)

    @staticmethod
    def read_sudoku(path: Path) -> "Sudoku":
        grid: list[list[int | None]] = []
        with open(path) as file:
            size = 0
            for index, line in enumerate(file):
                split: list[str] = line.split()
                row: list[int | None] = [
                    int(x) if x.isdigit() else None for x in split
                ]
                size = max(size, len(row))
                if math.isqrt(len(row)) ** 2 != len(row):
                    size = max(size, (math.isqrt(len(row)) + 1) ** 2)
                    print(
                        f"Row {index + 1} is not a perfect square, appending "
                        f"{(math.isqrt(len(row))+1) ** 2  - len(row)}"
                        f" None values."
                    )
                    row += [None] * (
                        (math.isqrt(len(row)) + 1) ** 2 - len(row)
                    )
                grid.append(row)
        for index, row in enumerate(grid):
            if size != len(row):
                print(f"Fixing row {index + 1} size with None values.")
                row += [None] * (size - len(row))
        if size != len(grid):
            print("Fixing grid size with None values.")
            grid += [[None] * size] * (size - len(grid))
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
        def has_no_duplicates(numbers: list[int | None]) -> bool:
            numbers = [x for x in numbers if x is not None]
            return len(numbers) == len(set(numbers))

        iterator = SudokuIterator(self.grid)

        for cells in iterator.iter_rows():
            row = [self.grid[r][c] for r, c in cells]
            if not has_no_duplicates(row):
                return False

        for cells in iterator.iter_cols():
            col = [self.grid[r][c] for r, c in cells]
            if not has_no_duplicates(col):
                return False

        for cells in iterator.iter_cells():
            subgrid = [self.grid[r][c] for r, c in cells]
            if not has_no_duplicates(subgrid):
                return False

        return True
