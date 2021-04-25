#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os
from search import *  # for search engines
# for snowball specific classes
from snowman import SnowmanState, Direction, snowman_goal_state
from test_problems import PROBLEMS  # 20 test problems


def heur_manhattan_distance(state):
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a snowman state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each snowball that has yet to be stored and the storage point is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.
    distance = 0
    (x, y) = state.destination
    for a, b in state.snowballs:
        distance += abs(a - x) + abs(b - y)
    return distance


# HEURISTICS
def trivial_heuristic(state):
    '''trivial admissible snowball heuristic'''
    '''INPUT: a snowball state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state (# of moves required to get) to the goal.'''
    return len(state.snowballs)


def blocked(snowball, destination, width, height, obstacles, robot):
    '''return True if it is impossible for the snowball to reach goal'''
    if snowball == destination:
        return False
    if snowball in obstacles or snowball == robot:
        return True
    x, y = snowball
    if near_wall(x, y, destination, width, height):
        return True
    # left, right, top, down
    l, r, t, d = (x-1, y), (x+1, y), (x, y+1), (x, y-1)
    surroundings = {l: is_blocked(
        l[0], l[1], width, height, obstacles),
        r: is_blocked(
        r[0], r[1], width, height, obstacles),
        t: is_blocked(
        t[0], t[1], width, height, obstacles),
        d: is_blocked(
        d[0], d[1], width, height, obstacles)}
    # return True if any 2 neighboring sides are blocked
    return (surroundings[l] and surroundings[t]) or (surroundings[t] and surroundings[r]) or (surroundings[r] and surroundings[d]) or (surroundings[d] and surroundings[l])


def near_wall(x, y, destination, width, height):
    '''Return True if snowball is near wall but goal is not near wall'''
    if x in [0, width-1] and destination[0] != x:
        return True
    elif y in [0, height-1] and destination[1] != y:
        return True
    else:
        return False


def is_blocked(x, y, width, height, obstacles):
    '''Return True if (x, y) is outside the wall or contains a obstacle'''
    # return x in [-1, width] or y in [-1, height] or (x, y) in obstacles
    return x <= -1 or x >= width or y <= -1 or y >= height or (x, y) in obstacles


def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.
    distance = 0
    (x, y) = state.destination
    for ball in state.snowballs:
        if blocked(ball, state.destination, state.width, state.height, state.obstacles, state.robot):
            return float("inf")  # positive infinity
        length = abs(ball[0] - x) + abs(ball[1] - y)
        # 3 snowballs
        if state.snowball_sizes[state.snowballs[ball]] == 'G':
            length *= 3
        # 2 snowballs
        elif state.snowball_sizes[state.snowballs[ball]] in ['A', 'B', 'C']:
            length *= 2
        distance += length
    return distance


def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0


def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """

    # Many searches will explore nodes (or states) that are ordered by their f-value.
    # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
    # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
    # The function must return a numeric f-value.
    # The value will determine your state's position on the Frontier list during a 'custom' search.
    # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
    return sN.gval + (weight * sN.hval)


def anytime_weighted_astar(initial_state, heur_fn, weight=1., timebound=5):
    # IMPLEMENT
    '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''
    se = SearchEngine(strategy='custom', cc_level='full')
    se.init_search(initState=initial_state,
                   goal_fn=snowman_goal_state,
                   heur_fn=heur_fn,
                   fval_function=lambda sN: fval_function(sN, weight))

    costbound = (float("inf"), float("inf"), float("inf"))
    result = se.search(timebound=timebound, costbound=costbound)

    begin = os.times()[0]
    end = begin + timebound
    found = False
    while begin < end:
        # search failed
        if result == False:
            return found

        # prune by the g value
        if result.gval <= costbound[0]:
            found = result
            costbound = (result.gval, result.gval, result.gval*2)

        # calculate remaining time
        timebound -= os.times()[0] - begin
        result = se.search(timebound=timebound, costbound=costbound)

        # update start time
        begin = os.times()[0]
    return found


def anytime_gbfs(initial_state, heur_fn, timebound=5):
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    se = SearchEngine(strategy='best_first', cc_level='full')
    se.init_search(initState=initial_state,
                   goal_fn=snowman_goal_state,
                   heur_fn=heur_fn)

    costbound = (float("inf"), float("inf"), float("inf"))
    result = se.search(timebound=timebound, costbound=costbound)

    begin = os.times()[0]
    end = begin + timebound
    found = False
    while begin < end:
        # search failed
        if result == False:
            return found

        # prune by the g value
        if result.gval <= costbound[0]:
            found = result
            costbound = (result.gval, result.gval, result.gval*2)

        # calculate remaining time
        timebound -= os.times()[0] - begin
        result = se.search(timebound=timebound, costbound=costbound)

        # update start time
        begin = os.times()[0]
    return found
