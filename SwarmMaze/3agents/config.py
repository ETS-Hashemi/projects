# Visualization settings
CELL_SIZE = 30
WHITE = (255, 255, 255)  # Wall
BLACK = (0, 0, 0)        # Background
GREEN = (0, 255, 0)      # Goal
RED = (255, 0, 0)        # Start
BLUE = (0, 0, 255)       # Default agent color

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

# Collision visualization colors
RESERVATION_COLOR = (255, 0, 0)  # Red for reserved cells
COLLISION_COLOR = (255, 255, 0)  # Yellow for collisions

# Algorithm defaults
DEFAULT_ALGORITHM = "bfs"
