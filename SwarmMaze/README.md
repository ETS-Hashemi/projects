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
│   ├── simulation.py    # Simulation environment for agents
│   ├── collision_visualizer.py  # Visualizes collision avoidance mechanism
│   └── README.md        # Documentation for 3agents module
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
- **Multi-agent pathfinding with collision avoidance**:
  - Uses a **time-based reservation table** to prevent conflicts.
  - Visualized in `collision_visualizer.py`.

---

##  Multi-Agent Pathfinding and Collision Avoidance

The `3agents` module introduces multi-agent pathfinding with a robust **collision avoidance mechanism**. Key features include:

1. **Time-Based Reservation Table**:
   - Ensures no two agents occupy the same position at the same time.
   - Allows agents to "wait in place" if no valid moves are available.

2. **Visualization**:
   - Reserved cells are highlighted in red.
   - Collisions are highlighted in yellow.
   - Agents' paths are color-coded for clarity.

3. **Integration with Algorithms**:
   - Collision avoidance is seamlessly integrated into BFS, A*, and Greedy algorithms.

For more details, refer to the [`3agents/README.md`](./3agents/README.md).

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

For multi-agent pathfinding, navigate to the `3agents/` folder and run:

```bash
python main_3a.py maze4_3a.txt astar
```

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
