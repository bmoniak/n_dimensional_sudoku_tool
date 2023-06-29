import numpy as np
from sudoku_tool import Sudoku

def from_file(name:str="sudoku.txt"):
    txtfile = np.loadtxt(name, delimiter=" ",dtype=np.uint16)
    if len(txtfile[0])==len(txtfile[1]) and \
        np.sqrt(len(txtfile[0])).is_integer():
        try:
            n = int(np.sqrt(len(txtfile[0])))
        except:
            raise Exception('Incorrect size of matrix. The width/length\
                             of a grid M should be N*N')
    else:
        raise Exception('Incorrect sudoku matrix. Please provide matrix\
                         with size M by M, where M == N*N and N > 1')
    sudoku_grid = Sudoku.Sudoku(n, txtfile)
    return sudoku_grid