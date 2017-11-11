""" module containing implementation of automata which simulate some phenomena """

from automata.base_automata import BaseFloorFieldAutomaton  # import base class


class EmergencyEscapeAutomaton(BaseFloorFieldAutomaton):
    """ this class implements an automaton simulation of an evacuation during an emergency """

    # states of automaton
    STATE_EMPTY = 0  # grid cell is empty
    STATE_PERSON = 1  # a grid cell is a person
    STATE_EXIT = 2  # a grid cell is an escape exit

    def __init__(self, height, width, exits, exit_rad=3, dist_mod=3, crowd_mod=3, ppl_interval=3, evenly_dist=True):
        """
            Instantiate and setup the automaton simulation
            :param height: number of rows in automaton grid
            :param width: number of columns in automaton grid
            :param exits: list of exit coordinates to be placed on grid
            :param exit_rad: radius around exit which counts as an exit area (to count people in for each exit)
            :param dist_mod: modifier for weight of exit distance in utility function
            :param crowd_mod: modifier for weight of number of people in exit area in utility function
            :param ppl_interval: at what to seed people at (smaller interval generates more people at seed time)
            :param evenly_dist: evenly distribute people across the grid at seed time
        """

        # data structs
        self.exit_area = {}
        self.crowd = {}
        self.exits = exits

        # configs
        self.exit_radius = exit_rad
        self.dist_mod = dist_mod
        self.crowd_mod = crowd_mod
        self.ppl_interval = ppl_interval
        self.evenly_dist = evenly_dist

        # statistics
        self.escaped_at_exit = {exit_pos: {0: 0} for exit_pos in exits}

        # init super
        BaseFloorFieldAutomaton.__init__(self, height, width, radius=1, num_of_states=3)

    def __get_safety__(self, exit_pos, cur_pos):
        """ returns a safety rating of an exit, from the point of view of given position"""
        # calc distance and crowd at exit area
        dist = self.cheb_dist(exit_pos, cur_pos)
        crowd = self.crowd[exit_pos]
        # process values
        dist_val = dist ** self.dist_mod
        crowd_val = crowd ** self.crowd_mod
        # safety is inversely proportionate to dist and crowd at the exit
        return 1 / (dist_val + crowd_val)

    def __exit_choice__(self, cur_pos):
        """ randomly select an  exit pos - randomness weights are assigned via safety rating and uniform probability """
        exit_safe_list = list(
            map(lambda exit_pos: self.__get_safety__(exit_pos, cur_pos), self.exits))  # calc safety vals
        exit_prob_list = self.weights_to_uni_prob(exit_safe_list)  # calc probabilities from weights
        return self.rand_prob_choice(self.exits, exit_prob_list)  # chosen exit

    def __possible_pos__(self, cur_pos, exit_pos, neighbors):
        """ returns a list of positions which are spatially closer to the given exit """
        cur_dist = self.cheb_dist(cur_pos, exit_pos)
        return list(filter(lambda n_pos: self.cheb_dist(n_pos, exit_pos) < cur_dist, neighbors))

    def __min_dist_pos__(self, exit_pos, positions):
        """ returns a position with minimal spatial distance to the given exit """
        return min(positions, key=lambda x: self.cheb_dist(x, exit_pos))

    def __person_trans__(self, y, x, trg_to_src):
        """ handle a generational transition of a cell with a person state """
        # choose an exit
        exit_choice = self.__exit_choice__((y, x))

        # retrieve neighbor cells to CP
        neighbors = list(self.__get_neighbors_at__((y, x)))

        # filter out the neighbor cells where other people are located
        # this is by design - in real life a person might suddenly halt, so you don't rely on him/her moving
        neighbors = list(filter(lambda np: self.grid[np[0]][np[1]] in (self.STATE_EMPTY, self.STATE_EXIT), neighbors))

        # filter out cells which are marked for movement by other people
        neighbors = list(filter(lambda n_pos: n_pos not in trg_to_src, neighbors))

        # filter are neighbors which are not PPs
        neighbors = self.__possible_pos__((y, x), exit_choice, neighbors)

        if not neighbors:
            # if there are no cells meeting the required criteria to move - stay put
            return self.STATE_PERSON
        else:
            # mark cell as target for movement and set CP state in next generation as empty
            trg_to_src[self.__min_dist_pos__(exit_choice, neighbors)] = True
            return self.STATE_EMPTY

    def __trans_first_pass__(self, new_grid, is_target):
        """ the first pass of a generational transition - only handles people states, other states are skipped """
        for y in range(0, self.height):
            for x in range(0, self.width):
                if self.grid[y][x] == self.STATE_PERSON:
                    new_grid[y][x] = self.__person_trans__(y, x, is_target)
                else:
                    pass  # exits and empty cells are handled in a later stage

    def __trans_second_pass__(self, new_grid, is_target):
        """ second pass of a generational transition  handles empty states and exit states """
        for t_y, t_x in is_target:
            if self.grid[t_y][t_x] == self.STATE_EMPTY:  # a person has moved
                new_grid[t_y][t_x] = self.STATE_PERSON
            else:
                self.escaped_at_exit[(t_y, t_x)][self.generation_count] = 1  # a person has escaped

    def __emr_esc_trans__(self):
        """ this method generates the next generation grid of the automaton """
        # generate a new grid with all cells set to empty
        new_grid = self.uniform_seed(self.height, self.width, self.STATE_EMPTY)
        # place exits on newly created grid
        new_grid = self.__seed_exits__(new_grid)

        # keep track of where each person selects to go next to avoid collisions
        # and use it in stage 2 to handle target cells
        is_target = {}

        # first pass handles person cells
        self.__trans_first_pass__(new_grid, is_target)

        # second pass handles exit cells and empty cells
        self.__trans_second_pass__(new_grid, is_target)

        return new_grid

    def __get_exit_area__(self, exit_pos):
        """ returns a list of cell coords within the exit area radius of an exit """
        if exit_pos not in self.exit_area:
            self.exit_area[exit_pos] = self.get_cells_in_radius(exit_pos, self.exit_radius)
        return self.exit_area[exit_pos]

    def __seed_people__(self):
        """ generates a grid of randomly placed people, all other states are empty states """
        return self.rand_seed(self.height, self.width, self.STATE_EMPTY, self.STATE_PERSON,
                              interval=self.ppl_interval, fill_state=self.STATE_EMPTY, evenly_dist=self.evenly_dist)

    def __seed_exits__(self, grid):
        """ place exit states at set exit positions on a given grid"""
        # iterate over all exists and place on grid
        for exit_y, exit_x in self.exits:
            grid[exit_y][exit_x] = self.STATE_EXIT  # place the exit on the grid
        return grid

    def __get_seed_grid__(self):
        """ generates the initial state grid of the automaton """
        seed_grid = self.__seed_people__()  # place people randomly on the grid
        seed_grid = self.__seed_exits__(seed_grid)  # place exits at specified position on grid
        return seed_grid

    def __update_crowd_at_exits__(self):
        """ updates the crowd value for each exit """
        for exit_pos in self.exits:
            exit_area = self.__get_exit_area__(exit_pos)
            # sum the people at the exit area
            crowd_at_exit = sum(1 if self.grid[p[0]][p[1]] == self.STATE_PERSON else 0 for p in exit_area)
            self.crowd[exit_pos] = crowd_at_exit

    def __get_next_generation__(self):
        """ returns the next generation grid of the automaton"""
        self.__update_crowd_at_exits__()
        return self.__emr_esc_trans__()

    def is_terminal(self):
        """ returns true if all people escaped """
        if self.gen_state_count[self.generation_count][self.STATE_PERSON] == 0:
            return True
        else:
            return False

    def get_exit_esc_count(self):
        """ returns a dict of exit:generation:num_of_escaped_ppl """
        return self.escaped_at_exit

    def get_num_of_people_at_seed(self):
        return self.gen_state_count[0][self.STATE_PERSON]
