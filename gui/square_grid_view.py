""" module for visually displaying an automaton """

import tkinter as tk  # requires tkinter (a Python standard GUI library) to display the visualization
from gui import color_generator  # requires the color generator to generate distinct colors for each automaton state


class SquareGridView(tk.Frame):
    """ this class is used to visually display and animate a square grid based cellular automaton """

    def __init__(self, rows, cols, row_size, col_size, num_of_states, world_state_obj, update_time_interval):
        """
            Display an animated visualization of a cellular automaton - call mainloop() after initialization to run
            :param rows: number of automaton grid rows
            :param cols: number of automaton grid columns
            :param row_size: pixel size of each row
            :param col_size: pixel size of each columns
            :param num_of_states: number of possible states in automaton
            :param world_state_obj: the automaton object - a subclass of BaseAutomaton
            :param update_time_interval: time (in milliseconds) between each cycle of update-state + redraw-screen

        """
        tk.Frame.__init__(self, None, background='#000000')  # set the frame background color
        self.master.title("Cellular Automata")  # set the ui window name
        self.grid()

        # generate as many colors as there are states
        self.app_rows = rows
        self.app_cols = cols
        self.app_row_size = row_size
        self.app_col_size = col_size
        self.colors = color_generator.generate_tk_colors(num_of_states)
        self.world_state = world_state_obj  # this object is used to get automaton grid and access automaton state
        self.app_update_delay = update_time_interval  # screen update time interval
        # create the canvas on which to draw the grid and automata
        self.canvas = tk.Canvas(self, width=self.app_cols * self.app_col_size + 1,
                                height=self.app_rows * self.app_row_size + 1,
                                borderwidth=0, highlightthickness=0)

        self.canvas.grid(padx=5, pady=5)
        # create a description label
        self.__draw_description__()
        self.__app_update__()

    def __draw_description__(self):
        description = "Size: %sx%s" % (self.app_rows, self.app_cols)
        desc_label = tk.Label(self, text=description, fg='white', bg='black')
        desc_label.grid()

    def __app_draw_grid__(self, x=10, y=10):
        """ draw a grid of the automata universe """
        width, height = (self.app_cols * self.app_col_size, self.app_rows * self.app_row_size)
        for i in range(x, width, x):
            self.canvas.create_line(i, 0, i, height, fill="#222222")

        for i in range(x, height, y):
            self.canvas.create_line(0, i, width, i, fill="#222222")

    def __app_color_fill_cells__(self):
        """ fill the grid cells with color """
        grid = self.world_state.get_grid()
        # iterate over the world grid and draw each cell with a color corresponding to its state
        for y in range(0, len(grid)):
            for x in range(0, len(grid[y])):
                x0, y0 = x * self.app_col_size, y * self.app_row_size  # rect top-left coords
                x1, y1 = (x + 1) * self.app_col_size, (y + 1) * self.app_row_size  # rect bottom-right coords
                self.canvas.create_rectangle(x0, y0, x1, y1, width=0, fill=self.colors[grid[y][x]])  # draw rect

    def __app_draw_screen__(self):
        """ delete the previous screen and redraw the grid and automata """
        self.canvas.delete("all")
        self.__app_color_fill_cells__()  # draw the automata world state
        self.__app_draw_grid__()  # draw the grid

    def __app_update__(self):
        self.world_state.update_world_state()  # this call causes the automata to transition to the next generation
        # check if automaton simulation has ended - terminate visualization if so
        if self.world_state.is_terminal():
            self.quit()
            self.destroy()
        else:
            self.__app_draw_screen__()  # draw current universe state on screen
            # call update again after set amount of time (i.e this is the draw loop call)
            self.after(self.app_update_delay, self.__app_update__)
