# Author: Bartlomiej Moniak 2023
# Repository: https://github.com/bmoniak/n_dimensional_sudoku_tool
# Distributed under MIT License

import random
from sudoku_tool import *
from sudoku_tool.Sudoku import *
from sudoku_tool.solvers import *
from sudoku_tool.export_data import *

def generate_grid(sudoku:Sudoku, 
                    fill_with_initial_values:bool = True,
                    shuffle:int = 20, 
                    num_of_iterations_candidates_list_deletion: int = 1,
                    num_of_iterations_random: int = 1,
                    num_of_deleted_cells_per_iteration_rand: int = 1,
                    min_number_of_clues:int = 0,
                    print_intermediate:bool = False,
                    print_final:bool = False,
                    return_original:bool = False,
                    solver_name:str = "gecode",
                    timeout_seconds_per_check:int = 1000):
    if fill_with_initial_values:
        sudoku.fill_with_values()
    sudoku_grid_input = Sudoku(sudoku.n, sudoku.grid.copy())
    if shuffle < 0:
        raise Exception("Shuffle cannot be smaller than zero.")
    if min_number_of_clues > sudoku.m**2 or min_number_of_clues < 0:
        raise Exception("Min need to be an integer between 0 and M^2.")
    shuffle_random_rows(sudoku, shuffle)
    shuffle_random_groups(sudoku, shuffle)
    shuffle_random_rows(sudoku, shuffle)
    shuffle_random_groups(sudoku, shuffle)
    if num_of_iterations_candidates_list_deletion >= 0:
        best_sudoku = Sudoku(sudoku.n, sudoku.grid.copy())
    else:
        raise Exception("num_of_iterations_candidates_list_deletion has to be \
                        greater than zero or zero to disable the function.")
    if num_of_iterations_candidates_list_deletion > 0:
        for i in range(num_of_iterations_candidates_list_deletion):
            clear_cells_based_on_candidates_lists(sudoku, 
                                                limit = min_number_of_clues, 
                                                print_stats=print_intermediate)
            if sudoku.count_zero_cells() > best_sudoku.count_zero_cells():
                best_sudoku = Sudoku(sudoku.n, sudoku.grid.copy())
        sudoku = best_sudoku
        if print_final:
            print("Final solution after logical deletions: ")
            export_data.divided_by_spaces.print_grid(sudoku)

    if num_of_iterations_random >= 0:
        best_sudoku = Sudoku(sudoku.n, sudoku.grid.copy())
    else:
        raise Exception("num_of_iterations_random has to be greater than zero \
                        or zero to disable the function.")
    if num_of_iterations_random > 0:
        for i in range(num_of_iterations_random):
            clear_rand_cells(sudoku, 
                                limit = min_number_of_clues, 
                                print_stats = print_intermediate, 
                                solver_name = solver_name,
                                cells_to_delete = \
                                    num_of_deleted_cells_per_iteration_rand,
                                timeout_sec=timeout_seconds_per_check)
            if sudoku.count_zero_cells() > best_sudoku.count_zero_cells():
                best_sudoku = Sudoku(sudoku.n, sudoku.grid.copy())
        sudoku = best_sudoku
        if print_final:
            print("Final solution after random deletions: ")
            export_data.divided_by_spaces.print_grid(sudoku)
    if return_original:
        return sudoku, sudoku_grid_input
    else:
        return sudoku

def shuffle_random_rows(sudoku:Sudoku,
                        num_of_shuffles:int, 
                        x_shuffle = True, 
                        y_shuffle = True):
    if num_of_shuffles < 1:
        raise Exception('Number of shuffles should be an integer with a value \
                        of 1 or more.')
    if not(x_shuffle) and not(y_shuffle):
        raise Exception('Shuffling of both rows and columns was disabled!')
    for i in range(num_of_shuffles):
        randGroup = random.randrange(0,sudoku.n)
        if (x_shuffle and y_shuffle):
            randShuffle = random.randrange(3)
        elif x_shuffle:
            randShuffle = 0
        else:
            randShuffle = 2
        z=range(sudoku.n)
        finalRows = list(map(lambda x:x+sudoku.n*randGroup, z))    
        if x_shuffle and randShuffle <= 1:
            x = finalRows.copy()
            random.shuffle(x)
            # row
            sudoku.grid[finalRows,:] = sudoku.grid[x,:]
        if y_shuffle and randShuffle >= 1:
            y = finalRows.copy()
            random.shuffle(y)
            # column
            sudoku.grid[:,finalRows] = sudoku.grid[:,y]


