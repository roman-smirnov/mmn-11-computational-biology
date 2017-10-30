import tkinter as tk
import random
import time
import threading
from itertools import compress


class Application(tk.Frame):
    def __init__(self, rows, columns, rowsize=10, colsize=10, tick=100, grid=False, func=None):
        tk.Frame.__init__(self, None, background='#000000')
        self.master.title("Cellular Automata")
        self.grid()

        self.app_grid = grid
        self.app_rows = rows
        self.app_cols = columns
        self.app_rowsize = rowsize
        self.app_colsize = colsize
        self.create_widgets()

        self.automata = []

        if func is not None:
            self.app_update_func = func
            self.app_update_tick = tick
            self.app_update()

    def create_widgets(self):
        self.canvas = tk.Canvas(self, width=self.app_cols * self.app_colsize + 1,
                                height=self.app_rows * self.app_rowsize + 1,
                                borderwidth=0, highlightthickness=0)
        self.canvas.grid(padx=5, pady=5)

        if self.app_grid:
            self.app_draw_grid()

    def app_draw_grid(self, x=10, y=10):
        width, height = (self.app_cols * self.app_colsize, self.app_rows * self.app_rowsize)
        for i in range(x, width, x):
            self.canvas.create_line(i, 0, i, height)

        for i in range(x, height, y):
            self.canvas.create_line(0, i, width, i)

    def iter_rectangle_coords(self, i):
        for j in range(self.app_cols):
            yield (j * self.app_colsize, i * self.app_rowsize,
                   (j + 1) * self.app_colsize, (i + 1) * self.app_rowsize)

    def clear_automata(self):
        for a in self.automata:
            self.canvas.delete(a)

        self.automata = []

    def app_draw_automata(self, iterable):
        self.clear_automata()
        for i, row in enumerate(iterable):
            for coords in compress(self.iter_rectangle_coords(i), row):
                self.automata.append(self.canvas.create_rectangle(*coords, width=0, fill='#000000'))

    def app_update(self):
        generations = self.app_update_func()
        self.app_draw_automata(generations)
        self.after(self.app_update_tick, self.app_update)


def gen():
    return ([random.randint(0, 1) for i in range(50)] for j in range(50))


# TODO formulate the engine according to an formal automata rules
app = Application(rows=50, columns=50, grid=True, func=gen)

app.mainloop()


