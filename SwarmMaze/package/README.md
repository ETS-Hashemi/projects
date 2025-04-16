# Swarmaze

**Swarmaze** is a pathfinding toolkit and visualizer for 2D mazes, featuring real-time animations of multiple search algorithms (DFS, BFS, A*, etc.) using **Pygame**. Originally part of a larger “Trajectory” folder, it’s now a standalone Python package.

---

## 📁 Directory Structure

```
swarmaze/
├── __init__.py            # Makes this a Python package
├── main.py                # CLI / Pygame entry point
├── algorithms.py          # Search algorithms implemented
├── maze.py                # Maze environment & Node definitions
├── visualizer.py          # Visualization logic
├── maze4.txt (optional)   # Sample maze file
└── (other docs, tests, etc.)
```

**Key Files**:

- **main.py**  
  - Entry point for running the visual demo (if you set up `console_scripts`, you can do `swarmaze maze4.txt bfs`).  
- **algorithms.py**  
  - Various search algorithms (DFS, BFS, A*, Dijkstra, Greedy, etc.).  
- **maze.py**  
  - Maze class: handles grid dimensions, start/end cells, neighbors.  
- **visualizer.py**  
  - Renders the maze state in Pygame, color-coding walls, explored cells, and final path.

---

## 🏗️ Installation & Usage

1. **Install** from your local repo (with `setup.py` in the parent directory):
   ```bash
   cd path/to/parent/  # where setup.py is
   pip install .
   ```
   or
   ```bash
   pip install -e .  # for editable mode
   ```

2. **Run** the visualizer (two approaches):

   ### A) If you set up a console script:
   ```bash
   swarmaze maze4.txt bfs
   ```
   where `maze4.txt` is your maze file, and `bfs` is your chosen algorithm.

   ### B) Using the `-m` module approach:
   ```bash
   python -m swarmaze.main maze4.txt astar
   ```

**Maze Format**:
- `'A'` = Start  
- `'B'` = Goal  
- `' '` (space) = Free path  
- Anything else (e.g. `#`) = Wall

**Algorithms** (current selection):
```
dfs | bfs | astar | dijkstra | greedy | randomwalk | bidirectional | iddfs | hillclimbing
```

---

## 🧠 Features

- **Live Pygame animation** of pathfinding progress
- **Nine** out-of-the-box algorithms
- **Easily extendable** by adding new classes to `algorithms.py`
- **Colored** visualization of visited cells, final path, walls, etc.

---

## 🛠 Dev Notes

- **Add new algorithms** by creating a class with a `.solve()` method in `algorithms.py`.  
- **Link** that class in `main.py` if you want it selectable by name (e.g., `"myalgo"` → `MyAlgoClass`).
- **Tweak** the `Visualizer(delay=...)` to slow or speed up animations.

---

## 🏆 License

Apache 2.0

---

## 🙏 Credits / Attribution

- Developed by **Seyed Masoud Hashemi Ahmadi** for PhD research at **ÉTS**.  
- For bug reports or PRs, see the main GitHub repository.

