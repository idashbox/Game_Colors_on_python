import tkinter as tk
from settings_form import SettingsForm
from game_logic import GameLogic
from PIL import Image, ImageTk


class ImageDialog(tk.Toplevel):
    def __init__(self, parent, title, image, message):
        super().__init__(parent)
        self.title(title)

        self.message_label = tk.Label(self, text=message)
        self.message_label.pack()

        self.image_label = tk.Label(self, image=image)
        self.image_label.image = image
        self.image_label.pack()

        self.ok_button = tk.Button(self, text="OK", command=self.destroy)
        self.ok_button.pack()


class MainForm(tk.Tk):
    def __init__(self):
        super().__init__()
        self.game_logic = GameLogic(10, 10, {
            'blue': (0, 0, 255),
            'green': (34, 139, 34),
            'yellow': (255, 255, 0),
            'brown': (178, 34, 34),
            'orange': (255, 140, 0),
            'purple': (148, 0, 211),
            'cyan': (0, 255, 255),
            'pink': (255, 20, 147),
            'dark_green': (0, 100, 53),
            'maroon': (128, 0, 0)
        }, 25, 6)

        self.color_buttons = None
        self.start_button = None
        self.moves_label = None
        self.button_frame = None
        self.canvas = None
        self.panel_main = None
        self.settings_form = None
        self.game_menu = None
        self.menu = None
        self.win_gif_path = "win.gif"
        self.lose_gif_path = "lose.gif"
        self.win_gif = None
        self.lose_gif = None
        self.load_gifs()

        self.title("Перекраска")
        self.create_menu()
        self.create_widgets()
        self.reset_game()
        self.adjust_window_size()

    def create_menu(self):
        self.menu = tk.Menu(self)
        self.config(menu=self.menu)
        self.game_menu = tk.Menu(self.menu, tearoff=0)
        self.game_menu.add_command(label="Settings", command=self.open_settings)
        self.menu.add_cascade(label="Menu", menu=self.game_menu)

    def open_settings(self):
        self.settings_form = SettingsForm(self, self.game_logic.default_row_count, self.game_logic.default_col_count,
                                          self.game_logic.max_moves, self.game_logic.color_count,
                                          self.apply_game_settings)

    def adjust_window_size(self):
        field_width = self.game_logic.default_col_count * 70
        field_height = self.game_logic.default_row_count * 70
        window_width = field_width + 600
        window_height = max(field_height + 100, 900)
        self.geometry(f'{window_width}x{window_height}+100+100')

    def apply_settings(self):
        self.game_logic.default_row_count = self.settings_form.row_var.get()
        self.game_logic.default_col_count = self.settings_form.col_var.get()
        self.game_logic.max_moves = self.settings_form.moves_var.get()
        self.game_logic.color_count = self.settings_form.colors_var.get()
        self.settings_form.destroy()
        self.reset_game()
        self.update_canvas_size()

    def reset_game(self):
        self.game_logic.reset_game()
        self.update_view()
        self.game_logic.moves = 0
        if hasattr(self, 'moves_label'):
            self.moves_label.config(text=f"Moves: {self.game_logic.moves}")
        self.update_table_colors()
        self.update_canvas_size()

    def start_game(self):
        self.game_logic.reset_game()
        self.update_view()

    def create_widgets(self):
        self.panel_main = tk.Frame(self)
        self.panel_main.grid(row=0, column=0, padx=10, pady=10)

        canvas_width = self.game_logic.default_col_count * 70
        canvas_height = self.game_logic.default_row_count * 70
        self.canvas = tk.Canvas(self.panel_main, bg="white", width=canvas_width, height=canvas_height)
        self.canvas.grid(row=0, column=0)

        self.moves_label = tk.Label(self.panel_main, text=f"Moves: {self.game_logic.moves}")
        self.moves_label.grid(row=0, column=2, pady=10)

        self.update_table_colors()

        self.create_color_buttons()
        self.create_start_button()

    def apply_game_settings(self):
        self.game_logic.default_row_count = self.settings_form.row_var.get()
        self.game_logic.default_col_count = self.settings_form.col_var.get()
        self.game_logic.max_moves = self.settings_form.moves_var.get()
        self.game_logic.color_count = self.settings_form.colors_var.get()
        self.update_color_buttons()
        self.create_start_button()
        self.settings_form.destroy()
        self.reset_game()

    def update_canvas_size(self):
        canvas_width = self.game_logic.default_col_count * 70
        canvas_height = self.game_logic.default_row_count * 70

        self.canvas.config(width=canvas_width, height=canvas_height)
        self.update_table_colors()

    def create_color_buttons(self):
        self.button_frame = tk.Frame(self.panel_main)
        self.button_frame.grid(row=0, column=1, padx=10)
        self.color_buttons = []
        color_count = 0
        for color_name in self.game_logic.colors:
            if color_count != self.game_logic.color_count:
                color = self.game_logic.colors[color_name]
                button_text = ""
                button_bg = f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
                button = tk.Button(self.button_frame, text=button_text, bg=button_bg,
                                   command=lambda c=color_name: self.change_color(c), width=10, height=3)
                button.grid(row=len(self.color_buttons), column=0, pady=5)
                self.color_buttons.append(button)
                color_count += 1

    def update_color_buttons(self):
        for button in self.color_buttons:
            button.destroy()
        self.create_color_buttons()

    def create_start_button(self):
        self.start_button = tk.Button(self.button_frame, text="Start", bg="gray", command=self.start_game)
        self.start_button.grid(row=len(self.color_buttons), column=0, pady=10)

    def update_table_colors(self):
        self.canvas.delete("all")
        for i in range(self.game_logic.default_row_count):
            for j in range(self.game_logic.default_col_count):
                color_name = self.game_logic.main_field[i][j]
                color = "#{:02x}{:02x}{:02x}".format(*self.game_logic.colors.get(color_name, (0, 0, 0)))
                x0, y0 = j * 70, i * 70
                x1, y1 = x0 + 70, y0 + 70
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")

    def change_color(self, color_index):
        initial_color = self.game_logic.main_field[0][0]
        visited = set()
        self.game_logic.dfs(0, 0, initial_color, color_index, visited)
        self.game_logic.moves += 1
        self.update_view()

    def update_view(self):
        self.update_table_colors()
        if self.game_logic.check_win():
            image_dialog = ImageDialog(self, "Победа", self.win_gif, "Поздравляем, вы выиграли!")
            self.start_game()
        elif self.game_logic.moves >= 25:
            image_dialog = ImageDialog(self, "Проигрыш", self.lose_gif, "К сожалению, вы проиграли :(")

            self.start_game()
        else:
            if self.moves_label:
                self.moves_label.config(text=f"Moves: {self.game_logic.moves}")
            self.update()

    def load_gifs(self):
        self.win_gif = Image.open(self.win_gif_path)
        self.win_gif = self.win_gif.resize((200, 200))
        self.win_gif = ImageTk.PhotoImage(self.win_gif)

        self.lose_gif = Image.open(self.lose_gif_path)
        self.lose_gif = self.lose_gif.resize((200, 200))
        self.lose_gif = ImageTk.PhotoImage(self.lose_gif)


if __name__ == "__main__":
    app = MainForm()
    app.mainloop()
