"""
compare_algorithms.py
-----------------------
Runs A* Search and Greedy Best-First Search on the SAME initial state
and prints a side-by-side comparison of path cost and nodes expanded.

This is useful for the assignment's analysis/discussion section:
A* is optimal (always finds the lowest-cost path) but may expand more
nodes. Greedy is faster/expands fewer nodes in many cases, but is not
guaranteed to find the shortest path.
"""

from astar_8puzzle import a_star_search
from greedy_8puzzle import greedy_best_first_search
from puzzle_utils import is_solvable, print_state, GOAL_STATE


def compare(initial_state):
    print("Initial State:")
    print_state(initial_state)

    if not is_solvable(initial_state):
        print("This configuration is NOT solvable. Choose another state.")
        return

    _, a_moves, a_cost, a_expanded = a_star_search(initial_state)
    _, g_moves, g_cost, g_expanded = greedy_best_first_search(initial_state)

    print(f"{'Metric':<20}{'A* Search':<20}{'Greedy Search':<20}")
    print("-" * 60)
    print(f"{'Path Cost':<20}{a_cost:<20}{g_cost:<20}")
    print(f"{'Moves':<20}{len(a_moves):<20}{len(g_moves):<20}")
    print(f"{'Nodes Expanded':<20}{a_expanded:<20}{g_expanded:<20}")
    print(f"{'Optimal?':<20}{'Yes (guaranteed)':<20}{'Not guaranteed':<20}")

    print("\nA* Move Sequence:    ", " -> ".join(a_moves))
    print("Greedy Move Sequence:", " -> ".join(g_moves))


if __name__ == "__main__":
    # Try a moderately scrambled state; feel free to change this
    initial_state = (1, 6, 2,
                      5, 3, 0,
                      4, 7, 8)

    compare(initial_state)
