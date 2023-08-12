import sys
import time
from ortools.sat.python import cp_model


class NQueensSolutionPrinter(cp_model.CpSolverSolutionCallback):
    """Print intermediate solutions."""

    def __init__(self, queens):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__queens = queens
        self.__solution_count = 0
        self.__start_time = time.time()

    def solution_count(self):
        return self.__solution_count

    def on_solution_callback(self):
        current_time = time.time()
        print(
            f"Solution {self.__solution_count}, "
            f"time = {current_time - self.__start_time} s"
        )
        self.__solution_count += 1

        all_queens = range(len(self.__queens))
        for i in all_queens:
            for j in all_queens:
                if self.Value(self.__queens[j]) == i:
                    # There is a queen in column j, row i
                    print("Q", end=" ")
                else:
                    print("_", end=" ")
            print()
        print()


def main(board_size):
    model = cp_model.CpModel()

    # There are `board_size` number of variables, one for a queen in each column
    # of the board. The value of each variable is the row that the queen is in.
    queens = [model.NewIntVar(0, board_size - 1, f"x_{i}") for i in range(board_size)]

    # All rows must be different.
    model.AddAllDifferent(queens)

    # No two queens can be on the same diagonal.
    model.AddAllDifferent(queens[i] + i for i in range(board_size))
    model.AddAllDifferent(queens[i] - i for i in range(board_size))

    solver = cp_model.CpSolver()
    solution_printer = NQueensSolutionPrinter(queens)
    solver.parameters.enumerate_all_solutions = True
    status = solver.Solve(model, solution_printer)

    if status == cp_model.OPTIMAL:
        print("Total solutions found:", solution_printer.solution_count())
    else:
        print("No solutions found.")


if __name__ == "__main__":
    # By default, solve the 8x8 problem.
    size = 8
    if len(sys.argv) > 1:
        size = int(sys.argv[1])
    main(size)
