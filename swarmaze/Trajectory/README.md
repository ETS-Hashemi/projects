# 🧠 Swarmaze — Trajectory Module

This module contains the core logic and visualization tools for executing a variety of search algorithms on grid-based mazes using **Pygame**.

---

## 📁 Contents

### `main.py`
- Command-line entry point.
- Usage:  
  ```bash
  python main.py maze.txt [algorithm]
  ```
  Where `algorithm` is one of:
  ```
  dfs | bfs | astar | dijkstra | greedy | randomwalk | bidirectional | iddfs | hillclimbing
  ```
- Loads a maze from a text file and runs the selected algorithm with real-time visual feedback.

### `maze.py`
- Defines the maze structure and search utilities:
  - `Maze`: parses a maze from file and handles wall logic, neighbors, and start/goal detection.
  - `Node`: state object used in all search algorithms, including support for cost and heuristics.
  - `StackFrontier`, `QueueFrontier`: LIFO/FIFO data structures for DFS and BFS.

### `algorithms.py`
- Implements multiple pathfinding/search algorithms, each as a class with a `.solve()` method.
- Algorithms:
  - ✅ **DFS** (Depth-First Search)
  - ✅ **BFS** (Breadth-First Search)
  - ✅ **A\*** (A-Star with Manhattan heuristic)
  - ✅ **Dijkstra** (Uniform Cost Search)
  - ✅ **Greedy Best-First Search**
  - ✅ **Random Walk** (non-deterministic, limited by max steps)
  - ✅ **Bidirectional Search** (from start and goal simultaneously)
  - ✅ **Iterative Deepening DFS**
  - ✅ **Hill Climbing** (greedy with local minimum risk)

### `visualizer.py`
- Renders the maze and algorithm progress using color-coded cells:
  - Red: start
  - Green: goal
  - White: wall
  - Yellow: explored
  - Blue: current agent
  - Purple: final path
- Handles user window interaction and frame delay for step-by-step animation.

---

## ▶️ How to Run

Make sure `pygame` is installed:

```bash
pip install pygame
```

Then run from the `trajectory/` directory:

```bash
python main.py maze.txt astar
```

Replace `astar` with any other supported algorithm name.

The maze file should:
- Use `"A"` for the **start**
- Use `"B"` for the **goal**
- Use `" "` for open paths
- Use any other character (e.g. `"#"`) for **walls**

Example `maze.txt`:
```
##########
#A     #B#
# ### ####
#        #
##########
```

---

## 🔍 Notes

- All algorithms visualize explored cells in real-time.
- Algorithms are modular and interchangeable.
- Maze parsing and neighbor handling is decoupled from the algorithm code.
- Visualization delay is adjustable in `Visualizer(delay=200)` (in ms).

---

## 💡 Extension Ideas

- Support diagonal movement and custom cost maps
- Add multi-agent planning support
- Export solution metrics and runtime stats
- Integrate dynamic obstacle updates (e.g. for replanning)
