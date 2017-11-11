""" module contains some simple automata as implementation examples """
from automata.base_automata import BaseStochasticAutomaton


class RandomWalkAutomaton(BaseStochasticAutomaton):
    """ this class implements a simple automaton which simulates actors randomly moving randomly to adjacent cells """

    STATE_TAKEN = 1
    STATE_EMPTY = 0

    def __init__(self, height, width):
        BaseStochasticAutomaton.__init__(self, height, width, radius=1, num_of_states=2)

    def rand_gen_trans(self):
        """ stochasticly transition to next the generation of the automaton """
        new_grid = self.uniform_seed(self.height, self.width, self.STATE_EMPTY)
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.grid[y][x] == self.STATE_EMPTY:
                    continue
                else:
                    neighbors = self.__get_neighbors_at__((y, x))
                    new_y, new_x = self.rand_choice(neighbors)
                    if self.grid[new_y][new_x] == self.STATE_EMPTY and new_grid[new_y][new_x] == self.STATE_EMPTY:
                        new_grid[new_y][new_x] = self.STATE_TAKEN  # move to new position
                    else:
                        new_grid[y][x] = self.STATE_TAKEN  # stay put
        return new_grid

    def __get_seed_grid__(self):
        return self.rand_seed(self.height, self.width, self.STATE_EMPTY,
                              self.STATE_TAKEN, interval=3, fill_state=self.STATE_EMPTY)

    def __get_next_generation__(self):
        return self.rand_gen_trans()


class FoodHierarchyAutomaton(BaseStochasticAutomaton):
    """ this class implements a simple automaton which simulates cells having a food-chain-like hierarchy """

    STATE_EMPTY = 0

    def __init__(self, height, width):
        BaseStochasticAutomaton.__init__(self, height, width, radius=1, num_of_states=10)

    def food_chain_gen_trans(self):
        """ transition to next the generation of the automaton """
        new_grid = self.uniform_seed(self.height, self.width, self.STATE_EMPTY)
        for y in range(0, self.height):
            for x in range(0, self.width):
                # if the current cell is in empty state - it stays empty and nothing needs to be done
                if self.grid[y][x] == self.STATE_EMPTY:
                    continue
                else:
                    neighbors = self.__get_neighbors_at__((y, x))
                    # iterate over neighbor cells - if a cell is found having a higher state, the cur cell dies
                    for n_y, n_x in neighbors:
                        if self.grid[n_y][n_x] > self.grid[y][x]:
                            self.grid[y][x] = self.STATE_EMPTY
                            break
                    if self.grid[y][x] == self.STATE_EMPTY:
                        continue
                    new_y, new_x = self.rand_choice(neighbors)  # choose a random neighbor
                    if new_grid[new_y][new_x] == self.STATE_EMPTY:
                        new_grid[new_y][new_x] = self.grid[y][x]  # move to chosen position
                    else:
                        new_grid[y][x] = self.grid[y][x]  # stay put
        return new_grid

    def __get_seed_grid__(self):
        return self.rand_seed(self.height, self.width, self.STATE_EMPTY,
                              self.num_of_states, interval=3, fill_state=self.STATE_EMPTY)

    def __get_next_generation__(self):
        return self.food_chain_gen_trans()
