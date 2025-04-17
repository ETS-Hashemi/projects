import pygame
import sys
import heapq
from collections import deque
from algorithms import BFS, DFS, AStar, Greedy, Dijkstra, BidirectionalSearch, IterativeDeepeningDFS

# Colors
WHITE = (255, 255, 255)   # Wall
BLACK = (0, 0, 0)         # Background
GREEN = (0, 255, 0)       # Goal
RED = (255, 0, 0)         # Start
BLUE = (0, 0, 255)        # Default agent color

# Agent colors
AGENT_COLORS = {
    1: (0, 0, 255),       # Blue
    2: (255, 165, 0),     # Orange
    3: (128, 0, 128)      # Purple
}

# Path colors
PATH_COLORS = {
    1: (100, 100, 255),   # Light blue
    2: (255, 200, 100),   # Light orange
    3: (200, 100, 200)    # Light purple
}

# Shared path color
SHARED_PATH_COLOR = (150, 150, 150)  # Gray

# Cell size in pixels
CELL_SIZE = 30

class Maze:
    """Class to represent and parse a maze from a file"""
    def __init__(self, filename):
        # Read maze file
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
        
        # Calculate the width
        self.height = len(lines)
        self.width = max(len(line.replace('A1', ' ').replace('A2', ' ').replace('A3', ' ')) for line in lines)
        
        # Parse maze structure
        self.walls = []
        self.starts = {}
        self.goal = None
        
        for i, line in enumerate(lines):
            row = []
            col_index = 0  # Actual grid column index
            
            j = 0  # Character index in the original line
            while j < len(line):
                if j < len(line) - 1 and line[j:j+2] in ['A1', 'A2', 'A3']:
                    agent_num = int(line[j+1])
                    self.starts[agent_num] = (i, col_index)
                    row.append(False)  # Not a wall
                    j += 2
                    col_index += 1
                elif j < len(line) and line[j] == 'B':
                    self.goal = (i, col_index)
                    row.append(False)  # Not a wall
                    j += 1
                    col_index += 1
                elif j < len(line) and line[j] == ' ':
                    row.append(False)  # Not a wall
                    j += 1
                    col_index += 1
                else:
                    # Any other character is treated as a wall
                    row.append(True)   # Wall
                    j += 1
                    col_index += 1
            
            # Pad row to match width
            while len(row) < self.width:
                row.append(False)  # Treat padding as empty spaces
            
            self.walls.append(row)
        
        # Print only basic information, not the full maze
        print(f"Maze loaded: {self.height}x{self.width}")
        print(f"Start positions: {self.starts}")
        print(f"Goal position: {self.goal}")

    def neighbors(self, position):
        """Returns traversable neighbor positions"""
        i, j = position
        neighbors = []
        
        # Check all four adjacent cells
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj
            
            # Check bounds
            if 0 <= ni < self.height and 0 <= nj < self.width:
                # Check if not a wall
                if not self.walls[ni][nj]:
                    neighbors.append((ni, nj))
        
        return neighbors
    
    def is_valid_position(self, position):
        """Check if a position is valid (within bounds and not a wall)."""
        i, j = position
        if 0 <= i < self.height and 0 <= j < self.width:
            return not self.walls[i][j]  # Valid if not a wall
        return False  # Out of bounds

class PathFinder:
    """Class to find paths using various algorithms"""
    def __init__(self, maze):
        self.maze = maze

    def find_path(self, algorithm, start, goal, reservation=None):
        """Find path using the specified algorithm"""
        if algorithm == "dfs":
            return DFS.solve(self.maze, start, goal, reservation)
        elif algorithm == "astar":
            return AStar.solve(self.maze, start, goal, reservation)
        elif algorithm == "greedy":
            return Greedy.solve(self.maze, start, goal, reservation)
        elif algorithm == "dijkstra":
            return Dijkstra.solve(self.maze, start, goal, reservation)
        elif algorithm == "bidirectional":
            return BidirectionalSearch.solve(self.maze, start, goal, reservation)
        elif algorithm == "iddfs":
            return IterativeDeepeningDFS.solve(self.maze, start, goal, reservation)
        else:  # Default to BFS
            return BFS.solve(self.maze, start, goal, reservation)

