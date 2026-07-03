# 8-Puzzle Solver — A* and Greedy Best-First Search

AI CIA-1, Component 2 Assignment.

This project solves the classic **8-tile puzzle** using two informed search
algorithms and reports the **path cost** to reach the goal state from any
solvable initial state.

- `astar_8puzzle.py` — solves the puzzle using **A\* Search** (`f(n) = g(n) + h(n)`)
- `greedy_8puzzle.py` — solves the puzzle using **Greedy Best-First Search** (`f(n) = h(n)`)
- `puzzle_utils.py` — shared helpers: move generation, Manhattan-distance
  heuristic, solvability check, path reconstruction
- `compare_algorithms.py` — runs both algorithms on the same initial state
  and prints a side-by-side comparison table

## Problem representation

The board is represented as a flat tuple of 9 integers (`0` = blank), read
row by row:

```
1 2 3        (1, 2, 3,
4 5 6   -->   4, 5, 6,
7 8 _         7, 8, 0)
```

Goal state:

```
1 2 3
4 5 6
7 8 _
```

## Heuristic used

**Manhattan distance** — sum, over all tiles, of the distance (in grid
moves) between a tile's current position and its goal position. This
heuristic is admissible (never overestimates), which is what makes A*
optimal on this problem.

## How to run

```bash
python3 astar_8puzzle.py
python3 greedy_8puzzle.py
python3 compare_algorithms.py
```

Each script prints:
- the initial and goal states
- the sequence of moves (UP/DOWN/LEFT/RIGHT of the blank tile)
- the **path cost** (number of moves, since each move costs 1)
- the number of nodes expanded
- the full step-by-step board states from start to goal

To try your own puzzle, edit the `initial_state` tuple at the bottom of
`astar_8puzzle.py` / `greedy_8puzzle.py` (or pass one into
`compare_algorithms.py`).

## A* vs Greedy — key takeaway

| | A* Search | Greedy Best-First Search |
|---|---|---|
| Evaluation function | `f(n) = g(n) + h(n)` | `f(n) = h(n)` |
| Uses path cost so far? | Yes | No |
| Optimal (shortest path guaranteed)? | Yes, with an admissible heuristic | No |
| Typically expands fewer/more nodes? | More nodes, but shortest path | Often fewer nodes, but path can be longer |

Running `compare_algorithms.py` on various scrambled states shows this in
practice: Greedy often reaches the goal after expanding far fewer nodes,
but its path cost can be significantly higher than A*'s optimal cost.

## Solvability check

Not every arrangement of the 8-puzzle is solvable. Both scripts check the
number of inversions in the tile sequence before searching; if the count
is odd, the state is unsolvable and the script reports this instead of
searching forever.
