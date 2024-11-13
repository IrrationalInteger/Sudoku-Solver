from typing import List, Tuple, Any, cast
from ortools.linear_solver import pywraplp  # type: ignore
from src.sudoku.sudoku import Sudoku


def encode_int(sudoku: Sudoku) -> Tuple[Any, List[List[Any]]]:
    solver = pywraplp.Solver.CreateSolver("SCIP")
    x = [
        [
            [solver.BoolVar(f"b_{r}_{c}_{v + 1}") for v in range(sudoku.n)]
            for c in range(sudoku.n)
        ]
        for r in range(sudoku.n)
    ]

    for r in range(sudoku.n):
        for c in range(sudoku.n):
            solver.Add(sum(x[r][c][v] for v in range(sudoku.n)) == 1)

    for r in range(sudoku.n):
        for v in range(sudoku.n):
            solver.Add(sum(x[r][c][v] for c in range(sudoku.n)) == 1)

    for c in range(sudoku.n):
        for v in range(sudoku.n):
            solver.Add(sum(x[r][c][v] for r in range(sudoku.n)) == 1)

    for block_row in range(3):
        for block_col in range(3):
            for v in range(sudoku.n):
                cells = [
                    (block_row * 3 + r, block_col * 3 + c)
                    for r in range(3)
                    for c in range(3)
                ]
                solver.Add(sum(x[r][c][v] for r, c in cells) == 1)

    for r in range(sudoku.n):
        for c in range(sudoku.n):
            if sudoku.grid[r][c] is not None:
                v = cast(int, sudoku.grid[r][c]) - 1
                solver.Add(x[r][c][v] == 1)

    return solver, x


def solve_int(
    sudoku: Sudoku, solver: Any, x: List[List[Any]]
) -> List[List[int]] | None:
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        solved_grid = [[0] * sudoku.n for _ in range(sudoku.n)]
        for r in range(sudoku.n):
            for c in range(sudoku.n):
                for v in range(sudoku.n):
                    if x[r][c][v].solution_value() == 1:
                        solved_grid[r][c] = v + 1
                        break
        return solved_grid
    else:
        print("No solution found!")
        return None
