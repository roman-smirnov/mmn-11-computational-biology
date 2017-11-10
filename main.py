# Portable 2d cellular automata simulation with GUI (tkinter)
#
# Author:   Roman Smirnov
# Created:  4/11/2017

import sys  # used to get command line arguments
from automata.mmn11_automata import *
from gui.square_grid_view import *
from stats.stats_runner import *


# TODO: implement a command line main method
# TODO: implement show exit area
# TODO: go over entire project and check documentation


def run_gui_demo():
    DEFAULT_ROWS = 25
    DEFAULT_COLS = 25
    ROW_SIZE = 10
    COL_SIZE = 10
    TICK_TIME = 10
    EMERGENCY_EXITS = [(0, 0), (24, 24)]
    automaton = EmergencyEscapeAutomaton(DEFAULT_ROWS, DEFAULT_COLS, EMERGENCY_EXITS, ppl_interval=2)  # run with ui
    gui = SquareGridView(DEFAULT_ROWS, DEFAULT_COLS, ROW_SIZE, COL_SIZE,
                         automaton.get_num_of_states(), automaton, TICK_TIME)
    gui.mainloop()
    automaton.print_stats()


def run_stats_demo():
    demo_choice_bias()  # slight bias toward lower y,x exits on grid....

    demo_dist_modifier()

    demo_crowd_modifier()

    demo_exit_radius()

    demo_people_density()


if __name__ == '__main__':
    print(sys.argv)
