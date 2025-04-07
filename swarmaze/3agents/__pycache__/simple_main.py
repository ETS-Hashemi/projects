import sys
from simple_maze import SimpleMaze, SimpleVisualizer, PATH_COLORS

def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        sys.exit("Usage: python simple_main.py maze4_3a.txt [algorithm]")
    
    # Get maze file from command line
    maze_file = sys.argv[1]
    
    # Get algorithm choice (default to BFS)
    algorithm = "bfs"
    if len(sys.argv) > 2:
        algorithm = sys.argv[2].lower()
    
    print(f"Loading maze from {maze_file}...")
    print(f"Using {algorithm.upper()} search algorithm")
    
    # Create maze and visualizer
    maze = SimpleMaze(maze_file)
    visualizer = SimpleVisualizer(maze)
    
    # Calculate paths for all agents with collision avoidance
    # and collect exploration traces for visualization
    agent_paths = []
    agent_ids = []
    exploration_traces = []
    reservation = {}  # Time-based reservation table for collision avoidance
    
    # Plan paths in order (priority by agent ID)
    for agent_id in range(1, 4):
        if agent_id in maze.starts:
            start = maze.starts[agent_id]
            
            # Choose algorithm based on user selection
            if algorithm == "astar":
                path, exploration = maze.find_path_with_astar_and_trace(start, maze.goal, reservation)
            elif algorithm == "greedy":
                # Use greedy for path finding, but trace not implemented
                path = maze.find_path_greedy(start, maze.goal)
                # For trace, use BFS exploration pattern (simplified)
                _, exploration = maze.find_path_with_reservation_and_trace(start, maze.goal, {})
            else:  # Default to BFS
                path, exploration = maze.find_path_with_reservation_and_trace(start, maze.goal, reservation)
            
            # Update reservation table with this agent's path
            for t, pos in enumerate(path):
                if (pos, t) not in reservation:
                    reservation[(pos, t)] = agent_id
            
            agent_paths.append(path)
            agent_ids.append(agent_id)
            exploration_traces.append(exploration)
            print(f"Agent {agent_id} path length: {len(path)}, explored {len(exploration)} cells")
    
    # Run visualization showing both exploration and final paths
    print("Starting visualization of path finding process...")
    visualizer.visualize_exploration(agent_ids, exploration_traces, agent_paths)
    
    print("Visualization complete.")

if __name__ == "__main__":
    main()