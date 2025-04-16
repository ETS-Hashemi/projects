import pygame
import sys
from collections import deque
import heapq  # For priority queue in A* search

# Colors
WHITE = (255, 255, 255)  # Wall
BLACK = (0, 0, 0)        # Background
GREEN = (0, 255, 0)      # Goal
RED = (255, 0, 0)        # Start
BLUE = (0, 0, 255)       # Default agent color

# Agent colors
AGENT_COLORS = {
    1: (0, 0, 255),      # Blue
    2: (255, 165, 0),    # Orange
    3: (128, 0, 128)     # Purple
}

# Path colors (lighter than agent colors for visibility)
PATH_COLORS = {
    1: (100, 100, 255),   # Light blue
    2: (255, 200, 100),   # Light orange
    3: (200, 100, 200)    # Light purple
}

# Shared path color (when multiple agents use the same cell)
SHARED_PATH_COLOR = (150, 150, 150)  # Gray

# Cell size in pixels
CELL_SIZE = 30

class SimpleMaze:
    def __init__(self, filename):
        # Read maze file
        with open(filename, 'r') as f:
            lines = f.read().splitlines()
        
        self.height = len(lines)
        self.width = max(len(line) for line in lines)
        
        # Parse maze structure
        self.walls = []
        self.starts = {}
        self.goal = None
        
        for i, line in enumerate(lines):
            row = []
            for j, char in enumerate(line):
                if j < len(line) and line[j:j+2] in ['A1', 'A2', 'A3']:
                    agent_num = int(line[j+1])
                    self.starts[agent_num] = (i, j)
                    row.append(False)  # Not a wall
                    j += 1  # Skip next character (the number)
                elif char == 'B':
                    self.goal = (i, j)
                    row.append(False)  # Not a wall
                elif char == ' ':
                    row.append(False)  # Not a wall
                else:
                    row.append(True)   # Wall
            
            # Pad row to match width
            while len(row) < self.width:
                row.append(False)
            
            self.walls.append(row)
            
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

    def find_path(self, start, goal):
        """Find path from start to goal using BFS"""
        queue = deque([(start, [start])])
        visited = set([start])
        
        while queue:
            position, path = queue.popleft()
            
            if position == goal:
                return path
            
            for neighbor in self.neighbors(position):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        # No path found
        return [start]

    def find_path_with_reservation(self, start, goal, reservation):
        """Find path from start to goal using BFS with time-based reservations"""
        queue = deque([(start, [start], 0)])  # (position, path, time)
        visited = set([(start, 0)])  # (position, time)
        
        while queue:
            position, path, time = queue.popleft()
            
            if position == goal:
                return path
            
            for neighbor in self.neighbors(position):
                # Check if the neighbor is reserved at next time step
                if (neighbor, time + 1) not in reservation and (neighbor, time + 1) not in visited:
                    visited.add((neighbor, time + 1))
                    queue.append((neighbor, path + [neighbor], time + 1))
            
            # Waiting in place is also an option
            if (position, time + 1) not in reservation and (position, time + 1) not in visited:
                visited.add((position, time + 1))
                queue.append((position, path + [position], time + 1))
        
        # No path found
        return [start]

    def find_path_with_reservation_and_trace(self, start, goal, reservation):
        """Find path with exploration trace for visualization"""
        queue = deque([(start, [start], 0)])  # (position, path, time)
        visited = set([(start, 0)])  # (position, time)
        exploration_trace = []  # Store cells explored in order
        
        while queue:
            position, path, time = queue.popleft()
            exploration_trace.append(position)
            
            if position == goal:
                return path, exploration_trace
            
            neighbors = []
            for neighbor in self.neighbors(position):
                if (neighbor, time + 1) not in reservation and (neighbor, time + 1) not in visited:
                    neighbors.append(neighbor)
            
            # Also consider waiting in place
            if (position, time + 1) not in reservation and (position, time + 1) not in visited:
                neighbors.append(position)
            
            # Add all valid neighbors to the queue
            for neighbor in neighbors:
                visited.add((neighbor, time + 1))
                if neighbor == position:  # Waiting in place
                    queue.append((neighbor, path + [neighbor], time + 1))
                else:
                    queue.append((neighbor, path + [neighbor], time + 1))
        
        # No path found
        return [start], exploration_trace

    def find_path_astar(self, start, goal):
        """Find path from start to goal using A* search algorithm"""
        # Priority queue with (priority, position, path)
        open_set = [(0, start, [start])]
        closed_set = set()
        g_score = {start: 0}  # Cost from start to current node
        
        while open_set:
            _, current, path = heapq.heappop(open_set)
            
            if current == goal:
                return path
            
            if current in closed_set:
                continue
                
            closed_set.add(current)
            
            for neighbor in self.neighbors(current):
                if neighbor in closed_set:
                    continue
                    
                # A* uses g_score (path cost) + h_score (heuristic)
                g = g_score[current] + 1  # 1 is the cost of moving to a neighbor
                
                if neighbor not in g_score or g < g_score[neighbor]:
                    g_score[neighbor] = g
                    # Manhattan distance heuristic
                    h = abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])
                    f = g + h  # f = g + h is the A* formula
                    heapq.heappush(open_set, (f, neighbor, path + [neighbor]))
        
        return [start]  # No path found
        
    def find_path_greedy(self, start, goal):
        """Find path using Greedy Best-First Search algorithm"""
        # Priority queue with (heuristic, position, path)
        open_set = [(0, start, [start])]
        visited = set([start])
        
        while open_set:
            _, current, path = heapq.heappop(open_set)
            
            if current == goal:
                return path
                
            for neighbor in self.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    # Only use heuristic (no path cost) - this is what makes it "greedy"
                    h = abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])
                    heapq.heappush(open_set, (h, neighbor, path + [neighbor]))
        
        return [start]  # No path found

    def find_path_with_astar_and_trace(self, start, goal, reservation):
        """Find path with A* and collect exploration trace"""
        # Priority queue with (priority, time, position, path)
        open_set = [(0, 0, start, [start])]
        closed_set = set()
        g_score = {(start, 0): 0}  # Cost from start to (position, time)
        exploration_trace = []
        
        while open_set:
            _, time, current, path = heapq.heappop(open_set)
            exploration_trace.append(current)
            
            if current == goal:
                return path, exploration_trace
            
            if (current, time) in closed_set:
                continue
                
            closed_set.add((current, time))
            
            # Consider all neighbors plus waiting in place
            neighbors = self.neighbors(current) + [current]  # Add current for waiting
            
            for neighbor in neighbors:
                # Check reservation
                if (neighbor, time + 1) in reservation or (neighbor, time + 1) in closed_set:
                    continue
                
                # A* calculation
                g = g_score.get((current, time), float('inf')) + 1
                if (neighbor, time + 1) not in g_score or g < g_score[(neighbor, time + 1)]:
                    g_score[(neighbor, time + 1)] = g
                    h = abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])
                    f = g + h
                    heapq.heappush(open_set, (f, time + 1, neighbor, path + [neighbor]))
        
        return [start], exploration_trace  # No path found

