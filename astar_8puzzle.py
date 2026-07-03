"""
astar_8puzzle.py
-----------------
Solves the 8-Puzzle problem using the A* Search Algorithm.

A* evaluates nodes using:
    f(n) = g(n) + h(n)

where:
    g(n) = actual path cost from the start state to node n
    h(n) = estimated cost (Manhattan distance heuristic) from n to the goal

A* is complete and optimal (guaranteed shortest path cost) as long as the
heuristic used is admissible -- Manhattan distance satisfies this.

Author: <your name>
Course: AI CIA-1 Component 2
"""

import heapq
import itertools
import time

from puzzle_utils import (
    GOAL_STATE,
    is_solvable,
    get_neighbors,
    manhattan_distance,
    print_state,
    reconstruct_path,
)


def a_star_search(start_state, goal_state=GOAL_STATE, heuristic=manhattan_distance):
    """
    Performs A* search from start_state to goal_state.

    Returns:
        path        -> list of states from start to goal
        moves       -> list of moves ('UP', 'DOWN', ...) taken
        path_cost   -> total path cost g(goal)  (= number of moves, since
                        each move has a uniform cost of 1)
        nodes_expanded -> number of nodes popped from the frontier (for analysis)
    """

    if not is_solvable(start_state):
        return None, None, None, 0

    # Tie-breaker counter so heapq never tries to compare states directly
    counter = itertools.count()

    g_score = {start_state: 0}
    f_score = {start_state: heuristic(start_state, goal_state)}

    # Priority queue entries: (f_score, counter, state)
    open_set = [(f_score[start_state], next(counter), start_state)]
    open_set_hash = {start_state}

    came_from = {}
    closed_set = set()

    nodes_expanded = 0

    while open_set:
        _, _, current = heapq.heappop(open_set)
        open_set_hash.discard(current)

        if current == goal_state:
            path, moves = reconstruct_path(came_from, current)
            return path, moves, g_score[current], nodes_expanded

        closed_set.add(current)
        nodes_expanded += 1

        for neighbor, move in get_neighbors(current):
            if neighbor in closed_set:
                continue

            tentative_g = g_score[current] + 1  # uniform step cost = 1

            if tentative_g < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = (current, move)
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal_state)

                if neighbor not in open_set_hash:
                    heapq.heappush(open_set, (f_score[neighbor], next(counter), neighbor))
                    open_set_hash.add(neighbor)

    return None, None, None, nodes_expanded  # No solution found


def run_demo(start_state):
    print("Initial State:")
    print_state(start_state)
    print("Goal State:")
    print_state(GOAL_STATE)

    if not is_solvable(start_state):
        print("This puzzle configuration is NOT solvable.")
        return

    start_time = time.time()
    path, moves, cost, expanded = a_star_search(start_state)
    elapsed = time.time() - start_time

    if path is None:
        print("No solution found.")
        return

    print(f"Solved in {len(moves)} moves using A* Search")
    print(f"Path cost (g): {cost}")
    print(f"Nodes expanded: {expanded}")
    print(f"Time taken: {elapsed:.4f} seconds\n")

    print("Move sequence:", " -> ".join(moves))
    print("\nStep-by-step path:\n")
    for step, state in enumerate(path):
        print(f"Step {step}:")
        print_state(state)


if __name__ == "__main__":
    # Example initial state (change this to test other puzzles)
    # 1 2 3
    # 4 _ 6
    # 7 5 8
    initial_state = (1, 2, 3,
                      4, 0, 6,
                      7, 5, 8)

    run_demo(initial_state)
