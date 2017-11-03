import random

from automata import base_automata

# import importlib
# importlib.reload(base_automata)

STATE_TAKEN = 1
STATE_FREE = 0
NUM_OF_STATES = 2
RADIUS = 1


def rand_seed(height, width):
    seed_grid = []
    for y in range(0, height):
        seed_grid.append([])
        for x in range(0, width):
            state = random.getrandbits(1) if (x % 3, y % 3) == (0, 0) else 0
            seed_grid[y].append(state)
    return seed_grid


def zero_seed(height, width):
    zero_grid = []
    for y in range(0, height):
        zero_grid.append([])
        for x in range(0, width):
            zero_grid[y].append(STATE_FREE)
    return zero_grid


def rand_trans(automaton):
    old_grid = automaton.get_grid()
    height = automaton.get_height()
    width = automaton.get_width()
    new_grid = zero_seed(height, width)
    for y in range(0, height):
        for x in range(0, width):
            if old_grid[y][x] == STATE_FREE:
                continue
            else:
                neighbors = automaton.__get_neighbors_at__((y, x))
                new_y, new_x = random.choice(neighbors)
                if old_grid[new_y][new_x] == STATE_FREE and new_grid[new_y][new_x] == STATE_FREE:
                    new_grid[new_y][new_x] = STATE_TAKEN  # move to new position
                else:
                    new_grid[y][x] = STATE_TAKEN  # stay put
    return new_grid


class RandomAutomaton(base_automata.BaseAutomaton):
    def __init__(self, height, width):
        seed_grid = rand_seed(height, width)
        base_automata.BaseAutomaton.__init__(self, height, width, RADIUS, NUM_OF_STATES, rand_trans, seed_grid)
