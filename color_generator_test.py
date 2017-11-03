import tkinter as tk
import color_generator as cg

# color generator test - displays a row of cells with the generated colors

NUM_OF_COLORS = 50


class TestApp(tk.Frame):
    def __init__(self, rowsize=20, colsize=20, tick=500):
        tk.Frame.__init__(self, None, background='#000000')
        self.master.title("Cellular Automata")
        self.colors = cg.generate_tk_colors(NUM_OF_COLORS)
        self.grid()
        self.app_rows = 1
        self.app_cols = 50
        self.app_row_size = rowsize
        self.app_col_size = colsize
        self.app_update_delay = tick
        self.canvas = tk.Canvas(self, width=self.app_cols * self.app_col_size + 1,
                                height=self.app_rows * self.app_row_size + 1,
                                borderwidth=0, highlightthickness=0)

        self.canvas.grid(padx=5, pady=5)

        self.app_draw_grid()
        self.app_draw_colors()

    def app_draw_grid(self, x=10, y=10):
        width, height = (self.app_cols * self.app_col_size, self.app_rows * self.app_row_size)
        for i in range(x, width, x):
            self.canvas.create_line(i, 0, i, height)

        for i in range(x, height, y):
            self.canvas.create_line(0, i, width, i)

    def app_draw_colors(self):
        for x in range(0, self.app_cols):
            pos = (0, x)
            x0, y0 = pos[1] * self.app_col_size, pos[0] * self.app_row_size
            x1, y1 = (pos[1] + 1) * self.app_col_size, (pos[0] + 1) * self.app_row_size
            self.canvas.create_rectangle(x0, y0, x1, y1, width=0, fill=self.colors[x % NUM_OF_COLORS])


test_app = TestApp()
test_app.mainloop()
