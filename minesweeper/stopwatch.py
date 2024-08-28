import tkinter as tk
from utilities import generate_time_string


class Stopwatch:
    def __init__(self, root):
        self.root = root

        # Initialize time
        self.seconds = 0

        # Create and pack the label to show the time
        self.time_label = tk.Label(root, text="00:00", font=("Arial", 48))
        self.time_label.pack(pady=20)

        self.paused = False

    def update_clock(self):
        # Calculate minutes and seconds
        if self.paused:
            return

        # Update the label with the new time
        self.time_label.config(text=generate_time_string(self.seconds))

        # Increment the time
        self.seconds += 1

        # Schedule this function to be called again after 1000 ms (1 second)
        self.root.after(1000, self.update_clock)

    def reset(self):
        self.seconds = 0
        self.time_label.config(text=generate_time_string(self.seconds))

    def get_time(self):
        return self.seconds

    def pause(self):
        if self.paused:
            self.paused = False
            self.update_clock()
        else:
            self.paused = True

    def stop(self):
        self.paused = True

    def start(self):
        self.paused = False
        self.update_clock()
