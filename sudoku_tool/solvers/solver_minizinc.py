# Author: Bartlomiej Moniak 2023
# Repository: https://github.com/bmoniak/n_dimensional_sudoku_tool
# Distributed under MIT License

from minizinc import Instance, Model, Solver
from sudoku_tool import Sudoku, import_data
import datetime

def solve_sudoku(sudoku:Sudoku, solver:str = "gecode", timeout_seconds:int = 1000, stats:bool=False):
    res = solve_sudoku_minizinc(sudoku, solver)
    return res

def check_if_unique(sudoku: Sudoku, solver_name:str = "gecode", timeout_seconds:int = 1000):
    if timeout_seconds <= 0:
        raise Exception("Timeout value has to be integer greater than zero.")
    sudoku_solver = Model("./sudoku_tool/solvers/sudoku.mzn")
    if solver_name == "highs":
        print('This solver may not be able to find more than one solution. In case of execution errors please try using different one.')
    try:
        chosen_solver = Solver.lookup(solver_name)
    except:
        raise Exception('No solver found, please make sure you use a correct name!')
    instance = Instance(chosen_solver, sudoku_solver)
    instance["N"] = sudoku.n
    instance["start"] = sudoku.grid.tolist()
    result = instance.solve(timeout = datetime.timedelta(seconds=timeout_seconds), nr_solutions=2, processes=4)
    if len(result) == 1:
        return True
    else:
        return False
    
def solve_sudoku_minizinc(sudoku:Sudoku, solver_name:str = "gecode", timeout_seconds:int = 1000, stats:bool=False):
    if timeout_seconds <= 0:
        raise Exception("Timeout value has to be integer greater than zero.")
    sudoku_solver_file = Model("./sudoku_tool/solvers/sudoku.mzn")
    # Find the MiniZinc solver configuration for given solver
    try:
        chosen_solver = Solver.lookup(solver_name)
    except:
        raise Exception('No solver found, please make sure you use a correct name!')

    instance = Instance(chosen_solver, sudoku_solver_file)
    instance["N"] = sudoku.n
    instance["start"] = sudoku.grid.tolist()
    if solver_name == "highs":
        result = instance.solve(timeout = datetime.timedelta(seconds=timeout_seconds), processes=1)
    else:
        result = instance.solve(timeout = datetime.timedelta(seconds=timeout_seconds), nr_solutions=1, processes=1)
    # Output the array
    if len(result) > 0:
        try:
            solved_grid = result.__getitem__(0)
            with open('temp.txt', 'w') as f:
                f.write(str(solved_grid))
            final_sudoku = import_data.from_minizinc_array.from_file(name='temp.txt', skip_header_rows=0)
            if stats:
                return final_sudoku, result
            else:
                return final_sudoku
        except:
            print("Problem occured while extracting Sudoku grid. Try again or use parameter 'stats' to get second return value. You can use data provided in stats to extract grid yourself.")
            if stats:
                return [], result
            else:
                return []
    else:
        return False
