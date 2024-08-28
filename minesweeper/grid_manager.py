import random
import tkinter as tk
from single_space import SingleSpace
from utilities import generate_time_string


class GridManager:
    def __init__(self, root, size, flag_var, stopwatch):
        self.width = 0
        self.height = 0
        self.num_bombs = 0

        self.stopwatch = stopwatch

        print("SIZE")
        print(size)

        self.size = size

        self.set_dimensions(size)

        self.flag_var = flag_var
        self.flag_var.set(self.num_bombs)

        self.board = [[0] * self.width for _ in range(self.height)]

        self.directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        self.button_grid = None

        self.game_start = True

        self.root = root

        self.small_best_time = None
        self.medium_best_time = None
        self.large_best_time = None

    def set_dimensions(self, size):
        if size == "small":
            self.width = 10
            self.height = 8
            self.num_bombs = 10
        elif size == "medium":
            self.width = 18
            self.height = 14
            self.num_bombs = 40
        elif size == "large":
            self.width = 24
            self.height = 20
            self.num_bombs = 99

    def off_limits(self, start_x, start_y, x_pos, y_pos):
        off_limit_positions = [(start_x, start_y)]

        for x,y in self.directions:
            neighbor_x = start_x + x
            neighbor_y = start_y + y

            off_limit_positions.append((neighbor_x, neighbor_y))

        if (x_pos, y_pos) in off_limit_positions:
            return True

        return False

    def initialize_board(self, start_x, start_y):
        disallowed_spaces = []
        restart = False
        i = 0
        while i < self.num_bombs:
            x_pos = random.choice(range(self.width))
            y_pos = random.choice(range(self.height))

            # Maybe need some code to make sure we cant randomly get huge blocks of bombs?
            while (self.disallowed(x_pos, y_pos, disallowed_spaces) or self.is_bomb(x_pos, y_pos)
                   or self.off_limits(start_x, start_y, x_pos, y_pos)):
                disallowed_spaces.append((x_pos, y_pos))
                x_pos = random.choice(range(self.width))
                y_pos = random.choice(range(self.height))

                # in case we randomly generate an impossible board state
                if len(disallowed_spaces) + i >= self.width * self.height:
                    restart = True
                    break

            if restart:
                print("Restarting Building Board")
                restart = False
                i = 0
                disallowed_spaces = []
                self.board = [[0] * self.width for _ in range(self.height)]
            else:
                self.board[y_pos][x_pos] = 'B'
                i += 1

        for y_pos in range(self.height):
            for x_pos in range(self.width):
                if not self.is_bomb(x_pos, y_pos):
                    space_value = self.num_bomb_neighbors(x_pos, y_pos)
                    self.board[y_pos][x_pos] = space_value

                # Set the value of the button for display:
                self.button_grid[y_pos][x_pos].set_value(self.get_space_value(x_pos, y_pos))

        print(self.board)

    def disallowed(self, x_pos, y_pos, disallowed_spaces):
        if (x_pos, y_pos) in disallowed_spaces:
            return True

        return False

    def is_bomb(self, x_pos, y_pos):
        if self.get_space_value(x_pos, y_pos) == 'B':
            return True
        else:
            return False

    def num_bomb_neighbors(self, x_pos, y_pos):
        bomb_neighbors = 0

        for x,y in self.directions:
            neighbor_x = x_pos + x
            neighbor_y = y_pos + y

            if 0 <= neighbor_x < self.width and 0 <= neighbor_y < self.height:
                if self.is_bomb(neighbor_x, neighbor_y):
                    bomb_neighbors += 1

        return bomb_neighbors

    def get_board(self):
        return self.board

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def uptick_flags(self):
        self.flag_var.set(self.flag_var.get() + 1)

    def downtick_flags(self):
        self.flag_var.set(self.flag_var.get() - 1)

    def get_space_value(self, x_pos, y_pos):
        return self.board[y_pos][x_pos]

    def is_free_space(self, x_pos, y_pos):
        if self.get_space_value(x_pos, y_pos) == 0:
            return True
        else:
            return False

    def initialize_button_grid(self):
        button_grid = []
        for j in range(self.height):
            button_column = []
            for i in range(self.width):
                button = SingleSpace(self.root, self, (i, j))
                button.set_value(self.get_space_value(i, j))
                button.grid(row=j, column=i, padx=1, pady=1)
                button_column.append(button)
            button_grid.append(button_column)
        self.button_grid = button_grid

    def already_cleared(self, x_pos, y_pos):
        return self.button_grid[y_pos][x_pos].revealed()

    def clear_all_neighbors(self, x_pos, y_pos):
        for x,y in self.directions:
            neighbor_x = x_pos + x
            neighbor_y = y_pos + y

            if 0 <= neighbor_x < self.width and 0 <= neighbor_y < self.height:
                if self.is_free_space(neighbor_x, neighbor_y) and not self.already_cleared(neighbor_x, neighbor_y):
                    self.button_grid[neighbor_y][neighbor_x].clear()
                    self.clear_all_neighbors(neighbor_x, neighbor_y)
                else:
                    self.button_grid[neighbor_y][neighbor_x].clear()

    def is_winstate(self):
        for y_pos in range(self.height):
            for x_pos in range(self.width):
                if not self.is_bomb(x_pos, y_pos):
                    if not self.button_grid[y_pos][x_pos].revealed():
                        return False
        return True

    def turn_off_buttons(self):
        for y_pos in range(self.height):
            for x_pos in range(self.width):
                self.button_grid[y_pos][x_pos].end_game()

    def is_flagged(self, x_pos, y_pos):
        return self.button_grid[y_pos][x_pos].flagged()

    def display_all_bombs(self):
        for y_pos in range(self.height):
            for x_pos in range(self.width):
                if self.is_bomb(x_pos, y_pos) and not self.is_flagged(x_pos, y_pos):
                    self.button_grid[y_pos][x_pos].clear()
                elif self.is_flagged(x_pos, y_pos) and not self.is_bomb(x_pos, y_pos):
                    # The user erroneously marked this space as a bomb, so showing them there error
                    self.button_grid[y_pos][x_pos].wrong_flagged()

    def game_loss(self):
        self.stopwatch.pause()
        print("YOU LOSE!!!!!")
        self.turn_off_buttons()

        text_label = tk.Label(self.root, text="YOU LOSE!!!!", font=("Arial", 20, "bold"))
        # Place the label above the grid
        text_label.grid(row=0, column=0, columnspan=10, pady=(10, 0))

        self.display_all_bombs()

        action_button = tk.Button(self.root, text="Play Again", command=self.reset_board)
        action_button.grid(row=1, column=0, columnspan=10, pady=(10, 0))

        return

    def game_win(self):
        self.stopwatch.pause()
        completion_time = self.stopwatch.get_time()
        self.update_best_time(completion_time)
        print("YOU WON!!!!!")
        self.turn_off_buttons()

        best_time = self.get_best_time()

        text_label = tk.Label(self.root, text="YOU WON!!!!", font=("Arial", 20, "bold"))
        # Place the label above the grid
        text_label.grid(row=0, column=0, columnspan=10, pady=(10, 0))

        second_label = tk.Label(self.root, text="Completion Time: {}".format(generate_time_string(completion_time)), font=("Arial", 16))
        second_label.grid(row=1, column=0, columnspan=10, pady=(10, 0))

        third_label = tk.Label(self.root, text="Best Time: {}".format(generate_time_string(best_time)), font=("Arial", 16))
        third_label.grid(row=2, column=0, columnspan=10, pady=(10, 0))

        action_button = tk.Button(self.root, text="Play Again", command=self.reset_board)
        action_button.grid(row=3, column=0, columnspan=10, pady=(10, 0))

        return

    def get_best_time(self):
        if self.size == "small":
            return self.small_best_time
        elif self.size == "medium":
            return self.medium_best_time
        elif self.size == "large":
            return self.large_best_time

    def update_best_time(self, new_time):
        if self.size == "small":
            if self.small_best_time:
                if new_time < self.small_best_time:
                    self.small_best_time = new_time
            else:
                self.small_best_time = new_time
        elif self.size == "medium":
            if self.medium_best_time:
                if new_time < self.medium_best_time:
                    self.medium_best_time = new_time
            else:
                self.medium_best_time = new_time
        elif self.size == "large":
            if self.large_best_time:
                if new_time < self.large_best_time:
                    self.large_best_time = new_time
            else:
                self.large_best_time = new_time

    def reset_board(self):
        print("WE RESETTIN")
        self.stopwatch.stop()
        self.stopwatch.reset()
        # RESET HOW BUTTONS LOOK:
        for y_pos in range(self.height):
            for x_pos in range(self.width):
                self.button_grid[y_pos][x_pos].reset()

        self.board = [[0] * self.width for _ in range(self.height)]
        self.game_start = True
        self.flag_var.set(self.num_bombs)

        # Remove all end of game messages:
        for widget in self.root.winfo_children():
            if not isinstance(widget, SingleSpace):
                widget.destroy()

    def resize_and_reset(self, size):
        self.stopwatch.stop()
        self.stopwatch.reset()
        self.set_dimensions(size)
        for widget in self.root.winfo_children():
            widget.destroy()
        self.board = [[0] * self.width for _ in range(self.height)]
        self.initialize_button_grid()
        self.game_start = True
        self.flag_var.set(self.num_bombs)

    def get_adjacent_flags(self, x_pos, y_pos):
        adjacent_flags = 0

        for x, y in self.directions:
            neighbor_x = x_pos + x
            neighbor_y = y_pos + y

            if 0 <= neighbor_x < self.width and 0 <= neighbor_y < self.height:
                if self.is_flagged(neighbor_x, neighbor_y):
                    adjacent_flags += 1

        return adjacent_flags

    def handle_double_click(self, grid_position):
        # FIXME: seems to be a bug here, edge case near sides of board
        x_pos = grid_position[0]
        y_pos = grid_position[1]

        # only works if its bordered by the correct amount of flags
        adjacent_flags = self.get_adjacent_flags(x_pos, y_pos)
        if adjacent_flags != self.get_space_value(x_pos, y_pos):
            return

        for x, y in self.directions:
            neighbor_x = x_pos + x
            neighbor_y = y_pos + y

            if 0 <= neighbor_x < self.width and 0 <= neighbor_y < self.height:
                if not self.is_flagged(neighbor_x, neighbor_y)  and not self.already_cleared(neighbor_x, neighbor_y):
                    if self.is_free_space(neighbor_x, neighbor_y):
                        self.clear_all_neighbors(neighbor_x, neighbor_y)
                    elif self.is_bomb(neighbor_x, neighbor_y):
                        self.game_loss()
                    else:
                        self.button_grid[neighbor_y][neighbor_x].clear()

        if self.is_winstate():
            self.game_win()

    def update_board(self, grid_position):
        print(grid_position)
        x_pos = grid_position[0]
        y_pos = grid_position[1]

        # Initialiizes the board on first click
        if self.game_start:
            self.stopwatch.start()
            self.game_start = False
            self.initialize_board(x_pos, y_pos)

        if self.is_bomb(x_pos, y_pos):
            self.game_loss()

        if self.is_free_space(x_pos, y_pos):
            self.clear_all_neighbors(x_pos, y_pos)

        if self.is_winstate():
            self.game_win()

        return