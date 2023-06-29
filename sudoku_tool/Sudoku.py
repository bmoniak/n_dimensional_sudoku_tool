# Author: Bartlomiej Moniak 2023
# Repository: https://github.com/bmoniak/n_dimensional_sudoku_tool
# Distributed under MIT License

import numpy as np
from itertools import chain

class Sudoku:

    def __init__(self, n:int = 3, arr:np.ndarray = np.zeros(1)):
        # initialization of Sudoku object either with default values or with n 
        # and grid array provided by the user. It holds variables such as grid,
        # N and M for a Sudoku instance. 
        if n > 1 and n < 256:
            self.n = n
            self.m = self.n**2
        else:
            raise Exception('Variable n has to be an integer greater than one \
                            and smaller than 255.')
        if arr.shape[0] == 1:
            self.grid = np.zeros((self.m,self.m), dtype = np.uint16)
        elif arr.shape[0] == arr.shape[1] == self.m:
            self.grid = arr.astype(np.uint16)
        else:
            raise Exception('Input Numpy ndarray with shape [n^2, n^2] is \
                            necessary to proceed.')
    
    def fill_with_values(self):
        # fill_with_values fills the whole Sudoku grid with default values that
        # meet Sudoku puzzle conditions. It can be used for Sudoku generation
        # or for testing purposes.
        if self.grid.shape[0] == self.grid.shape[1] == self.m:
            filler = [arr for arr in range(1,self.m+1)]
            for block in range(self.n):
                for row in range(self.n):
                    len_of_filler = len(self.grid[block*self.n+row,row*self.n+\
                                                  block:])
                    self.grid[block*self.n+row,row*self.n+block:] = \
                        filler[:len_of_filler]
                    self.grid[block*self.n+row,:row*self.n+block] = \
                        filler[len_of_filler:]
        else:
            raise Exception('Detected shape inconsistency of a numpy ndarray.')

    def get_used_nums(self, x: int, y: int):
        # get_used_nums returns all the numbers used in Sudoku grid for a given
        # cell. It checks the column, row and appropriate box looking for all
        # of the already used values.
        if self.grid.shape[0] < x or x < 0:
            raise Exception('Value of x should be between zero and M.')
        if self.grid.shape[1] < y or y < 0:
            raise Exception('Value of y should be between zero and M.')
        sum = list(self.grid[x,:]) + list(self.grid[:,y]) + \
        list(chain.from_iterable(self.grid[x//self.n:x//self.n+self.n,
                                        y//self.n:y//self.n+self.n].tolist()))
        result = set([val for val in sum if val != 0 and val != self.grid[x,y]])
        return result

    def get_possible_nums(self, x: int, y: int):
        # get_possible_nums returns the candidates list for a given cell
        # (available cells) with a usage of get_used_nums function.
        if self.grid.shape[0] < x or x < 0:
            raise Exception('Value of x should be between zero and M.')
        if self.grid.shape[1] < y or y < 0:
            raise Exception('Value of y should be between zero and M.')
        used_nums = self.get_used_nums(x, y)
        possible_nums = list([val for val in range(1,self.m+1) if val not in \
                              used_nums])
        return possible_nums
    
    def get_non_zero_cells(self):
        # get_non_zero_cells returns a list of coordinates of all cells 
        # that are not empty in a Sudoku grid.
        list_of_non_zero_cells = []
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if self.grid[x,y] > 0:
                    list_of_non_zero_cells.append([x,y])
        return list_of_non_zero_cells
    
    def count_zero_cells(self):
        # count_zero_cells evaluates and returns number of empty cells 
        # within the grid.
        cntr = 0
        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):
                if self.grid[x,y] < 1:
                    cntr += 1
        return cntr
        return np.count_nonzero(sudoku.grid==0)
    
    