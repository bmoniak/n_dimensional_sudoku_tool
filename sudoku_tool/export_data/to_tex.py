from sudoku_tool import Sudoku

def print_grid(sudoku: Sudoku):
    grid = ""
    grid += r"\begin{center}"+"\n"+r"\begin{tikzpicture}[scale=.5]"+"\n"+\
        r"\begin{scope}[black, font=\fontsize{8}{0}\sffamily\slshape]"+"\n"+\
        r"\draw (0, 0) grid ("+str(sudoku.m)+", "+str(sudoku.m)+");"+"\n"+\
        r"\draw[very thick, scale="+str(sudoku.n)+"] (0, 0) grid ("+\
        str(sudoku.n)+", "+str(sudoku.n)+");"+"\n"+\
        r"\draw[very thick, scale="+str(sudoku.n)+"] (0, 0) grid ("+\
            str(sudoku.n)+", "+str(sudoku.n)+");"+"\n"+\
        r"\def \sudokufontsize{6}"+"\n"+r"\setcounter{row}{1}"
    
    for i in range(sudoku.grid.shape[0]):
        grid += r"\setrow{"
        k = 1
        for j in range(sudoku.m):
            if k != sudoku.m:
                grid += str(sudoku.grid[i,j]) + ", "
            else:
                grid += str(sudoku.grid[i,j])
            k = k + 1
        grid += r"}{"+str(sudoku.m)+"}\n"
    grid += r"\node[anchor=center] at ("+str(sudoku.m/2)+r", -0.5){Sudoku};"+"\n"+\
    r"\end{scope}"+"\n"+r"\end{tikzpicture}"+"\n"+r"\end{center}"
    print(grid)

def save_grid(sudoku:Sudoku, name:str="sudoku.txt"):
    grid = ""
    grid += r"\begin{center}"+"\n"+r"\begin{tikzpicture}[scale=.5]"+"\n"+\
        r"\begin{scope}[black, font=\fontsize{8}{0}\sffamily\slshape]"+"\n"+\
        r"\draw (0, 0) grid ("+str(sudoku.m)+", "+str(sudoku.m)+");"+"\n"+\
        r"\draw[very thick, scale="+str(sudoku.n)+"] (0, 0) grid ("+\
        str(sudoku.n)+", "+str(sudoku.n)+");"+"\n"+\
        r"\draw[very thick, scale="+str(sudoku.n)+"] (0, 0) grid ("+\
            str(sudoku.n)+", "+str(sudoku.n)+");"+"\n"+\
        r"\def \sudokufontsize{6}"+"\n"+r"\setcounter{row}{1}"
    
    for i in range(sudoku.grid.shape[0]):
        grid += r"\setrow{"
        k = 1
        for j in range(sudoku.m):
            if k != sudoku.m:
                grid += str(sudoku.grid[i,j]) + ", "
            else:
                grid += str(sudoku.grid[i,j])
            k = k + 1
        grid += r"}{"+str(sudoku.m)+"}\n"
    grid += r"\node[anchor=center] at ("+str(sudoku.m/2)+r", -0.5){Sudoku};"+"\n"+\
    r"\end{scope}"+"\n"+r"\end{tikzpicture}"+"\n"+r"\end{center}"
    try:
        with open(name, "w") as text_file:
            text_file.write(grid)
        return True
    except:
        return False