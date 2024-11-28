from dataclasses import dataclass
from typing import Iterator


@dataclass
class SudokuIterator:
    grid: list[list[int | None]]

    def iter_rows(self) -> Iterator[list[tuple[int, int]]]:
        for r in range(len(self.grid)):
            yield [(r, c) for c in range(len(self.grid))]

    def iter_cols(self) -> Iterator[list[tuple[int, int]]]:
        for c in range(len(self.grid)):
            yield [(r, c) for r in range(len(self.grid))]

    def iter_cells(self) -> Iterator[list[tuple[int, int]]]:
        subgrid_size = int(len(self.grid) ** 0.5)
        for br in range(0, len(self.grid), subgrid_size):
            for bc in range(0, len(self.grid), subgrid_size):
                yield [
                    (br + r, bc + c)
                    for r in range(subgrid_size)
                    for c in range(subgrid_size)
                ]
