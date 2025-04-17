# 3Agents Maze Solver

The **3Agents Maze Solver** is a Python-based project designed to solve multi-agent pathfinding problems in a maze environment. It supports various search algorithms and visualizes the agents' exploration and pathfinding processes. The project is built with flexibility to handle multiple agents, collision avoidance, and customizable algorithms.

---

## Screenshot

<p align="center">
  <img src="./Screenshot_3.gif" alt="Visualization of 3Agents Maze Solver in action" width="500"/>
</p>

---

## Features

- **Multi-Agent Pathfinding**:
  - Supports up to three agents navigating the maze simultaneously.
  - Implements a robust **collision avoidance mechanism** using a time-based reservation table.

- **Search Algorithms**:
  - **Breadth-First Search (BFS)**: Guarantees the shortest path and explores all possible paths systematically.
  - **Depth-First Search (DFS)**: Explores paths deeply but does not guarantee the shortest path.
  - **A* Search**: Combines path cost and heuristic to find the optimal path efficiently.
  - **Greedy Best-First Search**: Uses a heuristic to prioritize exploration but does not guarantee optimality.
  - **Dijkstra's Algorithm**: Guarantees the shortest path by exploring all possible paths with minimal cost.
  - **Bidirectional Search**: Searches from both the start and goal positions to reduce exploration time.
  - **Iterative Deepening DFS (IDDFS)**: Combines the benefits of DFS and BFS by incrementally increasing the search depth.

- **Visualization**:
  - Displays the maze, agents' paths, and collision avoidance in real-time using `pygame`.
  - Highlights reserved cells, collisions, and shared paths for better understanding.

- **Performance Metrics**:
  - Measures path length and the number of explored cells for each agent.

- **Customizable Configuration**:
  - Centralized configuration for colors, cell size, and default algorithms in `config.py`.

---

## File Structure

### Code Structure Overview

| File                     | Description                                                                 |
|--------------------------|-----------------------------------------------------------------------------|
| `main_3a.py`             | Main entry point for solving the maze and visualizing the solution.         |
| `collision_visualizer.py`| Visualizes the collision avoidance mechanism step by step.                  |
| `maze.py`                | Core logic for parsing the maze and integrating pathfinding algorithms.     |
| `algorithms.py`          | Implements various search algorithms (BFS, DFS, A*, Greedy, etc.).         |
| `reservation.py`         | Manages the reservation table for collision avoidance.                     |
| `config.py`              | Centralized configuration for colors, cell size, and algorithm defaults.   |
| `performance_metrics.py` | Measures and reports performance metrics for multi-agent pathfinding.       |
| `maze4_3a.txt`           | Example maze file defining the maze structure.                             |

---

## Algorithm Comparison

| Algorithm               | Optimality | Completeness | Time Complexity | Space Complexity |
|--------------------------|------------|--------------|------------------|------------------|
| **BFS**                 | Yes        | Yes          | O(b^d)          | O(b^d)          |
| **DFS**                 | No         | Yes          | O(b^m)          | O(b*m)          |
| **A***                  | Yes        | Yes          | O(b^d)          | O(b^d)          |
| **Greedy**              | No         | No           | O(b^d)          | O(b^d)          |
| **Dijkstra's**          | Yes        | Yes          | O(b^2)          | O(b^2)          |
| **Bidirectional Search**| No         | Yes          | O(b^(d/2))       | O(b^(d/2))       |
| **Iterative Deepening** | No         | Yes          | O(b^d)          | O(d*b)          |

- **Optimality**: Whether the algorithm guarantees the shortest path.
- **Completeness**: Whether the algorithm guarantees finding a solution if one exists.
- **Time Complexity**: `b` is the branching factor, and `d` is the depth of the shallowest solution.
- **Space Complexity**: Memory usage of the algorithm.

---

## Performance Metrics

The project calculates the following performance metrics for each agent:

1. **Path Length**:
   - The total number of steps taken by the agent to reach the goal.

2. **Explored Cells**:
   - The total number of cells explored by the agent during the search process.

### Example Output
```plaintext
==================================================
Performance Metrics for Algorithm: DFS
==================================================
Total Agents: 3
--------------------------------------------------
Agent     Path Length    Explored Cells
--------------------------------------------------
    1             101              250
    2              98              230
    3             105              270
==================================================
```

