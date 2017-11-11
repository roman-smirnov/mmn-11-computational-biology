# Portable 2d cellular automata simulation with GUI (tkinter)
#
# Author:   Roman Smirnov
# Created:  4/11/2017

import sys  # used to get command line arguments
from automata.mmn11_automata import EmergencyEscapeAutomaton
from gui.square_grid_view import *
from gui.graph_view import *
from stats.mmn11_stats import *

# some global constants
ROW_SIZE = 10
COL_SIZE = 10
TICK_TIME = 5


def q2_0():
    """ visualizes an automaton with a 50x50 grid and roughly 50 people"""
    rows = 50
    cols = 50
    exits = [(0, 0), (49, 49)]
    # initialize the automaton
    automaton = EmergencyEscapeAutomaton(rows, cols, exits, ppl_interval=5)
    # create the visualization grid
    gui = SquareGridView(rows, cols, ROW_SIZE, COL_SIZE,
                         automaton.get_num_of_states(), automaton, TICK_TIME)
    gui.mainloop()

    # show statistics and graph plot
    graph = ExitGraph(automaton)
    graph.mainloop()


def q2_1():
    """ visualizes an automaton with a 50x50 grid and roughly 150 people"""
    rows = 50
    cols = 50
    exits = [(0, 0), (49, 49)]
    # initialize the automaton
    automaton = EmergencyEscapeAutomaton(rows, cols, exits, ppl_interval=3)
    # create the visualization grid
    gui = SquareGridView(rows, cols, ROW_SIZE, COL_SIZE,
                         automaton.get_num_of_states(), automaton, TICK_TIME)
    gui.mainloop()

    # show statistics and graph plot
    graph = ExitGraph(automaton)
    graph.mainloop()


def q2_2():
    """ visualizes an automaton with a 25x25 grid and roughly 50 people"""
    rows = 25
    cols = 25
    exits = [(0, 0), (24, 24)]
    # initialize the automaton
    automaton = EmergencyEscapeAutomaton(rows, cols, exits, ppl_interval=3)
    # create the visualization grid
    gui = SquareGridView(rows, cols, ROW_SIZE, COL_SIZE,
                         automaton.get_num_of_states(), automaton, TICK_TIME)
    gui.mainloop()

    # show statistics and graph plot
    graph = ExitGraph(automaton)
    graph.mainloop()


def q2_3():
    """ visualizes an automaton with a 25x25 grid and roughly 150 people"""
    rows = 25
    cols = 25
    exits = [(0, 0), (24, 24)]
    # initialize the automaton
    automaton = EmergencyEscapeAutomaton(rows, cols, exits, ppl_interval=2)
    # create the visualization grid
    gui = SquareGridView(rows, cols, ROW_SIZE, COL_SIZE,
                         automaton.get_num_of_states(), automaton, TICK_TIME)
    gui.mainloop()

    # show statistics and graph plot
    graph = ExitGraph(automaton)
    graph.mainloop()


def q2():
    """ runs the demonstrations as defined in mmn11 question 2"""
    q2_0()
    q2_1()
    q2_2()
    q2_3()


def run_stats_demo():
    """ generate some intertesting statistics - run without a GUI """
    demo_choice_bias()  # slight bias toward lower y,x exits on grid....
    demo_dist_modifier()
    demo_crowd_modifier()
    demo_exit_radius()


if __name__ == '__main__':
    if sys.argv[1] == "q2":
        q2()
    elif sys.argv[1] == "stats":
        run_stats_demo()
    else:
        print(" no such command ")
