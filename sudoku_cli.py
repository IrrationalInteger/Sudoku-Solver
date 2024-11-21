import cmd
from pathlib import Path
from typing import List, cast

from attr import dataclass
from src.sudoku import Sudoku, SudokuSolver


def print_matrix(matrix: List[List[int]]) -> None:
    for row in matrix:
        print(" ".join(str(cell) if cell is not None else "." for cell in row))


@dataclass(init=False)
class SudokuCLI(cmd.Cmd):
    intro = (
        "Welcome to the Sudoku Solver CLI! "
        "Type 'help' or '?' for a list of commands.\n"
    )
    prompt = "Sudoku Solver: "
    current_solution = None
    solver = SudokuSolver()
    sudoku = None

    def __init__(self) -> None:
        super().__init__()

    def do_load(self, file_path: str) -> None:
        if not file_path:
            print("Usage: load <file_path>")
            return
        try:
            self.sudoku = Sudoku.read_sudoku(Path(file_path))
            self.current_solution = None
            print(f"Sudoku puzzle loaded from '{file_path}'.")
        except Exception as e:
            print(f"Error: Could not load puzzle. {e}")

    def do_solve(self, method: str) -> None:
        if not self.sudoku:
            print("Error: No puzzle loaded. Use 'load <file_path>' first.")
            return
        elif not self.sudoku.check_solution():
            print("This puzzle has no solution!")
            return
        method = method.strip().lower()
        if method not in {"sat", "ip", "cp", "all"}:
            print("Usage: solve <sat|ip|cp|all>")
            return

        try:
            if method == "sat":
                self.current_solution = self.solver.solve_with_sat(self.sudoku)
                print("Solved using SAT solver:")
                print_matrix(self.current_solution)
            elif method == "ip":
                self.current_solution = (
                    self.solver.solve_with_integer_programming(self.sudoku)
                )
                print("Solved using Integer Programming:")
                print_matrix(self.current_solution)
            elif method == "cp":
                self.current_solution = (
                    self.solver.solve_with_constraint_programming(self.sudoku)
                )
                print("Solved using Constraint Programming:")
                print_matrix(self.current_solution)
            elif method == "all":
                solutions = self.solver.solve_all_methods(self.sudoku)
                self.current_solution = solutions[0]
                for name, solution in zip(
                    ["SAT", "Integer Programming", "Constraint Programming"],
                    solutions,
                ):
                    print(f"{name} Solution:")
                    print_matrix(solution)
        except Exception as e:
            print(f"Error: Could not solve the puzzle. {e}")

    def do_show(self, arg: str) -> None:
        if not self.sudoku:
            print("Error: No puzzle loaded.")
            return

        arg = arg.strip().lower()
        if arg == "puzzle":
            print("Current Puzzle:")
            print_matrix(cast(list[list[int]], self.sudoku.grid))
        elif arg == "solution":
            if self.current_solution:
                print("Current Solution:")
                print_matrix(self.current_solution)
            else:
                print("Error: No solution available. Use 'solve' first.")
        else:
            print("Usage: show <puzzle|solution>")

    def do_save(self, file_path: str) -> None:
        if not self.sudoku:
            print("Error: No puzzle loaded.")
            return
        if not file_path:
            print("Usage: save <file_path>")
            return

        try:
            self.sudoku.write_sudoku(Path(file_path))
            print(f"Puzzle saved to '{file_path}'.")
        except Exception as e:
            print(f"Error: Could not save the puzzle. {e}")


if __name__ == "__main__":
    SudokuCLI().cmdloop()
