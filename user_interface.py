import tkinter as tk
import color_generator


class Application(tk.Frame):
    def __init__(self, rows, cols, row_size, col_size, num_of_states, world_state_obj,  update_time_interval):
        tk.Frame.__init__(self, None, background='#000000')  # set the frame background color
        self.master.title("Cellular Automata")  # set the ui window name
        self.grid()
        # generate as many colors as there are states
        self.app_rows = rows
        self.app_cols = cols
        self.app_row_size = row_size
        self.app_col_size = col_size
        self.colors = color_generator.generate_tk_colors(num_of_states)
        self.world_state = world_state_obj
        self.app_update_delay = update_time_interval  # screen update time interval
        # create the canvas on which to draw the grid and automata
        self.canvas = tk.Canvas(self, width=self.app_cols * self.app_col_size + 1,
                                height=self.app_rows * self.app_row_size + 1,
                                borderwidth=0, highlightthickness=0)
        self.canvas.grid(padx=5, pady=5)

        self.app_update()

    def app_draw_grid(self, x=10, y=10):
        """ draw a grid of the automata universe """
        width, height = (self.app_cols * self.app_col_size, self.app_rows * self.app_row_size)
        for i in range(x, width, x):
            self.canvas.create_line(i, 0, i, height)

        for i in range(x, height, y):
            self.canvas.create_line(0, i, width, i)

    def app_color_fill_cells(self):
        """ fill the grid cells with color """
        grid = self.world_state.get_grid()
        # iterate over the world grid and draw each cell with a color corresponding to its state
        for y in range(0, len(grid)):
            for x in range(0, len(grid[y])):
                x0, y0 = x * self.app_col_size, y * self.app_row_size  # rect top-left coords
                x1, y1 = (x + 1) * self.app_col_size, (y + 1) * self.app_row_size  # rect bottom-right coords
                self.canvas.create_rectangle(x0, y0, x1, y1, width=0, fill=self.colors[grid[y][x]])  # draw rect

    def app_draw_screen(self):
        """ delete the previous screen and redraw the grid and automata """
        self.canvas.delete("all")
        self.app_color_fill_cells()  # draw the automata world state
        # self.app_draw_grid()  # uncomment to draw grid lines

    def app_update(self):
        self.world_state.update_world_state()  # this call causes the automata to transition to the next generation
        self.app_draw_screen()  # draw current universe state on screen
        self.after(self.app_update_delay,
                   self.app_update)  # call update again after set amount of time (i.e this is the draw loop call)
