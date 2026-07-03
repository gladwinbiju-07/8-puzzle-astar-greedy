"""
greedy_8puzzle.py
-------------------
Solves the 8-Puzzle problem using the Greedy Best-First Search Algorithm.

Greedy Best-First Search evaluates nodes using only the heuristic:
    f(n) = h(n)

It always expands the node that *looks* closest to the goal, ignoring
the cost already spent (g(n)). This makes it faster than A* in many
cases, but it is NOT guaranteed to find the optimal (shortest) path --
it only guarantees *a* solution (given the heuristic is well-behaved
and the state space is finite), not the cheapest one.

We still track g(n) (path cost) alongside the search purely for
reporting the final path cost of the solution found.

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


def greedy_best_first_search(start_state, goal_state=GOAL_STATE, heuristic=manhattan_distance):
    """
    Performs Greedy Best-First Search from start_state to goal_state.

    Returns:
        path        -> list of states from start to goal
        moves       -> list of moves ('UP', 'DOWN', ...) taken
        path_cost   -> total path cost of the solution found (number of moves)
        nodes_expanded -> number of nodes popped from the frontier (for analysis)
    """

    if not is_solvable(start_state):
        return None, None, None, 0

    counter = itertools.count()

    # Priority queue entries: (h_score, counter, state)
    open_set = [(heuristic(start_state, goal_state), next(counter), start_state)]
    open_set_hash = {start_state}

    came_from = {}
    g_score = {start_state: 0}      # tracked only to report path cost at the end
    visited = set()

    nodes_expanded = 0

    while open_set:
        _, _, current = heapq.heappop(open_set)
        open_set_hash.discard(current)

        if current == goal_state:
            path, moves = reconstruct_path(came_from, current)
            return path, moves, g_score[current], nodes_expanded

        if current in visited:
            continue
        visited.add(current)
        nodes_expanded += 1

        for neighbor, move in get_neighbors(current):
            if neighbor in visited:
                continue

            # Greedy search does not compare/update based on g(n);
            # it simply expands unseen nodes by heuristic value.
            if neighbor not in g_score:
                came_from[neighbor] = (current, move)
                g_score[neighbor] = g_score[current] + 1

                if neighbor not in open_set_hash:
                    heapq.heappush(
                        open_set,
                        (heuristic(neighbor, goal_state), next(counter), neighbor),
                    )
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
    path, moves, cost, expanded = greedy_best_first_search(start_state)
    elapsed = time.time() - start_time

    if path is None:
        print("No solution found.")
        return

    print(f"Solved in {len(moves)} moves using Greedy Best-First Search")
    print(f"Path cost (g): {cost}")
    print(f"Nodes expanded: {expanded}")
    print(f"Time taken: {elapsed:.4f} seconds\n")

    print("Move sequence:", " -> ".join(moves))
    print("\nStep-by-step path:\n")
    for step, state in enumerate(path):
        print(f"Step {step}:")
        print_state(state)


if __name__ == "__main__":
    # Example initial state (same as A* demo, so you can directly compare results)
    # 1 2 3
    # 4 _ 6
    # 7 5 8
    initial_state = (1, 2, 3,
                      4, 0, 6,
                      7, 5, 8)

    run_demo(initial_state)
