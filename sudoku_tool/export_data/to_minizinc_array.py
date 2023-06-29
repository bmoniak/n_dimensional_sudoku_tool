from sudoku_tool import Sudoku

def print_grid(sudoku: Sudoku):
    print("[", end="")
    for i in sudoku.grid.astype(int):
        k = 1
        print("| ", end="")
        for j in i:
            if k != sudoku.m:
                print(j, end=", ")
            else:
                print(j)
            k = k + 1
    print("|]")

def save_grid(sudoku:Sudoku, name:str="sudoku.txt"):
    grid = ""
    grid += "["
    for i in sudoku.grid.astype(int):
        k = 1
        grid += "| "
        for j in i:
            if k != sudoku.m:
                grid += str(j) + ", "
            else:
                grid += str(j) + "\n"
            k = k + 1
    grid += "|]"
    try:
        with open(name, "w") as text_file:
            text_file.write(grid)
        return True
    except:
        return False