import random


class GameLogic:
    def __init__(self, default_row_count, default_col_count, colors, max_moves, color_count):
        self.default_row_count = default_row_count
        self.default_col_count = default_col_count
        self.colors = colors
        self.max_moves = max_moves
        self.color_count = color_count
        self.main_field = [["0" for _ in range(self.default_col_count)] for _ in range(self.default_row_count)]
        self.moves = 0

    def reset_game(self):
        color_names = list(self.colors.keys())[:self.color_count]
        self.main_field = [[random.choice(color_names) for _ in range(self.default_col_count)] for _ in
                           range(self.default_row_count)]
        self.moves = 0

    def dfs(self, row, col, initial_color, new_color, visited):
        if (row, col) in visited:
            return
        visited.add((row, col))
        if self.main_field[row][col] != initial_color:
            return
        self.main_field[row][col] = new_color

        if row > 0:
            self.dfs(row - 1, col, initial_color, new_color, visited)
        if row < self.default_row_count - 1:
            self.dfs(row + 1, col, initial_color, new_color, visited)
        if col > 0:
            self.dfs(row, col - 1, initial_color, new_color, visited)
        if col < self.default_col_count - 1:
            self.dfs(row, col + 1, initial_color, new_color, visited)

    def check_win(self):
        first_color = self.main_field[0][0]
        return all(first_color == self.main_field[row][col] for row in range(self.default_row_count) for col in
                   range(self.default_col_count))
