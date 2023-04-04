import tkinter as tk

class SudokuBoard:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku")
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.create_widgets()
    
    def create_widgets(self):
        self.canvas = tk.Canvas(self.master, width=450, height=450)
        self.canvas.pack()
        
        for i in range(10):
            width = 3 if i % 3 == 0 else 1
            self.canvas.create_line(i*50, 0, i*50, 450, width=width)
            self.canvas.create_line(0, i*50, 450, i*50, width=width)
        
        self.entries = []
        for row in range(9):
            row_entries = []
            for col in range(9):
                entry = tk.Entry(self.canvas, width=4, font=('Arial', 20), justify='center')
                x = col * 50 + 16
                y = row * 50 + 14
                self.canvas.create_window(x, y, window=entry, anchor='nw')
                row_entries.append(entry)
            self.entries.append(row_entries)
        
        solve_button = tk.Button(self.master, text="Solve", font=('Arial', 20), command=self.solve)
        solve_button.pack(pady=10)
    
    def solve(self):
        self.get_board_values()
        if self.is_valid_board():
            self.solve_board()
    
    def get_board_values(self):
        for row in range(9):
            for col in range(9):
                try:
                    value = int(self.entries[row][col].get())
                except ValueError:
                    value = 0
                self.board[row][col] = value
    
    def is_valid_board(self):
        # Check rows
        for row in range(9):
            row_values = [value for value in self.board[row] if value != 0]
            if len(row_values) != len(set(row_values)):
                print("Invalid row at row", row)
                return False
        
        # Check columns
        for col in range(9):
            col_values = [self.board[row][col] for row in range(9) if self.board[row][col] != 0]
            if len(col_values) != len(set(col_values)):
                print("Invalid column at col", col)
                return False
        
        # Check 3x3 blocks
        for i in range(0, 9, 3):
            for j in range(0, 9, 3):
                block_values = [self.board[row][col] for row in range(i, i+3) for col in range(j, j+3) if self.board[row][col] != 0]
                if len(block_values) != len(set(block_values)):
                    print("Invalid block at row", i, "col", j)
                    return False
        
        return True
    
    def solve_board(self):
        self.solve_helper(0, 0)
        self.update_board()
    
    def solve_helper(self, row, col):
        if row == 9:
            return True
        
        next_row = row if col < 8 else row + 1
        next_col = (col + 1) % 9
        
        if self.board[row][col] != 0:
            return self.solve_helper(next_row, next_col)
        
        for value in range(1, 10):
            if self.is_valid_move(row, col, value):
