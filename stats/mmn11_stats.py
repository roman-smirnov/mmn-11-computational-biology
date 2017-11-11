""" module for executing multiple simulation runs and generating some interesting statistics """

from automata.mmn11_automata import *  # import crowd simulation automaton


def demo_choice_bias():
    """ demonstrate bias caused by sequential execution of automaton - exits with lower y/x more likely to be chosen """
    rows = 50
    cols = 50
    exits = [(5, 5), (49, 49)]
    runs = 25

    exit_esc_total = {exit_pos: 0 for exit_pos in exits}

    print("\n\nGENERATING CHOICE BIAS STATISTICS..............")
    print("Grid height: ", rows, " Grid width: ", cols)
    print("Number of runs: ", runs)

    for i in range(0, runs):    # runs many times
        automaton = EmergencyEscapeAutomaton(rows, cols, exits)
        while not automaton.is_terminal():
            automaton.update_world_state()
        for exit_pos in exits:  # collect stats from each run
            esc_count = sum(
                automaton.get_exit_esc_count()[exit_pos][g] for g in automaton.get_exit_esc_count()[exit_pos])
            exit_esc_total[exit_pos] += esc_count

    print("Escaped at each exit: ")
    for exit_pos in exits:
        print("  exit: " + str(exit_pos) + " escaped total: " + str(exit_esc_total[exit_pos]))

    print("Escaped average at each exit: ")
    for exit_pos in exits:
        print("  exit: " + str(exit_pos) + " escaped average: " + str(exit_esc_total[exit_pos] / runs))


def demo_dist_modifier():
    """ demonstrate distance utility function modifier effect on escape generation count """
    rows = 50
    cols = 50

    exits = [(5, 5), (45, 45)]

    min_dist_modifier = 2  # lower values than this take a very long time to run!
    max_dist_modifier = 6  #

    runs = 25

    modifier_esc_time = {modifier: 0 for modifier in range(min_dist_modifier, max_dist_modifier)}

    print("\n\nGENERATING DISTANCE MODIFIER STATISTICS..............")
    print("Grid height: ", rows, " Grid width: ", cols)
    print("Number of runs: ", runs)

    for i in range(0, runs):
        for d in range(min_dist_modifier, max_dist_modifier):
            automaton = EmergencyEscapeAutomaton(rows, cols, exits, dist_mod=d, evenly_dist=False)
            while not automaton.is_terminal():
                automaton.update_world_state()
            modifier_esc_time[d] += automaton.get_gen_count()

    for d in modifier_esc_time:
        print("distance modifier: ", d, " avg esc generations: ", modifier_esc_time[d] / runs)


def demo_crowd_modifier():
    """ demonstrate crowd utility function modifier effect on escape generation count """
    rows = 50
    cols = 50

    exits = [(5, 5), (45, 45)]

    min_crowd_modifier = 1
    max_crowd_modifier = 6

    runs = 25

    modifier_esc_time = {modifier: 0 for modifier in range(min_crowd_modifier, max_crowd_modifier)}

    print("\n\nGENERATING CROWD MODIFIER STATISTICS..............")
    print("Grid height: ", rows, " Grid width: ", cols)
    print("Number of runs: ", runs)

    for i in range(0, runs):
        for c in range(min_crowd_modifier, max_crowd_modifier):
            automaton = EmergencyEscapeAutomaton(rows, cols, exits, crowd_mod=c, evenly_dist=False)
            while not automaton.is_terminal():
                automaton.update_world_state()
            modifier_esc_time[c] += automaton.get_gen_count()

    for c in modifier_esc_time:
        print("crowd modifier: ", c, " avg esc generations: ", modifier_esc_time[c] / runs)


def demo_exit_radius():
    """ demonstrate exit area radius effect on escape generation count """
    rows = 50
    cols = 50

    exits = [(5, 5), (45, 45)]

    min_exit_radius = 1
    max_exit_radius = 20
    radius_iter_jump = 5

    runs = 25

    modifier_esc_time = {modifier: 0 for modifier in range(min_exit_radius, max_exit_radius, radius_iter_jump)}

    print("\n\nGENERATING EXIT RADIUS STATISTICS..............")
    print("Grid height: ", rows, " Grid width: ", cols)
    print("Number of runs: ", runs)

    for i in range(0, runs):
        for r in range(min_exit_radius, max_exit_radius, radius_iter_jump):
            automaton = EmergencyEscapeAutomaton(rows, cols, exits, exit_rad=r, evenly_dist=False)
            while not automaton.is_terminal():
                automaton.update_world_state()
            modifier_esc_time[r] += automaton.get_gen_count()

    for r in modifier_esc_time:
        print("exit radius: ", r, " avg esc generations: ", modifier_esc_time[r] / runs)


def demo_people_density():
    pass


def demo_room_size():
    pass


def demo_exit_location():
    pass


def demo_num_of_exits():
    pass


def demo_exit_size():  # several exits close by together
    pass
