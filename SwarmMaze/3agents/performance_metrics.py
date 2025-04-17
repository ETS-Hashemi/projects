import sys
from maze import Maze, PathFinder
from reservation import ReservationTable

class PerformanceMetrics:
    """Class to calculate performance metrics for multi-agent pathfinding."""
    def __init__(self, maze, algorithm):
        self.maze = maze
        self.algorithm = algorithm
        self.pathfinder = PathFinder(maze)
        self.reservation = ReservationTable()

    def measure(self):
        """Measure performance metrics for all agents."""
        agent_metrics = []
        for agent_id, start in self.maze.starts.items():
            # Find path using the specified algorithm
            path, exploration = self.pathfinder.find_path(self.algorithm, start, self.maze.goal, self.reservation)

            # Update reservation table with the agent's path
            for t, pos in enumerate(path):
                self.reservation.add_reservation(pos, t, agent_id)

            # Collect metrics for the agent
            agent_metrics.append({
                "agent_id": agent_id,
                "path_length": len(path),
                "explored_cells": len(exploration),
            })

        return agent_metrics

def main():
    # Check command line arguments
    if len(sys.argv) < 3:
        sys.exit("Usage: python performance_metrics.py maze_file algorithm")

    maze_file = sys.argv[1]
    algorithm = sys.argv[2].lower()

    print(f"Loading maze from {maze_file}...")
    print(f"Using {algorithm.upper()} search algorithm")

    # Load the maze
    maze = Maze(maze_file)

    # Calculate performance metrics
    metrics_calculator = PerformanceMetrics(maze, algorithm)
    metrics = metrics_calculator.measure()

    # Print performance metrics
    print("==================================================")
    print(f"Performance Metrics for Algorithm: {algorithm.upper()}")
    print("==================================================")
    print(f"Total Agents: {len(metrics)}")
    print("--------------------------------------------------")
    print("Agent     Path Length    Explored Cells")
    print("--------------------------------------------------")
    for metric in metrics:
        print(f"{metric['agent_id']:>5} {metric['path_length']:>15} {metric['explored_cells']:>15}")
    print("==================================================")

if __name__ == "__main__":
    main()
