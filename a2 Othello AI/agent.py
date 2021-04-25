"""
An AI player for Othello.

My heuristic for compute_heuristic:
I use the sum of the utility function and a score related to corners as my heuristic.
Since the disks at a corner or the disks surrounding it cannot be flipped,
it is beneficial for the player to place the disks there.
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

min_dict = dict()
max_dict = dict()
beta_dict = dict()
alpha_dict = dict()


def eprint(*args, **kwargs):  # you can use this for debugging, as it will print to sterr and not stdout
    print(*args, file=sys.stderr, **kwargs)


def pretty_print_board(board):
    """
    Return a string representing the board and the disks 
    """
    line = "-" * (2 * (len(board) - 1) + 5) + "\n"
    all_str = line
    for row in board:
        all_str += "| "
        for element in row:
            if element == 0:
                all_str += ". "
            else:
                all_str += str(element) + " "
        all_str += "|\n"
    all_str += line
    return all_str


def compute_utility(board, color):
    """
    Method to compute utility value of terminal state
    """
    # IMPLEMENT
    p1_count, p2_count = get_score(board)
    if color == 1:
        utility = p1_count - p2_count
    else:
        utility = p2_count - p1_count
    return utility


# Better heuristic value of board


def count_corners(board, color):
    """
    Count the number of disks of the given color at and near corners
    """
    # IMPLEMENT
    end = len(board) - 1
    corners = [(0, 0), (0, end), (end, 0), (end, end)]
    count = 0
    for c in corners:
        # advantagous to be at corner
        if board[c[0]][c[1]] == color:
            count += 1 + count_corner_adjacent(board, color, c, end)
        # disadvantagous to have opponent at corner
        elif board[c[0]][c[1]] == 3 - color:
            count -= 2
    return count


def is_within_range(position, end):
    """
    Return True if the position is within the dimensions of the board
    """
    return 0 <= position[0] <= end and 0 <= position[1] <= end


def count_corner_adjacent(board, color, corner, end):
    """
    Count the number of disks of the same color next to
    a occupied corner along walls
    """
    count = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    position = corner
    for d in directions:
        while True:
            # elementwise tuple addition e.g. (a, b) + (c, d) = (a + c, b + d)
            position = tuple(map(sum, zip(position, d)))
            if is_within_range(position, end) and board[position[0]][position[1]] == color:
                count += 1
            else:
                break
        # reset position for other directions
        position = corner
    return count


def compute_heuristic(board, color):
    """
    Please see the top of this file for explanation of my heuristic.
    """
    # IMPLEMENT
    return compute_utility(board, color) * 2 + count_corners(board, color)

############ MINIMAX ###############################


def minimax_min_node(board, color, limit, caching=0):
    # IMPLEMENT
    if caching and (board, 3 - color) in min_dict:
        return min_dict[(board, 3 - color)]
    min_val, min_node = float("Inf"), None
    moves = get_possible_moves(board, 3 - color)
    # if at depth limit or no more moves left
    if limit < 1 or moves == []:
        return min_node, compute_utility(board, color)
    for mv in moves:
        after = play_move(board, 3 - color, mv[0], mv[1])
        val = minimax_max_node(after, color, limit - 1, caching)[1]
        if val < min_val:
            min_val, min_node = val, mv
    if caching:
        min_dict[(board, 3 - color)] = min_node, min_val
    return min_node, min_val


def minimax_max_node(board, color, limit, caching=0):  # returns highest possible utility
    # IMPLEMENT
    if caching and (board, color) in max_dict:
        return max_dict[(board, color)]
    max_val, max_node = float("-Inf"), None
    moves = get_possible_moves(board, color)
    # if at depth limit or no more moves left
    if limit < 1 or moves == []:
        return max_node, compute_utility(board, color)
    for mv in moves:
        after = play_move(board, color, mv[0], mv[1])
        val = minimax_min_node(after, color, limit - 1, caching)[1]
        if val > max_val:
            max_val, max_node = val, mv
    if caching:
        max_dict[(board, color)] = max_node, max_val
    return max_node, max_val


def select_move_minimax(board, color, limit, caching=0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    """
    # IMPLEMENT
    return minimax_max_node(board, color, limit, caching)[0]

############ ALPHA-BETA PRUNING #####################


def sort_board_list(board, color, moves):
    # get a board from each move
    board_list = map(lambda mv: play_move(board, color, mv[0], mv[1]), moves)
    # sort by negative utility
    return sorted(board_list, key=lambda board: -compute_utility(board, color))


