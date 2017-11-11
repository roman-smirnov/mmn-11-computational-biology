""" a portable module for generating simple line/cluster/scatter/bar/pie plots """

################################################################################################
# IMPORTANT!!! NOT YET FULLY IMPLEMENTED!
################################################################################################

import tkinter as tk
from decimal import Decimal
from gui.color_generator import *


class Graph(tk.Frame):
    """
    Tkinter native graph (pretty basic, but doesn't require heavy install)
    Notes: the core of this object was creating using the
    basic structure found at: https://gist.github.com/ajbennieston/3072649
    """

    def __init__(self, x_max, y_max, x_tick, y_tick, x_min=0, y_min=0, height=500, width=500, parent=None):
        """
        Initializes the graph object.
        :param parent: the parent frame
        :param x_min: the x minimum
        :param x_max: the x maximum
        :param y_min: the y minimum
        :param y_max: the y maximum
        :param x_tick: the 'tick' on the x-axis
        :param y_tick: the 'tick' on the y-axis
        :param options: additional valid tkinter.canvas options
        """

        tk.Frame.__init__(self, parent, background='white')
        self.master.title("Graph")
        self.canvas = tk.Canvas(self, height=height, width=width)
        self.canvas.grid(row=0, column=0)

        self.w = float(self.canvas.config('width')[4])
        self.h = float(self.canvas.config('height')[4])
        self.x_min = x_min
        self.x_max = x_max
        self.x_tick = x_tick
        self.y_min = y_min
        self.y_max = y_max
        self.y_tick = y_tick
        self.px_x = (self.w - 100) / ((x_max - x_min) / x_tick)
        self.px_y = (self.h - 100) / ((y_max - y_min) / y_tick)

        self.draw_axes()

    def draw_axes(self):
        """
        Removes all existing series and re-draws the axes
        :return: None
        """
        self.canvas.delete('all')
        rect = 50, 50, self.w - 50, self.h - 50

        self.canvas.create_rectangle(rect, outline="black")

        for x in self.frange(0, self.x_max - self.x_min + 1, self.x_tick):
            value = Decimal(self.x_min + x)
            if self.x_min <= value <= self.x_max:
                x_step = (self.px_x * x) / self.x_tick
                coord = 50 + x_step, self.h - 50, 50 + x_step, self.h - 45
                self.canvas.create_line(coord, fill="black")
                coord = 50 + x_step, self.h - 40

                label = round(Decimal(self.x_min + x), 1)
                self.canvas.create_text(coord, fill="black", text=label)

        for y in self.frange(0, self.y_max - self.y_min + 1, self.y_tick):
            value = Decimal(self.y_max - y)

            if self.y_min <= value <= self.y_max:
                y_step = (self.px_y * y) / self.y_tick
                coord = 45, 50 + y_step, 50, 50 + y_step
                self.canvas.create_line(coord, fill="black")
                coord = 35, 50 + y_step

                label = round(value, 1)
                self.canvas.create_text(coord, fill="black", text=label)

    def plot_point(self, x, y, visible=True, color='black', size=10):
        """
        Places a single point on the grid
        :param x: the x coordinate
        :param y: the y coordinate
        :param visible: True if the individual point should be visible
        :param color: the color of the point
        :param size: the point size in pixels
        :return: The absolute coordinates as a tuple
        """
        xp = (self.px_x * (x - self.x_min)) / self.x_tick
        yp = (self.px_y * (self.y_max - y)) / self.y_tick
        coord = 50 + xp, 50 + yp

        if visible:
            # divide down to an appropriate size
            size = int(size / 2) if int(size / 2) > 1 else 1
            x, y = coord

            self.canvas.create_oval(
                x - size, y - size,
                x + size, y + size,
                fill=color
            )

        return coord

    def plot_line(self, points: list, color='black', point_visibility=False):
        """
        Plot a line of points
        :param points: a list of tuples, each tuple containing an (x, y) point
        :param color: the color of the line
        :param point_visibility: True if the points
        should be individually visible
        :return: None
        """
        last_point = ()
        for point in points:
            this_point = self.plot_point(point[0], point[1],
                                         color=color, visible=point_visibility)

            if last_point:
                self.canvas.create_line(last_point + this_point, fill=color)
            last_point = this_point
            # print last_point

    @staticmethod
    def frange(start, stop, step, digits_to_round=3):
        """
        Works like range for doubles
        :param start: starting value
        :param stop: ending value
        :param step: the increment
        :param digits_to_round: the digits to which to
        round (makes floating-point numbers much easier
        to work with)
        :return: generator
        """
        while start < stop:
            yield round(start, digits_to_round)
            start += step


def people_label(automaton):
    return "People at seed: %s" % automaton.gen_state_count[0][automaton.STATE_PERSON]


def size_label(automaton):
    return "Size: %sx%s" % (automaton.get_height(), automaton.get_width())


def esc_count_label(automaton):
    label_text = ""
    for exit_pos in automaton.exits:
        esc_count = sum(automaton.get_exit_esc_count()[exit_pos][g] for g in automaton.get_exit_esc_count()[exit_pos])
        label_text += "Total escaped at exit " + str(exit_pos) + " : " + str(esc_count) + " \n"
    return label_text


def generations_label(automaton):
    return "Number of generations: %s" % automaton.get_gen_count()


def description_label_text(automaton):
    return people_label(automaton) + "\n" + size_label(automaton) + "\n" + esc_count_label(
        automaton) + generations_label(automaton)


class ExitGraph(Graph):
    def __init__(self, automaton, height=700, width=700):
        self.automaton = automaton
        self.desc_str = description_label_text(automaton)

        # create a color dictionary for the plot
        num_of_exits = len(automaton.exits)
        color_list = generate_tk_colors(num_of_exits + 1)
        self.colors = {automaton.exits[i]: color_list[i + 1] for i in range(0, num_of_exits)}

        # calculate y axis range and value label interval
        y_max = automaton.get_num_of_people_at_seed()
        y_tick = round(y_max / (height / 30))  # 30 is approximate number of text pixel height
        # calculate x axis range and value label interval
        x_max = automaton.get_gen_count()
        x_tick = round(x_max / (width / 70))  # 70 is approximate number pixel width

        # init super
        Graph.__init__(self, x_max, y_max, x_tick, y_tick)
        self.master.title("Exit Graph")
        self.grid(row=0, column=0)

        self.draw_legend()
        self.draw_description()
        self.plot_exit_points()

    def draw_legend(self):
        for exit_pos in self.automaton.exits:
            legend_text = "Exit: " + str(exit_pos) + " Color: ■■■■■■■■■■■■"
            color_legend = tk.Label(self, text=legend_text, fg=self.colors[exit_pos], bg='white')
            color_legend.grid()

    def draw_description(self):
        desc_label = tk.Label(self, text=self.desc_str, fg="black", bg='white')
        desc_label.grid()

    def plot_exit_points(self):
        esc_gen_esc_dict = self.automaton.get_exit_esc_count()
        for exit_pos in self.automaton.exits:
            esc_ppl = 0
            point_list = []
            for g in range(0, self.automaton.get_gen_count()):
                if g in esc_gen_esc_dict[exit_pos]:
                    esc_ppl += esc_gen_esc_dict[exit_pos][g]
                point_list.append((g, esc_ppl))
            self.plot_line(point_list, color=self.colors[exit_pos])
