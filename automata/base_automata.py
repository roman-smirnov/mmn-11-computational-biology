"""
    The base_automata module contains a BaseAutomata class which provides a basic template for automata implementations
"""


class BaseAutomaton:
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
        self.grid = self.__get_seed_grid__()

    def get_height(self):
        """ returns the number of rows in the world grid """
        return self.height

    def get_width(self):
        """ returns the number of cols in the world grid """
        return self.width

    def get_grid(self):
        """ returns the world state grid  """
        return self.grid

    def set_grid(self, grid):
        """ replace the world state grid with another grid - new grid must have same dimensions and states"""
        self.grid = grid

    def get_num_of_states(self):
        """ get the number of possible states for each cell in the automaton """
        return self.num_of_states

    def __get_neighbors_at__(self, pos):
        """ returns a list of neighbors cell coordinates of the given position - default impl is for a square grid """
        # if not in the dict: calculate it, add to dict, return it
        if pos not in self.neighbors:
            y_pos, x_pos = pos
            neighbors = []
            # iterate over all the cells in neighborhood radius and add to list of neighbors
            for y in range(max(0, y_pos - self.radius), min(self.height, y_pos + self.radius + 1)):
                for x in range(max(0, x_pos - self.radius), min(self.width, x_pos + self.radius + 1)):
                    neighbors.append((y, x))  # add neighbor to list
            self.neighbors[pos] = tuple(neighbors)  # add neighbors to dict
        return self.neighbors[pos]

    def __get_seed_grid__(self):
        """ returns an initial state grid of the automaton """
        # SUBCLASSES OF BASE AUTOMATA MUST IMPLEMENT THIS METHOD AND RETURN A GRID OF INITIAL STATES - see example impls
        raise NotImplementedError("this method must be overridden by subclasses of BaseAutomata")

    def __get_next_generation__(self):
        """ returns the state grid of the next generation of the automaton """
        # SUBCLASSES OF BASE AUTOMATA MUST IMPLEMENT THIS METHOD AND RETURN GRID OF STATES OF THE NEXT GENERATION
        raise NotImplementedError("this method must be overridden by a subclasses of BaseAutomata")

    def update_world_state(self):
        """ transitions the automaton to its next generation """
        self.set_grid(self.__get_next_generation__())
