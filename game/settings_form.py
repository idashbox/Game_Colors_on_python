import tkinter as tk
from tkinter import ttk


class SettingsForm(tk.Toplevel):
    def __init__(self, parent, default_row_count, default_col_count, max_moves, color_count, apply_settings_callback):
        super().__init__(parent)
        self.title("Settings")

        ttk.Label(self, text="Rows (5-20):").grid(row=0, column=0)
        self.row_var = tk.IntVar(value=default_row_count)
        validate_row = self.register(lambda p: p.isdigit() and 5 <= int(p) <= 20)
        self.row_spinbox = ttk.Spinbox(self, from_=5, to=20, textvariable=self.row_var, validate="key",
                                       validatecommand=(validate_row, "%P"))
        self.row_spinbox.grid(row=0, column=1)

        ttk.Label(self, text="Columns (5-20):").grid(row=1, column=0)
        self.col_var = tk.IntVar(value=default_col_count)
        validate_col = self.register(lambda p: p.isdigit() and 5 <= int(p) <= 20)
        self.col_spinbox = ttk.Spinbox(self, from_=5, to=20, textvariable=self.col_var, validate="key",
                                       validatecommand=(validate_col, "%P"))
        self.col_spinbox.grid(row=1, column=1)

        ttk.Label(self, text="Moves (15-50):").grid(row=2, column=0)
        self.moves_var = tk.IntVar(value=max_moves)
        validate_moves = self.register(lambda p: p.isdigit() and 15 <= int(p) <= 50)
        self.moves_spinbox = ttk.Spinbox(self, from_=15, to=50, textvariable=self.moves_var,
                                         validate="key", validatecommand=(validate_moves, "%P"))
        self.moves_spinbox.grid(row=2, column=1)

        ttk.Label(self, text="Colors (5-10):").grid(row=3, column=0)
        self.colors_var = tk.IntVar(value=color_count)
        validate_colors = self.register(lambda p: p.isdigit() and 5 <= int(p) <= 10)
        self.colors_spinbox = ttk.Spinbox(self, from_=5, to=10, textvariable=self.colors_var,
                                          validate="key", validatecommand=(validate_colors, "%P"))
        self.colors_spinbox.grid(row=3, column=1)

        self.apply_button = ttk.Button(self, text="Apply", command=apply_settings_callback)
        self.apply_button.grid(row=4, column=0, columnspan=2)

