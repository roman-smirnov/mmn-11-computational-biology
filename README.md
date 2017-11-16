# MMN11 - cellular automata
Roman Smirnov 
9/11/2017

----------

## Q1.a 
### Question 11, page 80
In classic cellular automata models, for transitions which change the states of nearby cells there are equivalent transitions that only change its own state. 
For example: 
_Transition rule_: a cell with a WOLF state transitions all nearby LAMB cells to EMPTY cells. 
_Equivalent rule_: a cell with a LAMB state transitions to an EMPTY cell if there's a cell with state WOLF in its neighborhood. 

## Q1.b
### Question 14, page 81
The model does change significantly. 
Random choice means that some cells will be transitioned more times than other cells. This may result in unwanted model behavior. E.g a lamb passing near a wolf without being eaten. 

----------


## Q2.a
### Automaton Definition

**Layout**: 
a square non-cyclic 2d grid of cells. 

**States**:
 empty, person, exit.
 
**Neighborhood**: 
cells within a distance of 1 (chebyshev distance) from a given cell.  

**Global Knowledge**
The automaton specifications defined in mmn11 necessitate cells to have some global knowledge . Therefore, we enhance the classic automaton definition by providing the required global knowledge.
_Exit locations_: the coordinates of all the exit locations. 
_Distance to exits_: (AKA a Static Floor Field in literature).
_Crowd_: Number of people within a specified distance of each exit (AKA a Dynamic Floor Field in literature).
_Target Cells_: Selection of cells as destination by other cells - required due to non-deterministic exit selection and PP. 

**Utility Function**
Person cells select their target exit probabilistically based on a calculated safety rating for each exit. We call the formula for calculating this safety rating a Utility Function. The utility function of the subject automaton should be defined so as to result in consistent exit selection (i.e simulated people not likely to show indecisive behavior) while also enabling opportunistic exit re-selection.

Due to above specifications, small variations in spatial distance and crowds must have a dramatic effect on safety rating. Therefore, we define an exponential utility function (maybe there's a better way, didn't dive too deep or make comparisons) thus: safety = 1/(distance^distance_modifier + crowd^crowd_modifier).
(higher safety rating = safer) 

**Stochastic Selection**
_Exit selection_:
Exits are given a safety rating by the utility function. We generate a weighted probability distribution by normalizing the exit safety ratings:
prob(exit) = safety(exit)/sum(safety(exit) for all exits)
We perform the selection by generating a random real number in the range [0,1) and checking the probability distribution ranges to get the corresponding exit.

_Next Position selection_:
Once an Exit has been selected. The next cell to move to is selected by getting a a random cell out of the Possible Positions with the minimum spatial distance to selected exit.

**Transition Rule**:
_Empty cell_:
Change state to Person if it's marked as the next position by a Person in its neighborhood. Otherwise, retain Empty state.

_Person cell_:
1. assign each exit a safety rating based on its distance and crowd 
2. generate a weighted probability distribution based on exit safety ratings
3. randomly select an exit by consideration of its probability
Change state to Empty if there's an Empty cell in the neighborhood which has a lower distance to the selected exit (a PP) than the current cell (CP) which hasn't been selected by another Person cell. 
Otherwise, retain Person state.

_Exit cell_:
Always retain Exit state.

## Q2.b
### Implementation details

#### Overview 
The project is implemented in Python 3.6.

Should be compatible with Python 3+ (no guarantees) .  

An effort was made to make it as portable as possible - so no external (non-standard library) dependencies.

Automatons can be run with a GUI for visualization or without the GUI for faster execution and statistics generation. 

The project does not make use of parallel processing to enhance performance - everything is executed on a single thread/core. 

#### Usage
1. Install python 3.6+
2. Open terminal at project root 
3. type "Python main.py q2" to get a showcase with a GUI
4. type "Python main.py stats" to get some interesting statistics (no GUI)

#### Structure 
The project is composed of 3 main packages:

_automata_: contains templates for implementing automata and actual implementations. The base_automata module contains abstract classes for implementing automatons. The automaton for the mmn is in the mmn11_automata module. 

_gui_: contains visualization functionality for automata and statistics. 

_stats_: this module contains functionality for running bulk automata simulations and collecting and generating statistics without a GUI.

The main module provides a command line interface.


# Q2.c+d
Running the command "Python main.py q2" will go through a few visualisations and generate appropriate statistics and plot a graph at end of each visualisation. 

![automata grid](https://github.com/roman-smirnov/computational_biology/raw/master/automaton_grid.png)

![automata statistics](https://github.com/roman-smirnov/computational_biology/raw/master/automaton_graph.png)

# Q2.e
Running the command "Python main.py stats" will go through many runs with similar parameters for each scenario to generate statistics (runs without a GUI).
WARNING! MAY TAKE SOME TIME! 
 
![automata run with no gui](https://github.com/roman-smirnov/computational_biology/raw/master/automaton_stats.png)

### Some interesting findings: 

_exit selection bias_:
There is a slight biased towards exits with lower y/x coordinates - this is due to neighbor coordinates being generated top->down, left->right, so when it the minimum distance PP is selected it is always the top-left most. 
I reshuffled the list of neighbors to reduce the bias but it is still there somewhat, should implement a randomized selection between minimum PPs to get rid of it.

_spatial distance overweight_: 
Giving a very large weight to spatial distance in the utility function will cause Persons to disregard knowledge about crowd data and cause problems in scenarios where Persons are not uniformly distributed across the grid.

_crowd weight significance_:
overcrowding knowledge is advantageous primarily when people are not unevenly distributed across the grid and there are exits in both high density and low density regions. There are plenty of scenarios where crowd knowledge doesn't matter or even hurts performance. 

