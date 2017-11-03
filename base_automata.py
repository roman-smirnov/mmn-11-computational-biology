# this is the state object of the automata universe
class BaseAutomata:
    neighbors = {}  # holds the a list of neighbor coords for each cell - to avoid recalculating each time

    def __init__(self, height, width, radius, num_of_states, trans_func, seed_grid):
        self.height = height
        self.width = width
        self.radius = radius
        self.trans_func = trans_func
        self.num_of_states = num_of_states
        self.grid = seed_grid

    def update_world_state(self):
        new_grid = self.trans_func(self)
        self.set_grid(new_grid)

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_grid(self):
        return self.grid

    def set_grid(self, grid):
        self.grid = grid

    def get_neighbors_at(self, pos):
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

    def get_all_neighbors(self):
        return self.neighbors

    def get_num_of_states(self):
        return self.num_of_states
