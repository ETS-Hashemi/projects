import pygame
import sys
from maze import Maze, Visualizer, PathFinder  # Add PathFinder import
from reservation import ReservationTable
from config import PATH_COLORS, RESERVATION_COLOR, COLLISION_COLOR, CELL_SIZE, WHITE, BLACK, GREEN, BLUE

class CollisionVisualizer:
    def __init__(self, maze):
        self.maze = maze
        self.visualizer = Visualizer(maze)

    def visualize_collision_avoidance(self, agent_paths, reservation):
        """Visualize the collision avoidance mechanism step by step."""
        running = True
        clock = pygame.time.Clock()

        # Maximum path length to determine animation steps
        max_path_length = max(len(path) for path in agent_paths)

        for step in range(max_path_length):
            if not running:
                break

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Gather current agent positions
            current_positions = []
            for path in agent_paths:
                if step < len(path):
                    current_positions.append(path[step])
                else:
                    current_positions.append(path[-1])

            # Check for collisions
            collisions = self.detect_collisions(current_positions)

            # Draw maze with reservation table, current positions, and collisions
            self.draw_with_reservations(current_positions, reservation, step, collisions)

            # Display reservation table in the console for debugging
            print(f"Step {step}: Reservation Table")
            for (pos, time), agent_id in reservation.reservations.items():
                if time == step:
                    print(f"  Time {time}: Position {pos} reserved by Agent {agent_id}")
            if collisions:
                print(f"  Collisions detected at: {collisions}")

            # Add delay to slow down visualization
            pygame.time.delay(1000)

            # Control frame rate
            clock.tick(30)

        pygame.quit()

    def detect_collisions(self, positions):
        """Detect collisions among agents."""
        seen = set()
        collisions = set()
        for pos in positions:
            if pos in seen:
                collisions.add(pos)
            else:
                seen.add(pos)
        return collisions

    def draw_with_reservations(self, agent_positions, reservation, current_time, collisions):
        """Draw the maze with reservations and collisions highlighted."""
        # Fill background
        self.visualizer.screen.fill(BLACK)

        # Draw maze structure
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                x = j * CELL_SIZE
                y = i * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

                # Draw walls
                if self.maze.walls[i][j]:
                    pygame.draw.rect(self.visualizer.screen, WHITE, rect)

                # Draw goal
                elif self.maze.goal and (i, j) == self.maze.goal:
                    pygame.draw.rect(self.visualizer.screen, GREEN, rect)

                # Draw grid lines
                pygame.draw.rect(self.visualizer.screen, BLACK, rect, 1)

        # Highlight reserved cells
        for (pos, time), agent_id in reservation.reservations.items():
            if time == current_time:
                x = pos[1] * CELL_SIZE
                y = pos[0] * CELL_SIZE
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.visualizer.screen, RESERVATION_COLOR, rect)

        # Highlight collisions
        for pos in collisions:
            x = pos[1] * CELL_SIZE
            y = pos[0] * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.visualizer.screen, COLLISION_COLOR, rect)

        # Draw agents
        for pos, agent_id in zip(agent_positions, range(1, len(agent_positions) + 1)):
            x = pos[1] * CELL_SIZE
            y = pos[0] * CELL_SIZE
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            color = PATH_COLORS.get(agent_id, BLUE)
            pygame.draw.rect(self.visualizer.screen, color, rect)

        # Update display
        pygame.display.flip()

    def draw_legend(self):
        """Draw a legend explaining the colors used in the visualization."""
        font = pygame.font.SysFont(None, 24)
        legend_items = [
            ("Reserved Cell", RESERVATION_COLOR),
            ("Collision", COLLISION_COLOR),
            ("Agent 1", PATH_COLORS.get(1, BLUE)),
            ("Agent 2", PATH_COLORS.get(2, BLUE)),
            ("Agent 3", PATH_COLORS.get(3, BLUE)),
            ("Goal", GREEN),
        ]
        x, y = 10, self.maze.height * CELL_SIZE + 10
        for text, color in legend_items:
            pygame.draw.rect(self.visualizer.screen, color, (x, y, 20, 20))
            label = font.render(text, True, WHITE)
            self.visualizer.screen.blit(label, (x + 30, y))
            y += 30

if __name__ == "__main__":
    # Example usage
    if len(sys.argv) < 2:
        sys.exit("Usage: python collision_visualizer.py maze4_3a.txt [algorithm]")

    maze_file = sys.argv[1]
    algorithm = "bfs"  # Default to BFS
    if len(sys.argv) > 2:
        algorithm = sys.argv[2].lower()

    print(f"Loading maze from {maze_file}...")
    print(f"Using {algorithm.upper()} search algorithm")

    maze = Maze(maze_file)

    # Initialize pathfinder
    pathfinder = PathFinder(maze)

    # Dynamically compute paths for agents
    agent_paths = []
    reservation = ReservationTable()
    for agent_id, start in maze.starts.items():
        path, _ = pathfinder.find_path(algorithm, start, maze.goal, reservation)
        agent_paths.append(path)

        # Update reservation table
        for t, pos in enumerate(path):
            reservation.add_reservation(pos, t, agent_id)

    # Validate paths to ensure no agent passes through walls
    for agent_id, path in enumerate(agent_paths, start=1):
        for pos in path:
            if not maze.is_valid_position(pos):
                raise ValueError(f"Agent {agent_id} path includes invalid position {pos} (wall or out of bounds).")

    visualizer = CollisionVisualizer(maze)
    visualizer.visualize_collision_avoidance(agent_paths, reservation)