"""
puzzle_utils.py
----------------
Shared helper functions for the 8-Puzzle problem, used by both
astar_8puzzle.py and greedy_8puzzle.py

The puzzle state is represented as a tuple of 9 integers (0-8),
read row-wise, where 0 represents the blank tile.

Example state (goal state):
    (1, 2, 3,
     4, 5, 6,
     7, 8, 0)
"""

GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


def is_solvable(state):
    """
    Checks whether a given 8-puzzle configuration is solvable.
    A state is solvable if the number of 'inversions' in the tile
    sequence (ignoring the blank) is even.
    """
    tiles = [t for t in state if t != 0]
    inversions = 0
    for i in range(len(tiles)):
        for j in range(i + 1, len(tiles)):
            if tiles[i] > tiles[j]:
                inversions += 1
    return inversions % 2 == 0


def get_blank_position(state):
    return state.index(0)


def get_neighbors(state):
    """
    Returns a list of (new_state, move_name) tuples reachable
    from the given state by sliding one tile into the blank.
    """
    neighbors = []
    blank = get_blank_position(state)
    row, col = divmod(blank, 3)

    moves = {
        "UP": (row - 1, col),
        "DOWN": (row + 1, col),
        "LEFT": (row, col - 1),
        "RIGHT": (row, col + 1),
    }

    for move_name, (new_row, new_col) in moves.items():
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_blank = new_row * 3 + new_col
            new_state = list(state)
            new_state[blank], new_state[new_blank] = new_state[new_blank], new_state[blank]
            neighbors.append((tuple(new_state), move_name))

    return neighbors


def manhattan_distance(state, goal=GOAL_STATE):
    """
    Heuristic h(n): sum of Manhattan distances of every tile
    (except the blank) from its current position to its goal position.
    This heuristic is admissible and consistent, making it ideal for A*.
    """
    distance = 0
    for value in range(1, 9):
        current_index = state.index(value)
        goal_index = goal.index(value)

        cur_row, cur_col = divmod(current_index, 3)
        goal_row, goal_col = divmod(goal_index, 3)

        distance += abs(cur_row - goal_row) + abs(cur_col - goal_col)
    return distance


def misplaced_tiles(state, goal=GOAL_STATE):
    """
    Alternative heuristic: counts tiles that are not in their goal position
    (blank tile excluded). Weaker heuristic than Manhattan distance,
    but included here as an option.
    """
    return sum(1 for i in range(9) if state[i] != 0 and state[i] != goal[i])


def print_state(state):
    for i in range(0, 9, 3):
        row = state[i:i + 3]
        print(" ".join(str(x) if x != 0 else "_" for x in row))
    print()


def reconstruct_path(came_from, current):
    """
    Walks backward through the came_from map to build the
    sequence of states (and moves) from start to goal.
    """
    path = [current]
    moves = []
    while current in came_from:
        current, move = came_from[current]
        path.append(current)
        moves.append(move)
    path.reverse()
    moves.reverse()
    return path, moves