---

## Collision Avoidance Mechanism

The **3Agents Maze Solver** implements a robust and optimized **collision avoidance mechanism** to ensure that multiple agents can navigate the maze simultaneously without conflicts. This mechanism is seamlessly integrated into the pathfinding algorithms and visualized in `collision_visualizer.py`.

### Reservation Table
The reservation table is implemented in the `reservation.py` file. It is a dedicated class (`ReservationTable`) that manages time-based reservations for collision avoidance.

#### Key Features:
- **Add Reservations**:
  - Reserve a position for a specific agent at a specific time step.
- **Check Reservations**:
  - Verify if a position is reserved at a given time step.
- **Iterate Over Reservations**:
  - Expose reservations as an iterable for debugging or advanced operations.

#### Example Usage:
```python
from reservation import ReservationTable

# Initialize reservation table
reservation = ReservationTable()

# Add reservations
reservation.add_reservation((2, 3), 0, 1)  # Agent 1 reserves position (2, 3) at time 0
reservation.add_reservation((2, 4), 1, 2)  # Agent 2 reserves position (2, 4) at time 1

# Check reservations
print(reservation.is_reserved((2, 3), 0))  # True
print(reservation.is_reserved((2, 5), 0))  # False
```

---

## Future Work

- **Dynamic Agent Prioritization**:
  - Implement dynamic prioritization of agents based on their distance to the goal or other heuristics.

- **Support for Larger Mazes**:
  - Optimize the algorithms to handle larger and more complex mazes efficiently.

- **Integration with Real-World Robotics**:
  - Extend the project to simulate real-world multi-robot pathfinding scenarios.

- **Improved Visualization**:
  - Add more detailed visualizations, such as heatmaps for explored cells or agent-specific animations.

---

## How to Use

### Prerequisites
- Python 3.7 or higher.
- `pygame` library: Install using:
  ```bash
  pip install pygame
  ```

### Running the Project

#### 1. **Using `main_3a.py`**
The `main_3a.py` script calculates paths for all agents, handles collision avoidance, and visualizes the exploration and path execution.

Run the script with the maze file and an optional algorithm:
```bash
python main_3a.py maze4_3a.txt [algorithm]
```

- **Default Algorithm**: If no algorithm is specified, it defaults to `bfs` (Breadth-First Search).
- **Supported Algorithms**: `bfs`, `dfs`, `astar`, `greedy`, `dijkstra`, `bidirectional`, `iddfs`.

#### Example:
To solve the maze using A*:
```bash
python main_3a.py maze4_3a.txt astar
```

#### Output:
- The console will display the path length and explored cells for each agent.
- A `pygame` window will visualize the exploration and path execution.

---

#### 2. **Using `collision_visualizer.py`**
The `collision_visualizer.py` script provides a step-by-step visualization of the collision avoidance mechanism.

Run the script with the maze file and an optional algorithm:
```bash
python collision_visualizer.py maze4_3a.txt [algorithm]
```

- **Default Algorithm**: If no algorithm is specified, it defaults to `bfs` (Breadth-First Search).
- **Supported Algorithms**: `bfs`, `dfs`, `astar`, `greedy`, `dijkstra`, `bidirectional`, `iddfs`.

#### Example:
To visualize the collision avoidance mechanism using Greedy Best-First Search:
```bash
python collision_visualizer.py maze4_3a.txt greedy
```

---

## Customizing the Maze
- Edit `maze4_3a.txt` to define your own maze.
- Use `A1`, `A2`, `A3` for agent start positions and `B` for the goal.
- Use `#` for walls and spaces for open paths.

---

## License

```
Licensed under the Apache License, Version 2.0.
```

---

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests to improve the project.

---

## Acknowledgments
- Inspired by multi-agent pathfinding problems in robotics and AI.
- Built using Python and `pygame` for visualization.

---

## Academic Attribution
This project is developed as part of the PhD research of  
**Seyed Masoud Hashemi Ahmadi**  
at **École de technologie supérieure (ÉTS), Montréal**.

If you use this work in academic research, citation is appreciated.
