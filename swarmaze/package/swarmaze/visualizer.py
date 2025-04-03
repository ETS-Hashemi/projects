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
        self.maze = maze
        self.screen = pygame.display.set_mode((maze.width * CELL_SIZE, maze.height * CELL_SIZE))
        pygame.display.set_caption("Maze Solver")
        self.delay = delay  # Delay in milliseconds

    def draw_maze(self, agent_position=None, explored=None, solution=None):
        """
        Draws the maze with the current state of the agent, explored cells, and solution path.
        :param agent_position: The current position of the agent.
        :param explored: A set of explored cells.
        :param solution: A list of cells in the solution path.
        """
        self.screen.fill(BLACK)

        for i, row in enumerate(self.maze.walls):
            for j, col in enumerate(row):
                x = j * CELL_SIZE
                y = i * CELL_SIZE

                if col:
                    pygame.draw.rect(self.screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                elif (i, j) == self.maze.start:
                    pygame.draw.rect(self.screen, RED, (x, y, CELL_SIZE, CELL_SIZE))
                elif (i, j) == self.maze.goal:
                    pygame.draw.rect(self.screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
                elif solution and (i, j) in solution:
                    pygame.draw.rect(self.screen, PURPLE, (x, y, CELL_SIZE, CELL_SIZE))
                elif explored and (i, j) in explored:
                    pygame.draw.rect(self.screen, YELLOW, (x, y, CELL_SIZE, CELL_SIZE))
                elif agent_position == (i, j):
                    pygame.draw.rect(self.screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))

                pygame.draw.rect(self.screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

        pygame.display.flip()

        # Handle events to keep the window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Add a delay to slow down the visualization
        pygame.time.delay(self.delay)

    def wait_for_exit(self):
        """
        Waits for the user to close the window.
        """
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()