class Visualizer:
    """Class to visualize the maze and agents"""
    def __init__(self, maze):
        pygame.init()
        self.maze = maze
        self.width = maze.width * CELL_SIZE
        self.height = maze.height * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Multi-Agent Maze Solver")
        self.clock = pygame.time.Clock()
    
    def draw_with_paths(self, agent_positions=None, agent_ids=None, paths=None, path_colors=None):
        """Draw the maze with color-coded paths for each agent"""
        # Fill background
        self.screen.fill(BLACK)
        
        # Create a grid to track which agent's path is in each cell
        path_grid = {}
        
        # Draw agent paths
        if paths and path_colors:
            for agent_id, path in enumerate(paths):
                for cell in path:
                    if cell != self.maze.goal and (not agent_positions or cell not in agent_positions):
                        if cell in path_grid:
                            # If multiple agents use this cell, use shared color
                            path_grid[cell] = 0  # 0 means shared
                        else:
                            path_grid[cell] = agent_id + 1  # Store agent_id
        
        # Draw path cells with appropriate colors
        for cell, agent_id in path_grid.items():
            x = cell[1] * CELL_SIZE
            y = cell[0] * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            
            if agent_id == 0:  # Shared path
                pygame.draw.rect(self.screen, SHARED_PATH_COLOR, rect)
            else:
                color = path_colors.get(agent_id, BLUE)
                pygame.draw.rect(self.screen, color, rect)
        
        # Draw maze structure
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                # Draw walls
                if self.maze.walls[i][j]:
                    pygame.draw.rect(self.screen, WHITE, rect)
                
                # Draw goal
                elif self.maze.goal and (i, j) == self.maze.goal:
                    pygame.draw.rect(self.screen, GREEN, rect)
                
                # Draw grid lines
                pygame.draw.rect(self.screen, BLACK, rect, 1)
        
        # Draw agents (top layer)
        if agent_positions and agent_ids:
            for pos, agent_id in zip(agent_positions, agent_ids):
                x = pos[1] * CELL_SIZE
                y = pos[0] * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                color = AGENT_COLORS.get(agent_id, BLUE)
                pygame.draw.rect(self.screen, color, rect)
        
        # Update display
        pygame.display.flip()
    
    def visualize_exploration(self, agent_ids, exploration_traces, final_paths):
        """Visualize the exploration process followed by path execution"""
        running = True
        clock = pygame.time.Clock()
        
        # First, animate exploration process
        max_trace_length = max(len(trace) for trace in exploration_traces)
        current_paths = [[] for _ in range(len(agent_ids))]
        
        for step in range(max_trace_length):
            if not running:
                break
                
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Update current exploration state
            for i, trace in enumerate(exploration_traces):
                if step < len(trace):
                    cell = trace[step]
                    if cell not in current_paths[i]:
                        current_paths[i].append(cell)
            
            # Display current state
            agent_positions = [path[0] for path in current_paths if path]  # Start positions
            self.draw_with_paths(agent_positions, agent_ids, current_paths, PATH_COLORS)
            
            # Control frame rate
            clock.tick(30)
        
        # Pause briefly before showing path execution
        if running:
            pygame.time.delay(1000)
        
        # Then, animate agents following their final paths
        if running:
            self.animate_paths_smooth(final_paths, agent_ids, PATH_COLORS, animation_frames=8)
        else:
            pygame.quit()
    
    def animate_paths_smooth(self, agent_paths, agent_ids, path_colors, animation_frames=5):
        """Animate agents following their paths with smoother movement"""
        max_path_length = max(len(path) for path in agent_paths)
        
        running = True
        step = 0
        
        while running and step < max_path_length - 1:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Gather current paths up to this point
            current_exploration = [path[:step+1] for path in agent_paths]
            
            # For each sub-frame in the animation
            for frame in range(animation_frames):
                # Calculate interpolated positions
                current_positions = []
                
                for path, agent_id in zip(agent_paths, agent_ids):
                    if step < len(path) - 1:
                        # Current and next positions
                        current = path[step]
                        next_pos = path[step + 1]
                        
                        # Calculate interpolated position for smooth animation
                        progress = frame / animation_frames
                        interp_row = int(current[0] + (next_pos[0] - current[0]) * progress)
                        interp_col = int(current[1] + (next_pos[1] - current[1]) * progress)
                        
                        current_positions.append((interp_row, interp_col))
                    elif step < len(path):
                        current_positions.append(path[step])
                    else:
                        # Agent reached goal, stay there
                        current_positions.append(path[-1])
                
                # Draw maze and agents
                self.draw_with_paths(current_positions, agent_ids, current_exploration, path_colors)
                
                # Control frame rate for smooth animation
                pygame.time.Clock().tick(30)
            
            # Increment step counter
            step += 1
        
        # Wait for user to exit
        waiting = True
        while waiting and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
        
        pygame.quit()