import pygame
import sys

# Constants for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)  # Color for the solution path

# Constants for cell size
CELL_SIZE = 30

class Visualizer():
    def __init__(self, maze, delay=200):
        """
        Initializes the visualizer.
        :param maze: The maze object to visualize.
        :param delay: Delay in milliseconds between each frame.
        """
        pygame.init()
        self.maze = maze
        self.width = maze.width * CELL_SIZE
        self.height = maze.height * CELL_SIZE
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Multi-Agent Maze Solver")
        self.delay = delay
        self.clock = pygame.time.Clock()

    def draw_maze(self, agent_positions=None):
        """
        Draws the maze with the current state of the agents.
        :param agent_positions: A list of positions for multiple agents.
        """
        self.screen.fill(BLACK)
        
        # Draw maze structure
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                
                if self.maze.walls[i][j]:
                    pygame.draw.rect(self.screen, WHITE, rect)
                elif (i, j) == self.maze.goal:
                    pygame.draw.rect(self.screen, GREEN, rect)
                elif agent_positions and (i, j) in agent_positions:
                    pygame.draw.rect(self.screen, BLUE, rect)
                
                pygame.draw.rect(self.screen, BLACK, rect, 1)
        
        pygame.display.flip()
        self.clock.tick(30)  # Limit to 30 FPS
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def wait_for_exit(self):
        """
        Waits for the user to close the window.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()