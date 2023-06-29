from sudoku_tool import Sudoku
import numpy as np

def print_grid(sudoku:Sudoku):
    for i in sudoku.grid.astype(int):
        k = 1
        for j in i:
            if k != sudoku.m:
                print(j, end=" ")
            else:
                print(j)
            k = k + 1

def save_grid(sudoku:Sudoku, name:str="sudoku.txt"):
    try:
        np.savetxt(name, sudoku.sudoku, delimiter=" ",fmt="%i")
        return True
    except:
        return False