def shuffle_random_groups(sudoku:Sudoku,
                            num_of_shuffles:int, 
                            x_shuffle = True, 
                            y_shuffle = True):
    if num_of_shuffles < 1:
        raise Exception('Number of shuffles should be an integer with a value \
                        of 1 or more.')
    if not(x_shuffle) and not(y_shuffle):
        raise Exception('Shuffling of both rows and columns was disabled!')
    for i in range(num_of_shuffles):
        randGroup = random.randrange(sudoku.n) #number 0-n
        if (x_shuffle and y_shuffle):
            randShuffle = random.randrange(3)
        elif x_shuffle:
            randShuffle = 0
        else:
            randShuffle = 2
        fullRange = list(range(sudoku.m)) #list of numbers 0-m
        x = list(range(sudoku.n)) #list of numbers 0-n
        y = x.copy()
        random.shuffle(x)
        random.shuffle(y)
        final_x = []
        final_y = []
        for i in range(sudoku.n):
            final_x = final_x+list(range(x[i]*sudoku.n,x[i]*sudoku.n+sudoku.n))
            final_y = final_y+list(range(y[i]*sudoku.n,y[i]*sudoku.n+sudoku.n))
        if x_shuffle and randShuffle <= 1:
            # row
            sudoku.grid[fullRange,:] = sudoku.grid[final_x,:]
        if y_shuffle and randShuffle >= 1:
            # column
            sudoku.grid[:,fullRange] = sudoku.grid[:,final_y]


def clear_cells_based_on_candidates_lists(sudoku: Sudoku,
                                          limit:int=0, 
                                          print_stats:bool=False):
    if limit < 0 or limit > sudoku.m**2:
        raise Exception('Limit should be an integer - between 0 and M*M as a \
                        minimum number of clues.')
    temp_counter = sudoku.m**2 - sudoku.count_zero_cells()
    cells_to_check = sudoku.get_non_zero_cells()
    random.shuffle(cells_to_check)
    for cell in cells_to_check:
        if len(sudoku.get_possible_nums(cell[0],cell[1])) == 1:
            sudoku.grid[cell[0],cell[1]] = 0
            temp_counter -= 1
        if temp_counter <= limit :
            break
    if print_stats:
        print("Number of empty cells after clearing logical values: "+\
              str(sudoku.count_zero_cells())+"/"+str(sudoku.m**2))


def clear_rand_cells(sudoku: Sudoku,
                     limit:int=0, 
                     print_stats:bool=False, 
                     solver_name:str = "gecode", 
                     cells_to_delete: int = 1,
                     timeout_sec:int = 1000):
    if limit < 0 or limit > sudoku.m**2:
        raise Exception('Limit should be an integer - between 0 and M*M as a \
                        minimum number of clues.')
    sudoku_backup = Sudoku(sudoku.n, sudoku.grid.copy())
    cells_to_check = sudoku.get_non_zero_cells()
    random.shuffle(cells_to_check)
    temp_cell_counter = sudoku.m**2 - sudoku.count_zero_cells()
    while len(cells_to_check) > 0 and sudoku.m**2 - temp_cell_counter \
        > limit:
        if sudoku.m**2 - temp_cell_counter < limit + cells_to_delete:
            temp_limit = temp_cell_counter - limit
        else:
            temp_limit = cells_to_delete
        if temp_limit > len(cells_to_check):
            temp_limit = len(cells_to_check)
        temp_cells = random.sample(cells_to_check,temp_limit)
        for cell in temp_cells:
            sudoku.grid[cell[0],cell[1]] = 0
        temp_cell_counter -= temp_limit
        if solver_minizinc.check_if_unique(sudoku, solver_name,
                                           timeout_seconds=timeout_sec)==False:
            for cell in temp_cells: 
                sudoku.grid[cell[0],cell[1]] = \
                    sudoku_backup.grid[cell[0],cell[1]]
            temp_cell_counter += temp_limit
        for cell in temp_cells:
                cells_to_check.remove(cell)

    if print_stats:
        print("Number of empty cells after with verification of uniqueness: "+\
              str(sudoku.count_zero_cells())+"/"+str(sudoku.m**2))
