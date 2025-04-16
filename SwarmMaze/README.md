#  Swarmaze

**Swarmaze** is a Python-based visualizer for classical pathfinding algorithms in 2D grid mazes.  
It lays the groundwork for advanced systems in **3D multi-agent trajectory planning**, intended for AI agents, robotics, and swarm simulations.

---

##  Repository Structure

```
swarmaze/
├── trajectory/          # Core pathfinding logic and visualizer
│   ├── main.py          # Entry point for the visualizer
│   ├── maze.py          # Maze representation and utilities
│   ├── algorithms.py    # Implementation of pathfinding algorithms
│   └── visualizer.py    # Pygame-based visualization logic
├── map/                 # Tools for procedural map/maze generation
├── 3agents/             # Multi-agent pathfinding and coordination logic
│   ├── agent.py         # Agent behavior and properties
│   ├── coordination.py  # Multi-agent coordination strategies
│   └── simulation.py    # Simulation environment for agents
├── temp/                # Temporary or runtime files
├── text.txt             # Project notes and design documentation
├── LICENSE              # Apache 2.0 License
└── README.md
```

---

##  Features

- Real-time pathfinding visualizer using **Pygame**
- Implements **A\***, **BFS**, **DFS**, and **UCS**
- Modular and clean architecture
- Designed for extensibility to 3D and multi-agent systems
- Interactive algorithm selection via buttons

---

##  Algorithms Implemented

| Algorithm               | Type                  | Optimal? | Complete? |
|-------------------------|-----------------------|----------|-----------|
| A*                      | Heuristic search      |    Yes   |   Yes    |
| BFS                     | Uninformed search     |    Yes   |   Yes    |
| DFS                     | Uninformed search     |    Yes   |   No     |
| UCS                     | Cost-based search     |    Yes   |   Yes    |
| Dijkstra                | Cost-based search     |    Yes   |   Yes    |
| Greedy Best-First       | Heuristic search      |    No    |   No     |
| Random Walk             | Randomized search     |    No    |   No     |
| Bidirectional Search    | Bidirectional search  |    Yes   |   Yes    |
| Iterative Deepening DFS | Depth-limited search  |    Yes   |   Yes    |
| Hill Climbing           | Heuristic search      |    No    |   No     |

---

##  Roadmap

- [ ] Procedural maze generation (`map/`)
- [ ] Multi-agent pathfinding and coordination
- [ ] 3D simulation engine
- [ ] Performance benchmarking tools
- [ ] Swarm behavior and collision resolution

---

##  Requirements

- Python 3.x
- [`pygame`](https://www.pygame.org/)

Install with:

```bash
pip install pygame
```

---

##  How to Run

Navigate to the `trajectory/` folder and run:

```bash
python main.py
```

A window will open. Use the UI buttons to run pathfinding algorithms and visualize their steps.

---

##  Academic Attribution

This project is developed as part of the PhD research of  
**Seyed Masoud Hashemi Ahmadi**  
at **École de technologie supérieure (ÉTS), Montréal**.

If you use this work in academic research, citation is appreciated.

---

##  License

This project is licensed under the [Apache License 2.0](./LICENSE).  
Please refer to the LICENSE file for legal details.
