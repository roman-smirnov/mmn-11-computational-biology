"""
    The base_automata module contains a BaseAutomata class which provides a basic template for automata implementations
"""

import random
import math
from abc import ABC, abstractmethod
from functools import reduce


class BaseAutomaton(ABC):
    """
        Provides a template for implementing cellular automatons.
        Designed for inheritance - subclasses are required to implement a few specified methods,
        will raise a NotImplementedError if required methods are not implemented
    """

    def __init__(self, height, width, radius, num_of_states):
        """ :param height - how many rows in the world state grid
            :param width  - how many columns in the world state grid
            :param radius - the neighborhood radius of each cell (i.e distance in cells)
            :param num_of_states - the number of possible states for the automaton

         """
        self.height = height
        self.width = width
        self.radius = radius
        self.neighbors = {}  # holds a list of neighbor coords for each cell - to avoid recalculating each time
        self.num_of_states = num_of_states

        # used to generate stats
        self.generation_count = 0  # incremented after each generation transition
        self.gen_state_count = {}  # a dict of (state, generation): count

        # IMPORTANT! seed generation happens during init!
        self.grid = self.__get_seed_grid__()
        # IMPORTANT! this call sets stats at gen 0
        self.__update_stats__()

    def get_height(self):
        """ returns the number of rows in the world grid """
        return self.height

    def get_width(self):
        """ returns the number of cols in the world grid """
        return self.width

    def get_grid(self):
        """ returns the world state grid  """
        return self.grid

    def get_num_of_states(self):
        """ get the number of possible states for each cell in the automaton """
        return self.num_of_states

    def get_cells_in_radius(self, pos, radius):
        """ returns a list of cell coords in a given radius around a pos - default impl is for a square grid """
        y_pos, x_pos = pos
        cells_in_rad = []
        # iterate over all the cells in neighborhood radius and add to list of neighbors
        for y in range(max(0, y_pos - radius), min(self.height, y_pos + radius + 1)):
            for x in range(max(0, x_pos - radius), min(self.width, x_pos + radius + 1)):
                cells_in_rad.append((y, x))  # add neighbor to list
        return cells_in_rad

    def __get_neighbors_at__(self, pos):
        """ returns a list of neighbors cell coordinates of the given position - default impl is for a square grid """
        # if not in the dict: calculate it, add to dict, return it
        if pos not in self.neighbors:
            neighbors = self.get_cells_in_radius(pos, self.radius)
            # IMPORTANT!!!!!!!!!! randomize the order of neighbors
            random.shuffle(neighbors)  # if you don't randomize the order, you might create a bias toward lower coords!
            self.neighbors[pos] = tuple(neighbors)  # add neighbors to dict
        return self.neighbors[pos]

    @abstractmethod
    def __get_seed_grid__(self):
        """ returns an initial state grid of the automaton """
        # SUBCLASSES OF BASE AUTOMATA MUST IMPLEMENT THIS METHOD AND RETURN A GRID OF INITIAL STATES - see example impls
        raise NotImplementedError("this method must be overridden by subclasses of BaseAutomata")

    @abstractmethod
    def __get_next_generation__(self):
        """ returns the state grid of the next generation of the automaton """
        # SUBCLASSES OF BASE AUTOMATA MUST IMPLEMENT THIS METHOD AND RETURN GRID OF STATES OF THE NEXT GENERATION
        raise NotImplementedError("this method must be overridden by a subclasses of BaseAutomata")

    def __update_stats__(self):
        """ records how many states of each kind were present at each generation"""
        # flatten the grid into a 1d list of states
        flat_grid = reduce(lambda x, y: x + y, self.grid)
        # init a local dict count states
        state_count = {state: 0 for state in range(0, self.num_of_states)}
        # count the number of states per each generation
        for state in flat_grid:
            state_count[state] += 1
        # IMPORTANT!!! THIS IS A MEMORY LEAK! LONG RUNNING AUTOMATONS MAY SUFFER!!!!
        self.gen_state_count[self.generation_count] = state_count  # add the state count to generational dict

    def get_gen_state_count(self):
        """ returns a dict of generation_num:state_dict where state_dict:num number of states at given generation"""
        return self.gen_state_count

    def get_gen_count(self):
        """ returns the count of generations"""
        return self.generation_count

    def update_world_state(self):
        """ transitions the automaton to its next generation """
        self.grid = self.__get_next_generation__()
        self.generation_count += 1  # increment before recording stats
        self.__update_stats__()  # handle statistics record here

    def is_terminal(self):
        """ returns true if automaton has reached a quiescent state - this may never be True!!"""
        return False


