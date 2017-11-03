""" this module holds an implementation of a simple example stochastic automaton """

import random

from automata import base_automata

# module constants
STATE_TAKEN = 1
STATE_EMPTY = 0
NUM_OF_STATES = 2
RADIUS = 1


class RandomAutomaton(base_automata.BaseAutomaton):
    """ this class implements a simple automaton with 2 states per cell, the cells randomly move to adjacent cells """

    def __init__(self, height, width):
        base_automata.BaseAutomaton.__init__(self, height, width, RADIUS, NUM_OF_STATES)

    def rand_seed(self):
        """
            Stochasticly generates a seed state grid
            Every third grid cell will get a random state out of possible states - all other cells will set to state 0
        """
        seed_grid = []
        for y in range(0, self.height):
            seed_grid.append([])
            for x in range(0, self.width):
                # generate a random state in every third row,column cell - all others will be left at state 0
                state = random.randint(0, self.num_of_states-1) if (x % 3, y % 3) == (0, 0) else STATE_EMPTY
                seed_grid[y].append(state)
        return seed_grid

    def empty_seed(self):
        """ generate an empty state grid (i.e the state is 0 for each cell) """
        empty_grid = []
        for y in range(0, self.height):
            empty_grid.append([])
            for x in range(0, self.width):
                empty_grid[y].append(STATE_EMPTY)
        return empty_grid

    def rand_gen_trans(self):
        """ stochasticly transition to next the generation of the automaton """
        new_grid = self.empty_seed()
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.grid[y][x] == STATE_EMPTY:
                    continue
                else:
                    neighbors = self.__get_neighbors_at__((y, x))
                    new_y, new_x = random.choice(neighbors)
                    if self.grid[new_y][new_x] == STATE_EMPTY and new_grid[new_y][new_x] == STATE_EMPTY:
                        new_grid[new_y][new_x] = STATE_TAKEN  # move to new position
                    else:
                        new_grid[y][x] = STATE_TAKEN  # stay put
        return new_grid

    def __get_seed_grid__(self):
        return self.rand_seed()

    def __get_next_generation__(self):
        return self.rand_gen_trans()
