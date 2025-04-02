import sys
import pygame
import heapq

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
    def __init__(self, state, parent, action, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        self.heuristic = heuristic

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


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
            return self.frontier.pop()


class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return self.frontier.pop(0)


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
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


class DFS():
    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer
        self.frontier = StackFrontier()
        self.explored = set()

    def solve(self):
        start = Node(state=self.maze.start, parent=None, action=None)
        self.frontier.add(start)

        while not self.frontier.empty():
            node = self.frontier.remove()

            # Visualize the current state
            self.visualizer.draw_maze(agent_position=node.state, explored=self.explored)

            if node.state == self.maze.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                return actions, cells

            self.explored.add(node.state)

            for action, state in self.maze.neighbors(node.state):
                if not self.frontier.contains_state(state) and state not in self.explored:
                    child = Node(state=state, parent=node, action=action)
                    self.frontier.add(child)

        raise Exception("No solution")


def main():
    if len(sys.argv) != 3:
        sys.exit("Usage: python maze.py maze.txt [dfs|bfs]")

    filename = sys.argv[1]
    algorithm = sys.argv[2].lower()

    maze = Maze(filename)
    visualizer = Visualizer(maze)

    if algorithm == "dfs":
        solver = DFS(maze, visualizer)
    else:
        sys.exit("Invalid algorithm. Choose 'dfs'.")

    print("Solving...")
    try:
        actions, cells = solver.solve()
        visualizer.draw_maze(solution=cells)
        print("Solution found!")
    except Exception as e:
        print(f"Error: {e}")

    visualizer.wait_for_exit()


if __name__ == "__main__":
    pygame.init()
    main()