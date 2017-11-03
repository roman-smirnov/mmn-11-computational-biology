import random

from automata import base_automata

NUM_OF_STATES = 10
STATE_EMPTY = 0
RADIUS = 1


class FoodChainAutomaton(base_automata.BaseAutomaton):
    """ this class implements a simple automaton which simulates cells having a food-chain-like hierarchy """

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
                state = random.randint(0, self.num_of_states - 1) if (x % 3, y % 3) == (0, 0) else STATE_EMPTY
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

    def food_chain_gen_trans(self):
        """ transition to next the generation of the automaton """
        new_grid = self.empty_seed()
        for y in range(0, self.height):
            for x in range(0, self.width):
                # if the current cell is in empty state - it stays empty and nothing needs to be done
                if self.grid[y][x] == STATE_EMPTY:
                    continue
                else:
                    neighbors = self.__get_neighbors_at__((y, x))
                    # iterate over neighbor cells - if a cell is found having a higher state, the cur cell dies
                    for n_y, n_x in neighbors:
                        if self.grid[n_y][n_x] > self.grid[y][x]:
                            self.grid[y][x] = STATE_EMPTY
                            break
                    if self.grid[y][x] == STATE_EMPTY:
                        continue
                    new_y, new_x = random.choice(neighbors)  # choose a random neighbor
                    if new_grid[new_y][new_x] == STATE_EMPTY:
                        new_grid[new_y][new_x] = self.grid[y][x]  # move to chosen position
                    else:
                        new_grid[y][x] = self.grid[y][x]  # stay put
        return new_grid

    def __get_seed_grid__(self):
        return self.rand_seed()

    def __get_next_generation__(self):
        return self.food_chain_gen_trans()
