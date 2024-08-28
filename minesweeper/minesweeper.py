import tkinter as tk
from grid_manager import GridManager
from stopwatch import Stopwatch


# TODO:
#if you misflagged something show you what you misflagged

# different numbers different colors

# function that validates the board to make sure its correct

def run():
    root = tk.Tk()

    root.title("Minesweeper")

    OPTIONS = [
        "small",
        "medium",
        "large"
    ]

    board_size = tk.StringVar(root)
    board_size.set(OPTIONS[1])  # default value

    flag_var = tk.IntVar()

    stopwatch = Stopwatch(root)

    grid_frame = tk.Frame(root)
    test_grid = GridManager(grid_frame, board_size.get(), flag_var, stopwatch)

    w = tk.OptionMenu(root, board_size, *OPTIONS)
    w.pack()

    num_flag_display = tk.Label(root, text="# Flags: {}".format(flag_var.get()), font=("Arial", 10))
    num_flag_display.pack()

    grid_frame.pack()

    test_grid.initialize_button_grid()

    board_size.trace("w", lambda *args: on_option_change(board_size, test_grid))
    flag_var.trace("w", lambda *args: update_flag_display(flag_var, num_flag_display))

    root.mainloop()

def on_option_change(var, myGrid, *args):
    myGrid.resize_and_reset(var.get())

def update_flag_display(var, text_label, *args):
    new_value = var.get()
    text_label.config(text="# Flags: {}".format(new_value))

run()
