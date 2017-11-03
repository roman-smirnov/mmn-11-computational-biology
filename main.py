# pyca.animation
# Wraps matplotlib to provide animation
#
# Author:   Benjamin Bengfort <benjamin@bengfort.com>
# Created:  Fri Jan 31 09:41:31 2014 -0500
#
# Copyright (C) 2014 Bengfort.com
# For license information, see LICENSE.txt
#
# ID: animation.py [] benjamin@bengfort.com $

from automata.food_chain_automata import FoodChainAutomaton
from automata.random_automata import RandomAutomaton
from gui.square_grid_gui import SquareGridApp


ROW_SIZE = 10
COL_SIZE = 10
DEFAULT_ROWS = 50
DEFAULT_COLS = 50
TICK_TIME = 200

# TODO: implemented the escape automata
# TODO: see if you can do something off ui thread
# TODO: implement a command line main method
automaton = RandomAutomaton(DEFAULT_ROWS, DEFAULT_COLS)
# automaton = FoodChainAutomaton(DEFAULT_ROWS, DEFAULT_COLS)

gui_app = SquareGridApp(DEFAULT_ROWS, DEFAULT_COLS, ROW_SIZE, COL_SIZE,
                        automaton.get_num_of_states(), automaton, TICK_TIME)
gui_app.mainloop()
