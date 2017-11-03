import random_automata
import biosphere_automata
import user_interface

ROW_SIZE = 10
COL_SIZE = 10
DEFAULT_ROWS = 50
DEFAULT_COLS = 50
TICK_TIME = 200

# automaton = random_automata.RandomAutomata(DEFAULT_ROWS, DEFAULT_COLS)
automaton = biosphere_automata.BiosphereAutomata(DEFAULT_ROWS, DEFAULT_COLS)

ui = user_interface.Application(DEFAULT_ROWS, DEFAULT_COLS, ROW_SIZE, COL_SIZE,
                                automaton.get_num_of_states(), automaton, TICK_TIME)
ui.mainloop()
