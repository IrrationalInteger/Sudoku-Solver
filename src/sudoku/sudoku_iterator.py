from dataclasses import dataclass
from typing import List, Generator


@dataclass
class SudokuIterator:
    grid: List[List[int | None]]

    def iter_rows(self) -> Generator[List[tuple[int, int]], None, None]:
        for r in range(len(self.grid)):
            yield [(r, c) for c in range(len(self.grid))]

    def iter_cols(self) -> Generator[List[tuple[int, int]], None, None]:
        for c in range(len(self.grid)):
            yield [(r, c) for r in range(len(self.grid))]

    def iter_cells(self) -> Generator[List[tuple[int, int]], None, None]:
        subgrid_size = int(len(self.grid) ** 0.5)
        for br in range(0, len(self.grid), subgrid_size):
            for bc in range(0, len(self.grid), subgrid_size):
                yield [
                    (br + r, bc + c)
                    for r in range(subgrid_size)
                    for c in range(subgrid_size)
                ]
