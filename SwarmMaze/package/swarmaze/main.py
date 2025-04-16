import sys
import pygame
from .maze import Maze
from .visualizer import Visualizer
from .algorithms import DFS, BFS, AStar, Dijkstra, GreedyBestFirst, RandomWalk, BidirectionalSearch, IterativeDeepeningDFS, HillClimbing


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python main.py maze.txt [dfs|bfs|astar|dijkstra|greedy|randomwalk|bidirectional|iddfs|hillclimbing]")

    filename = sys.argv[1]
    algorithm = sys.argv[2].lower()

    # Load the maze
    maze = Maze(filename)

    # Initialize the visualizer with a delay of 200ms
    visualizer = Visualizer(maze, delay=200)

    # Choose the algorithm
    if algorithm == "dfs":
        solver = DFS(maze, visualizer)
    elif algorithm == "bfs":
        solver = BFS(maze, visualizer)
    elif algorithm == "astar":
        solver = AStar(maze, visualizer)
    elif algorithm == "dijkstra":
        solver = Dijkstra(maze, visualizer)
    elif algorithm == "greedy":
        solver = GreedyBestFirst(maze, visualizer)
    elif algorithm == "randomwalk":
        solver = RandomWalk(maze, visualizer)
    elif algorithm == "bidirectional":
        solver = BidirectionalSearch(maze, visualizer)
    elif algorithm == "iddfs":
        solver = IterativeDeepeningDFS(maze, visualizer)
    elif algorithm == "hillclimbing":
        solver = HillClimbing(maze, visualizer)
    else:
        sys.exit("Invalid algorithm. Choose 'dfs', 'bfs', 'astar', 'dijkstra', 'greedy', 'randomwalk', 'bidirectional', 'iddfs', or 'hillclimbing'.")

    print("Solving...")
    try:
        # Solve the maze and visualize the solution
        actions, cells = solver.solve()
        visualizer.draw_maze(solution=cells)
        print("Solution found!")
    except Exception as e:
        print(f"Error: {e}")

    # Wait for the user to close the visualization window
    visualizer.wait_for_exit()


if __name__ == "__main__":
    pygame.init()
    main()