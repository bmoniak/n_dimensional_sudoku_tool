import numpy as np
from sudoku_tool import Sudoku
import re
import os

def from_file(name:str="sudoku.txt",
              skip_header_rows:int=0,
              skip_footer_rows:int=0,
              delete_last_columns:int=0):
    string = open(name).read()
    new_str = re.sub('[^0-9\n\s\.\,]', ' ', string)
    open('temp.txt', 'w').write(new_str)
    arr = np.genfromtxt('temp.txt',
                        skip_header=skip_header_rows,
                        delimiter=",",
                        deletechars="||[] ",
                        skip_footer=skip_footer_rows,
                        dtype=np.uint16,
                        encoding=None)
    os.remove('temp.txt')
    if(delete_last_columns>0):
        arr = np.delete(arr, -delete_last_columns, axis=1)
    if len(arr[0])==len(arr[1]) and \
        np.sqrt(len(arr[0])).is_integer():
        try:
            n = int(np.sqrt(len(arr[0])))
        except:
            raise Exception('Incorrect size of matrix. The width/length \
                            of a grid M should be N*N')
    else:
        raise Exception('Incorrect sudoku matrix. Please provide matrix \
                        with size M by M, where M == N*N and N > 1')
    sudoku_grid = Sudoku.Sudoku(n, arr)
    return sudoku_grid