import sys
import pygame

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


class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class Maze():

    def __init__(self, filename):
        try:
            # Read file and set height and width of maze
            with open(filename) as f:
                contents = f.read()

            # Validate start and goal
            if contents.count("A") != 1:
                raise Exception("Maze must have exactly one start point (A).")
            if contents.count("B") != 1:
                raise Exception("Maze must have exactly one goal point (B).")

            # Determine height and width of maze
            contents = contents.splitlines()
            self.height = len(contents)
            self.width = max(len(line) for line in contents)

            # Keep track of walls
            self.walls = []
            for i in range(self.height):
                row = []
                for j in range(self.width):
                    try:
                        if contents[i][j] == "A":
                            self.start = (i, j)
                            row.append(False)
                        elif contents[i][j] == "B":
                            self.goal = (i, j)
                            row.append(False)
                        elif contents[i][j] == " ":
                            row.append(False)
                        else:
                            row.append(True)
                    except IndexError:
                        row.append(False)
                self.walls.append(row)

            self.solution = None
        except FileNotFoundError:
            sys.exit(f"Error: File '{filename}' not found.")
        except Exception as e:
            sys.exit(f"Error: {e}")

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action, (r, c)))
        return result

    def solve(self, screen):
        """Finds a solution to maze, if one exists, and shows the agent's position dynamically."""

        # Keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier()
        frontier.add(start)

        # Initialize an empty explored set
        self.explored = set()

        # Keep looping until solution found
        while True:

            # If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("No solution")

            # Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # Draw the maze with the agent's current position
            self.draw_maze(screen, node.state)

            # If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                self.draw_maze(screen, node.state, show_solution=True)  # Show the solution path
                return

            # Mark node as explored
            self.explored.add(node.state)

            # Add neighbors to frontier
            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    frontier.add(child)

    def draw_maze(self, screen, agent_position, show_solution=False):
        """
        Draws the maze with the agent's current position.
        """
        screen.fill(BLACK)

        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                x = j * CELL_SIZE
                y = i * CELL_SIZE

                if col:
                    pygame.draw.rect(screen, WHITE, (x, y, CELL_SIZE, CELL_SIZE))
                elif (i, j) == self.start:
                    pygame.draw.rect(screen, RED, (x, y, CELL_SIZE, CELL_SIZE))
                elif (i, j) == self.goal:
                    pygame.draw.rect(screen, GREEN, (x, y, CELL_SIZE, CELL_SIZE))
                elif show_solution and self.solution and (i, j) in self.solution[1]:
                    pygame.draw.rect(screen, PURPLE, (x, y, CELL_SIZE, CELL_SIZE))
                elif (i, j) == agent_position:
                    pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))
                elif (i, j) in self.explored:
                    pygame.draw.rect(screen, YELLOW, (x, y, CELL_SIZE, CELL_SIZE))
                else:
                    pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE))

                # Draw grid lines
                pygame.draw.rect(screen, BLACK, (x, y, CELL_SIZE, CELL_SIZE), 1)

        pygame.display.flip()

        # Handle events to keep the window responsive
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Add a delay to slow down the visualization
        pygame.time.wait(200)  # 200 milliseconds delay


if len(sys.argv) != 2:
    sys.exit("Usage: python maze.py maze.txt")

# Initialize pygame
pygame.init()

# Load the maze
m = Maze(sys.argv[1])

# Set up the display
screen = pygame.display.set_mode((m.width * CELL_SIZE, m.height * CELL_SIZE))
pygame.display.set_caption("Maze Solver")

# Solve the maze
print("Solving...")
try:
    m.solve(screen)
    print("States Explored:", m.num_explored)
except Exception as e:
    print(f"Error: {e}")

# Wait for the user to close the window
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()