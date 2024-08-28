import tkinter as tk
from tkinter.constants import DISABLED, NORMAL


class SingleSpace(tk.Button):
    def __init__(self, master=None, grid_manager=None, grid_position=(0,0), **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            relief=tk.FLAT,  # Remove button relief
            bd=5,  # Remove border
            highlightthickness=1,  # Remove highlight
            padx=10,  # Add horizontal padding
            pady=10,  # Add vertical padding
            text=" ",
            font=("Arial", 12),  # Set font
            foreground="black",  # Text color
            background="orange",  # Background color
        )

        self.bind("<Button-1>", self.on_left_down)
        self.bind("<ButtonRelease-1>", self.on_left_up)
        self.bind("<Button-3>", self.on_right_down)
        self.bind("<ButtonRelease-3>", self.on_right_up)
        self.left_activated = False
        self.right_activated = False

        self.grid_manager = grid_manager

        self.is_flagged = False
        self.is_revealed = False
        self.grid_position = grid_position
        self.space_value = ""
        self.game_over = False

    def handle_click(self):
        if self.left_activated and self.right_activated:
            print("DOUBLE CLICK")
            self.double_click()
        elif self.left_activated:
            print("LEFT CLICK")
            self.left_click()
        elif self.right_activated:
            print("RIGHT CLICK")
            self.right_click()

    def on_left_down(self, event):
        self.left_activated = True
        self.handle_click()

    def on_right_down(self, event):
        self.right_activated = True
        self.handle_click()

    def on_left_up(self, event):
        self.left_activated = False

    def on_right_up(self, event):
        self.right_activated = False

    def get_value(self):
        return self.space_value

    def set_value(self, space_value):
        if space_value == 0:
            self.space_value = " "
        else:
            self.space_value = space_value

    def left_click(self):
        if self.game_over or self.flagged() or self.revealed():
            return

        self.clear()
        self.grid_manager.update_board(self.grid_position)

    def right_click(self):
        if self.revealed() or self.game_over:
            return

        self.configure(state=DISABLED)

        if self.flagged():
            self.configure(text=" ")
            self.set_flagged(False)
            self.grid_manager.uptick_flags()
        else:
            self.configure(text="F")
            self.set_flagged(True)
            self.grid_manager.downtick_flags()

    def double_click(self):
        if not self.revealed() or self.game_over:
            return

        self.grid_manager.handle_double_click(self.grid_position)

    def flagged(self):
        return self.is_flagged

    def revealed(self):
        return self.is_revealed

    def set_flagged(self, flag_value=False):
        self.is_flagged = flag_value

    def wrong_flagged(self):
        self.configure(text="W")

    def clear(self):
        self.is_revealed = True

        self.configure(state=DISABLED)
        self.configure(background="white")
        self.configure(text=self.get_value())

    def end_game(self):
        self.configure(state=DISABLED)
        self.game_over = True

    def reset(self):
        self.configure(state=NORMAL)
        self.config(
            relief=tk.FLAT,  # Remove button relief
            bd=5,  # Remove border
            highlightthickness=1,  # Remove highlight
            padx=10,  # Add horizontal padding
            pady=10,  # Add vertical padding
            text=" ",
            font=("Arial", 12),  # Set font
            foreground="black",  # Text color
            background="orange",  # Background color
        )

        self.is_flagged = False
        self.is_revealed = False
        self.space_value = ""
        self.game_over = False
