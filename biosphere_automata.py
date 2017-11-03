import random
import base_automata

# import importlib
# importlib.reload(base_automata)


NUM_OF_STATES = 10
STATE_FREE = 0
RADIUS = 1


def rand_seed(height, width):
    seed_grid = []
    for y in range(0, height):
        seed_grid.append([])
        for x in range(0, width):
            state = random.randint(0, NUM_OF_STATES - 1) if (y % 2, x % 2) == (0, 0) else 0
            seed_grid[y].append(state)
    return seed_grid


def zero_seed(height, width):
    zero_grid = []
    for y in range(0, height):
        zero_grid.append([])
        for x in range(0, width):
            zero_grid[y].append(STATE_FREE)
    return zero_grid


def food_trans(automaton):
    old_grid = automaton.get_grid()
    height = automaton.get_height()
    width = automaton.get_width()
    new_grid = zero_seed(height, width)
    for y in range(0, height):
        for x in range(0, width):
            if old_grid[y][x] == STATE_FREE:
                continue
            else:
                neighbors = automaton.get_neighbors_at((y, x))
                for n_y, n_x in neighbors:
                    if old_grid[n_y][n_x] > old_grid[y][x]:
                        old_grid[y][x] = STATE_FREE
                        break
                if old_grid[y][x] == STATE_FREE:
                    continue
                new_y, new_x = random.choice(neighbors)
                if new_grid[new_y][new_x] == STATE_FREE:
                    new_grid[new_y][new_x] = old_grid[y][x]  # move to new position
                else:
                    new_grid[y][x] = old_grid[y][x]

    return new_grid


class BiosphereAutomata(base_automata.BaseAutomata):
    def __init__(self, height, width):
        seed_grid = rand_seed(height, width)
        base_automata.BaseAutomata.__init__(self, height, width, RADIUS, NUM_OF_STATES, food_trans, seed_grid)
