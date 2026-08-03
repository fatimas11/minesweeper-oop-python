import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, r, board_size, b_c):
        self._size = board_size
        self._root = r
        self._board = Board(self._size, b_c)
        self._create_board()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, value):
        self._board = value

    def _place_flag(self,event):
        button = event.widget
        row, col = button.grid_info()["row"], button.grid_info()["column"]
        self._board.cells[row][col].put_flag(self._root)

    def _reveal(self,event):
        button = event.widget
        row, col = button.grid_info()["row"], button.grid_info()["column"]
        if self._board.cells[row][col].is_a_bomb:
            self._game_over()
        self._board.reveal_all_around(row, col, self._root)
        self._check_win()

    def _create_board(self):
        """Create a size x size board of buttons."""
        for row in range(self._size):
            for col in range(self._size):
                button = tk.Button(self._root, text="", width=5, height=2)
                button.grid(row=row, column=col, padx=2, pady=2)
                button.bind("<Button-1>", self._reveal)
                button.bind("<Button-3>", self._place_flag)

    def _game_over(self):
        for i in range(0,self._size):
            for j in range(0,self._size):
                if self._board.cells[i][j].is_a_bomb and not self._board.cells[i][j].is_revealed:
                    button = self._root.grid_slaves(row=i, column=j)[0]
                    button.config(text="💣", bg="#CC6666")
        messagebox.showinfo("Game Over", "You hit a bomb!")
        quit()

    def _check_win(self):
        for i in range(self._size):
            for j in range(self._size):
                cell = self._board.cells[i][j]
                if not cell.is_a_bomb and not cell.is_revealed:
                    return
        tk.messagebox.showinfo("Congratulations!", "You won the game!")
        quit()


class Board:
    def __init__(self, board_size, b_count):
        self._size = board_size
        self._bomb_count = b_count
        self._cells = [[Cell(0, i, j) for j in range(size)] for i in range(size)]  # Create a 2D list of cells
        self._place_mines()
        self._count_adjacent_bombs()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value


    @property
    def bomb_count(self):
        return self._bomb_count

    @bomb_count.setter
    def bomb_count(self, value):
        self._bomb_count = value


    @property
    def cells(self):
        return self._cells

    def _place_mines(self):
        mine_positions = set()
        while len(mine_positions) < self._bomb_count:
            r = random.randint(0, self._size - 1)
            c = random.randint(0, self._size - 1)
            if (r,c) not in mine_positions :
                mine_positions.add((r, c))
            else : continue
        for r, c in mine_positions:
            self._cells[r][c].is_a_bomb = True

    def _count_adjacent_bombs(self):
        for i in range (0,self._size):
            for j in range (0,self._size):
                if not self._cells[i][j].is_a_bomb:
                    paths = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,1),(1,0)]
                    for (x,y) in paths:
                        if 0 <= i + x < self._size and 0 <= j + y < self._size:
                            if self._cells[i+x][j+y].is_a_bomb:
                                self._cells[i][j].adjacent_mines += 1

    def reveal_all_around(self, row, col, root_r):
        if self._cells[row][col].is_revealed:
            return
        cell = self._cells[row][col]

        if cell.is_a_bomb:
            return

        if cell.adjacent_mines == 0:
            self._cells[row][col].is_revealed = True
            button = root_r.grid_slaves(row,col)[0]
            button.config(text="", bg="light gray")

            paths = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 1), (1, 0)]
            for (x, y) in paths:
                new_row, new_col = row + x, col + y
                if 0 <= new_row < self._size and 0 <= new_col < self._size:
                    self.reveal_all_around(new_row, new_col, root)

        else:
            self._cells[row][col].is_revealed = True
            button = root_r.grid_slaves(row, col)[0]
            button.config(text=str(cell.adjacent_mines), bg="light gray")


class Cell:
    def __init__(self, adjacent_mines, row, col):
        self._is_a_bomb = False
        self._is_revealed = False
        self._is_flagged = False
        self._row = row
        self._col = col
        self._adjacent_mines = adjacent_mines

    @property
    def is_a_bomb(self):
        return self._is_a_bomb

    @is_a_bomb.setter
    def is_a_bomb(self, value):
        self._is_a_bomb = value

    @property
    def is_revealed(self):
        return self._is_revealed

    @is_revealed.setter
    def is_revealed(self, value):
        self._is_revealed = value

    @property
    def is_flagged(self):
        return self._is_flagged

    @is_flagged.setter
    def is_flagged(self, value):
        self._is_flagged = value

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @property
    def adjacent_mines(self):
        return self._adjacent_mines

    @adjacent_mines.setter
    def adjacent_mines(self, value):
        self._adjacent_mines = value

    def put_flag(self, root_t):
        button = root_t.grid_slaves(self.row,self.col)[0]
        if self.is_revealed:
            return
        if not self.is_flagged:
            button.config(text="|>", bg="light blue")
            self.is_flagged = True
        else :
            button.config(text="", bg="SystemButtonFace")
            self.is_flagged = False

if __name__ == "__main__":

    size = int(input("Enter the size of the board: "))
    while size <= 1:
        size = int(input("Enter a valid size for the board! : "))

    bomb_count = int(input("Enter the number of bombs: "))
    while  bomb_count >= (size*size)/2 :
        bomb_count = int(input("Too much bombs , Enter a smaller number: "))
    while bomb_count <= 0:
        bomb_count = int(input("Enter a number that is > 0: "))

    root = tk.Tk()
    root.title("Minesweeper")

    minesweeper = Minesweeper(root,size,bomb_count)

    root.mainloop()