def alphabeta_min_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    # IMPLEMENT
    if caching and (board, 3 - color) in beta_dict:
        return beta_dict[(board, 3 - color)]
    min_val, min_node = float("Inf"), None
    moves = get_possible_moves(board, 3 - color)
    # if at depth limit or no more moves left
    if limit < 1 or moves == []:
        return min_node, compute_utility(board, color)
    if ordering:
        board_list = sort_board_list(board, color, moves)
    for i in range(len(moves)):
        if ordering:
            val = alphabeta_max_node(
                board_list[i], color, alpha, beta, limit - 1, caching, ordering)[1]
        else:
            after = play_move(board, 3 - color, moves[i][0], moves[i][1])
            val = alphabeta_max_node(
                after, color, alpha, beta, limit - 1, caching, ordering)[1]
        if val < min_val:
            min_val, min_node = val, moves[i]
        if min_val < beta:
            beta = min_val
        if beta <= alpha:  # prune
            break
    if caching:
        beta_dict[(board, 3 - color)] = min_node, min_val
    return min_node, min_val


def alphabeta_max_node(board, color, alpha, beta, limit, caching=0, ordering=0):
    # IMPLEMENT
    if caching and (board, color) in alpha_dict:
        return alpha_dict[(board, color)]
    max_val, max_node = float("-Inf"), None
    moves = get_possible_moves(board, color)
    # if at depth limit or no more moves left
    if limit < 1 or moves == []:
        return max_node, compute_utility(board, color)
    if ordering:
        board_list = sort_board_list(board, color, moves)
    for i in range(len(moves)):
        if ordering:
            val = alphabeta_min_node(
                board_list[i], color, alpha, beta, limit - 1, caching, ordering)[1]
        else:
            after = play_move(board, color, moves[i][0], moves[i][1])
            val = alphabeta_min_node(
                after, color, alpha, beta, limit - 1, caching, ordering)[1]
        if val > max_val:
            max_val, max_node = val, moves[i]
        if max_val > alpha:
            alpha = max_val
        if beta <= alpha:  # prune
            break
    if caching:
        alpha_dict[(board, color)] = max_node, max_val
    return max_node, max_val


def select_move_alphabeta(board, color, limit, caching=0, ordering=0):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.

    Note that other parameters are accepted by this function:
    If limit is a positive integer, your code should enfoce a depth limit that is equal to the value of the parameter.
    Search only to nodes at a depth-limit equal to the limit.  If nodes at this level are non-terminal return a heuristic
    value (see compute_utility)
    If caching is ON (i.e. 1), use state caching to reduce the number of state evaluations.
    If caching is OFF (i.e. 0), do NOT use state caching to reduce the number of state evaluations.
    If ordering is ON (i.e. 1), use node ordering to expedite pruning and reduce the number of state evaluations.
    If ordering is OFF (i.e. 0), do NOT use node ordering to expedite pruning and reduce the number of state evaluations.
    """
    # IMPLEMENT
    return alphabeta_max_node(board, color, float("-Inf"), float("Inf"), limit, caching, ordering)[0]

####################################################


def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Othello AI")  # First line is the name of this AI
    arguments = input().split(",")

    # Player color: 1 for dark (goes first), 2 for light.
    color = int(arguments[0])
    limit = int(arguments[1])  # Depth limit
    minimax = int(arguments[2])  # Minimax or alpha beta
    caching = int(arguments[3])  # Caching
    ordering = int(arguments[4])  # Node-ordering (for alpha-beta only)

    if (minimax == 1):
        eprint("Running MINIMAX")
    else:
        eprint("Running ALPHA-BETA")

    if (caching == 1):
        eprint("State Caching is ON")
    else:
        eprint("State Caching is OFF")

    if (ordering == 1):
        eprint("Node Ordering is ON")
    else:
        eprint("Node Ordering is OFF")

    if (limit == -1):
        eprint("Depth Limit is OFF")
    else:
        eprint("Depth Limit is ", limit)

    if (minimax == 1 and ordering == 1):
        eprint("Node Ordering should have no impact on Minimax")

    while True:  # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL":  # Game is over.
            print
        else:
            # Read in the input and turn it into a Python
            board = eval(input())
            # object. The format is a list of rows. The
            # squares in each row are represented by
            # 0 : empty square
            # 1 : dark disk (player 1)
            # 2 : light disk (player 2)

            # Select the move and send it to the manager
            if (minimax == 1):  # run this if the minimax flag is given
                movei, movej = select_move_minimax(
                    board, color, limit, caching)
            else:  # else run alphabeta
                movei, movej = select_move_alphabeta(
                    board, color, limit, caching, ordering)

            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
