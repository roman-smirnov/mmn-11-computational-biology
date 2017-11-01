import random

STATE_TAKEN = 1
STATE_FREE = 0


class Grid:
    def __init__(self, height, width, radius, states, neighborhoods):
        self.height = height
        self.width = width
        self.radius = radius
        self.grid = {}
        self.neighborhoods = {}
        self.init_grid()
        self.init_states(states)
        self.init_neighborhoods(neighborhoods)

    def init_grid(self):
        # init a grid of size height,width with all cells in state zero
        for y in range(0, self.height):
            for x in range(0, self.width):
                self.grid[(y, x)] = STATE_FREE

    def init_states(self, states):
        # no seed states were received
        if states is None:
            return
        # set the initial seed states
        for y, x, state in states:
            self.grid[(y, x)] = state

    # requires more memory but less computation - alternatively can re-compute each time
    def init_neighborhoods(self, neighborhoods):
        # if neighborhoods were already pre-calculated
        if neighborhoods is not None:
            self.neighborhoods = neighborhoods
            return
        # pre-calculate the neighborhood values for each cell
        for y_pos, x_pos in self.grid:
            neighbors = []  # list of neighbors
            # iterate over all the cells in neighborhood radius
            for y in range(max(0, y_pos - self.radius), min(self.height, y_pos + self.radius+1)):
                for x in range(max(0, x_pos - self.radius), min(self.width, x_pos + self.radius+1)):
                    neighbors.append((y, x))  # add neighbor to list
            self.neighborhoods[(y_pos, x_pos)] = tuple(neighbors)

    def get_state(self, pos):
        return self.grid[pos]

    def set_state(self, pos, state):
        self.grid[pos] = state

    def get_all_positions(self):
        return self.grid

    def get_neighbors(self, pos):
        return self.neighborhoods[pos]

    def get_all_neighborhoods(self):
        return self.neighborhoods


def rand_seed(height, width, how_many):
    seed_states = set()  # the set is to prevent duplicates
    for i in range(0, how_many):
        # WARNING! some duplicates will be created but not added to the set
        seed_states.add((random.randint(0, height), random.randint(0, width), STATE_TAKEN))
    return seed_states


def rand_trans(pos, neighbors, grid):
    valid_neighbors = []  # collect only the valid position in the neighborhood
    for y, x in neighbors:
        if grid.get_state((y, x)) == STATE_FREE:
            valid_neighbors.append((y, x))
    if not valid_neighbors:
        new_pos = pos
    else:
        new_pos = random.choice(valid_neighbors)  # new position chosen randomly from valid transition positions
    return new_pos


class Universe:
    def __init__(self, height=50, width=50, radius=1, how_many=50, trans_func=rand_trans, seed_states=None):
        self.height = height
        self.width = width
        self.radius = radius
        self.trans_func = trans_func
        if seed_states is None:
            seed_states = rand_seed(height, width, how_many)
        self.grid = Grid(height, width, radius, seed_states, None)

    def time_tick(self):
        new_grid = Grid(self.height, self.width, self.radius, None, self.grid.get_all_neighborhoods())
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.grid.get_state((y, x)) == STATE_TAKEN:
                    neighbors = self.grid.get_neighbors((y, x))
                    new_pos = self.trans_func((y, x), neighbors, self.grid)
                    new_grid.set_state(new_pos, STATE_TAKEN)
        self.grid = new_grid

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_grid(self):
        return self.grid