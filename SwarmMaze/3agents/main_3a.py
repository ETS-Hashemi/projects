import sys
import pygame
from maze import Maze, PathFinder, Visualizer, PATH_COLORS

def main():
    # Check command line arguments
    if len(sys.argv) < 2:
        sys.exit("Usage: python main_3a.py maze4_3a.txt [algorithm]")
    
    # Get maze file from command line
    maze_file = sys.argv[1]
    
    # Get algorithm choice (default to BFS)
    algorithm = "bfs"
    if len(sys.argv) > 2:
        algorithm = sys.argv[2].lower()
    
    print(f"Loading maze from {maze_file}...")
    print(f"Using {algorithm.upper()} search algorithm")
    
    # Create maze, pathfinder and visualizer
    maze = Maze(maze_file)
    pathfinder = PathFinder(maze)
    visualizer = Visualizer(maze)
    
    # Calculate paths for all agents with collision avoidance
    agent_paths = []
    agent_ids = []
    exploration_traces = []
    reservation = {}  # Time-based reservation table
    
    # Plan paths in order (priority by agent ID)
    for agent_id in range(1, 4):
        if agent_id in maze.starts:
            start = maze.starts[agent_id]
            
            # Find path using selected algorithm
            path, exploration = pathfinder.find_path(algorithm, start, maze.goal, reservation)
            
            # Update reservation table with this agent's path
            for t, pos in enumerate(path):
                reservation[(pos, t)] = agent_id
            
            agent_paths.append(path)
            agent_ids.append(agent_id)
            exploration_traces.append(exploration)
            print(f"Agent {agent_id} path length: {len(path)}, explored {len(exploration)} cells")
    
    # Debugging: Check if exploration_traces is empty
    if not exploration_traces:
        print("Error: No exploration traces generated. Check the search algorithm.")
        return
    
    # Run visualization
    print("Starting visualization of path finding process...")
    visualizer.visualize_exploration(agent_ids, exploration_traces, agent_paths)
    
    print("Visualization complete.")

if __name__ == "__main__":
    main()