class SimpleVisualizer:
    def __init__(self, maze):
        pygame.init()
        self.maze = maze
        self.width = maze.width * CELL_SIZE
        self.height = maze.height * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simple Maze Visualizer")
        self.clock = pygame.time.Clock()
    
    def draw(self, agent_positions=None, path_cells=None, agent_ids=None):
        # Fill background
        self.screen.fill(BLACK)
        
        # Draw path visualization first (lowest layer)
        if path_cells:
            for cell in path_cells:
                if cell not in agent_positions and cell != self.maze.goal:
                    x = cell[1] * CELL_SIZE
                    y = cell[0] * CELL_SIZE
                    rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, YELLOW, rect)
        
        # Draw maze
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
                color = AGENT_COLORS.get(agent_id, BLUE)  # Use specific color for agent
                pygame.draw.rect(self.screen, color, rect)
        
        # Update display
        pygame.display.flip()
    
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
                    if cell != self.maze.goal and cell not in agent_positions:
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
    
    def run(self, agent_positions=None, max_frames=100):
        """Run visualization loop for specified frames"""
        frame_count = 0
        running = True
        
        while running and frame_count < max_frames:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Draw maze and agents
            self.draw(agent_positions)
            
            # Control frame rate
            self.clock.tick(30)
            
            frame_count += 1
        
        # Wait for user to exit
        waiting = True
        while waiting and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
        
        pygame.quit()

    def animate_paths(self, agent_paths, delay_frames=10):
        """Animate agents following their paths"""
        max_path_length = max(len(path) for path in agent_paths)
        
        running = True
        step = 0
        
        while running and step < max_path_length:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Get current positions
            current_positions = []
            for path in agent_paths:
                if step < len(path):
                    current_positions.append(path[step])
                else:
                    # Agent reached goal, stay there
                    current_positions.append(path[-1])
            
            # Draw maze and agents
            self.draw(current_positions)
            
            # Control frame rate
            self.clock.tick(5)  # Slower for better visualization
            
            # Increment step counter
            step += 1
        
        # Wait for user to exit
        waiting = True
        while waiting and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
        
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
            agent_positions = [path[0] for path in current_paths]  # Start positions
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