class BaseStochasticAutomaton(BaseAutomaton):
    """
        Provides a basic abstract template for implementing cellular automatons. See BaseAutomaton parent class.
        Includes some helper methods to implement automatons with stochastic behaviours.
    """

    @staticmethod
    def weights_to_uni_prob(list_of_weights):
        """ generates a list of probabilities (sums to 1) from given list of weights, assumes uniform distribution """
        norm_factor = sum(list_of_weights)
        return list(map(lambda s: s / norm_factor, list_of_weights))  # normalize and subtract from 1

    @staticmethod
    def rand_prob_choice(choices, probabilities):
        """
            Randomly choose an item from list of choices, with probability specified by probabilities list
            :param choices: list of items from which to choose a single item
            :param probabilities: a list of probabilities corresponding with list of items (same index)
        """
        rand_prob = random.random()  # generate random float between 0 and 1
        prob_sum = 0
        for i in range(0, len(probabilities)):  # sum probabilities until random number is exceeded
            prob_sum += probabilities[i]
            if prob_sum >= rand_prob:  # if random number is exceeded - return the choice in prob range
                return choices[i]
        raise RuntimeError(" this should never happen! check choices and probabilities!")

    @staticmethod
    def rand_choice(choices):
        """ randomly choose an item with equal probability for each item """
        return random.choice(choices)

    @staticmethod
    def rand_int(range_s, range_e):
        """ generate a random integer within given range """
        return random.randint(range_s, range_e)

    @staticmethod
    def rand_seed(height, width, min_state, max_state, interval, fill_state, evenly_dist):
        """
            Generate a randomized a seed state grid
            Every grid cell at an interval position will get a random state between min_state and max_state(inclusive)
            Every grid cell between intervals will set to fill_state
        """
        seed_grid = []
        for y in range(0, height):
            seed_grid.append([])
            for x in range(0, width):
                # generate a random state in every third row,column cell - all others will be left at state 0
                state = random.randint(min_state, max_state) if (x % interval, y % interval) == (0, 0) else fill_state
                # if not evenly distributed option is selected - people will be seeded on only a quarter of the grid
                state = fill_state if not evenly_dist and (x > int(width / 2) or y > int(height / 2)) else state
                seed_grid[y].append(state)
        return seed_grid

    @staticmethod
    def uniform_seed(height, width, fill_state):
        """ generate a state grid with all cells set to value of given state """
        uniform_grid = []
        for y in range(0, height):
            uniform_grid.append([])
            for x in range(0, width):
                uniform_grid[y].append(fill_state)
        return uniform_grid


class BaseFloorFieldAutomaton(BaseStochasticAutomaton):
    """
        Base class for implementing automatons with some global knowledge of their world. See parent class.
        Contains some helper methods for measuring distance etc.
    """

    @staticmethod
    def euc_dist(pos1, pos2):
        """ calculate the euclidean distance between given 2d positions"""
        pos1_y, pos1_x = pos1
        pos2_y, pos2_x = pos2
        return math.sqrt((pos1_y - pos2_y) ** 2 + (pos1_x - pos2_x) ** 2)

    @staticmethod
    def man_dist(pos1, pos2):
        """ calculate the manhattan distance between given 2d positions"""
        pos1_y, pos1_x = pos1
        pos2_y, pos2_x = pos2
        return math.fabs(pos1_y - pos2_y) + math.fabs(pos1_x - pos2_x)

    @staticmethod
    def cheb_dist(pos1, pos2):
        """ calculate the chebyshev distance between given 2d positions"""
        pos1_y, pos1_x = pos1
        pos2_y, pos2_x = pos2
        return max(math.fabs(pos1_y - pos2_y), math.fabs(pos1_x - pos2_x))
