import tkinter as tk
import random

GRID_WIDTH, GRID_HEIGHT, CELL_SIZE, DELAY = 10, 20, 30, 500

# ミノの定義
SHAPES = [
    [[1, 1, 1, 1]], 
    [[1, 1], [1, 1]], 
    [[0, 1, 1], [1, 1, 0]], 
    [[1, 1, 0], [0, 1, 1]], 
    [[1, 0, 0], [1, 1, 1]], 
    [[0, 0, 1], [1, 1, 1]], 
    [[0, 1, 0], [1, 1, 1]]
]
COLORS = ["cyan", "yellow", "green", "red", "blue", "orange", "purple"]

class Tetris(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tetris")
        self.canvas = tk.Canvas(self, width=GRID_WIDTH * CELL_SIZE, height=GRID_HEIGHT * CELL_SIZE)
        self.canvas.pack()
        self.bind("<KeyPress>", self.handle_keypress)
        self.init_game()

    def init_game(self):
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.current_block = self.new_block()
        self.game_over_flag = False
        self.after_id = self.after(DELAY, self.game_loop)

    def new_block(self):
        shape = random.choice(SHAPES)
        color = COLORS[SHAPES.index(shape)]
        return {"shape": shape, "color": color, "x": GRID_WIDTH // 2 - len(shape[0]) // 2, "y": 0}

    def draw_grid(self):
        self.canvas.delete("all")
        for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
            self.canvas.create_line(x, 0, x, GRID_HEIGHT * CELL_SIZE, fill="gray")
        for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
            self.canvas.create_line(0, y, GRID_WIDTH * CELL_SIZE, y, fill="gray")
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    self.canvas.create_rectangle(x * CELL_SIZE, y * CELL_SIZE,
                                                 x * CELL_SIZE + CELL_SIZE, y * CELL_SIZE + CELL_SIZE,
                                                 fill=self.grid[y][x], outline="black")
        for y, row in enumerate(self.current_block["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    self.canvas.create_rectangle((self.current_block["x"] + x) * CELL_SIZE,
                                                 (self.current_block["y"] + y) * CELL_SIZE,
                                                 (self.current_block["x"] + x) * CELL_SIZE + CELL_SIZE,
                                                 (self.current_block["y"] + y) * CELL_SIZE + CELL_SIZE,
                                                 fill=self.current_block["color"], outline="black")
        if self.game_over_flag:
            self.canvas.create_text(GRID_WIDTH * CELL_SIZE // 2, GRID_HEIGHT * CELL_SIZE // 2,
                                    text="Game Over", fill="red", font=("Helvetica", 24))

    def move_block(self, dx, dy):
        self.current_block["x"] += dx
        self.current_block["y"] += dy
        if not self.is_valid_position():
            self.current_block["x"] -= dx
            self.current_block["y"] -= dy
            return False
        return True

    def rotate_block(self):
        shape = self.current_block["shape"]
        rotated = list(zip(*shape[::-1]))
        self.current_block["shape"], old_shape = rotated, self.current_block["shape"]
        if not self.is_valid_position():
            self.current_block["shape"] = old_shape

    def is_valid_position(self):
        for y, row in enumerate(self.current_block["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    new_x, new_y = self.current_block["x"] + x, self.current_block["y"] + y
                    if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or self.grid[new_y][new_x]:
                        return False
        return True

    def freeze_block(self):
        for y, row in enumerate(self.current_block["shape"]):
            for x, cell in enumerate(row):
                if cell:
                    self.grid[self.current_block["y"] + y][self.current_block["x"] + x] = self.current_block["color"]
        if any(self.grid[0]):
            self.game_over_flag = True
        else:
            self.clear_lines()
            self.current_block = self.new_block()
            if not self.is_valid_position():
                self.game_over_flag = True

    def clear_lines(self):
        self.grid = [row for row in self.grid if any(cell == 0 for cell in row)]
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT - len(self.grid))] + self.grid

    def game_loop(self):
        if not self.game_over_flag:
            if not self.move_block(0, 1):
                self.freeze_block()
            self.draw_grid()
            self.after_id = self.after(DELAY, self.game_loop)
        else:
            self.draw_grid()
            self.after_cancel(self.after_id)

    def handle_keypress(self, event):
        if not self.game_over_flag:
            if event.keysym == "Left":
                self.move_block(-1, 0)
            elif event.keysym == "Right":
                self.move_block(1, 0)
            elif event.keysym == "Down":
                self.move_block(0, 1)
            elif event.keysym == "Up":
                self.rotate_block()
            self.draw_grid()

if __name__ == "__main__":
    Tetris().mainloop()
