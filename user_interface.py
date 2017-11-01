
class Application(tk.Frame):
    def __init__(self, rowsize=10, colsize=10, tick=100, universe=Universe()):
        tk.Frame.__init__(self, None, background='#000000')
        self.master.title("Cellular Automata")
        self.grid()

        self.universe = universe

        self.app_rows = universe.get_height()
        self.app_cols = universe.get_width()
        self.app_row_size = rowsize
        self.app_col_size = colsize
        self.app_update_delay = tick
        self.canvas = tk.Canvas(self, width=self.app_cols * self.app_col_size + 1,
                                height=self.app_rows * self.app_row_size + 1,
                                borderwidth=0, highlightthickness=0)

        self.canvas.grid(padx=5, pady=5)
        self.app_update()

    def app_draw_grid(self, x=10, y=10):
        width, height = (self.app_cols * self.app_col_size, self.app_rows * self.app_row_size)
        for i in range(x, width, x):
            self.canvas.create_line(i, 0, i, height)

        for i in range(x, height, y):
            self.canvas.create_line(0, i, width, i)

    def app_draw_automata(self):
        grid = self.universe.get_grid()
        for pos in grid.get_all_positions():
            if grid.get_state(pos) == STATE_TAKEN:
                x0, y0 = pos[1] * self.app_col_size, pos[0] * self.app_row_size
                x1, y1 = (pos[1] + 1) * self.app_col_size, (pos[0] + 1) * self.app_row_size
                self.canvas.create_rectangle(x0, y0, x1, y1, width=0, fill='#000000')

    def app_draw_screen(self):
        self.canvas.delete("all")
        self.app_draw_grid()
        self.app_draw_automata()

    def app_update(self):
        self.universe.time_tick()
        self.app_draw_screen()
        self.after(self.app_update_delay, self.app_update)  # call the update functions after set amount of time
