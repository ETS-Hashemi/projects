from maze import Node, StackFrontier, QueueFrontier
import heapq


class PriorityQueueFrontier():
    def __init__(self):
        self.frontier = []

    def add(self, node):
        heapq.heappush(self.frontier, node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            return heapq.heappop(self.frontier)


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


class BFS():
    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer
        self.frontier = QueueFrontier()
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


class AStar():
    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer
        self.frontier = PriorityQueueFrontier()
        self.explored = set()

    def heuristic(self, state):
        """
        Heuristic function: Manhattan distance from the current state to the goal.
        """
        x1, y1 = state
        x2, y2 = self.maze.goal
        return abs(x1 - x2) + abs(y1 - y2)

    def solve(self):
        start = Node(state=self.maze.start, parent=None, action=None, cost=0, heuristic=self.heuristic(self.maze.start))
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
                    cost = node.cost + 1  # Increment cost by 1 for each step
                    heuristic = self.heuristic(state)
                    child = Node(state=state, parent=node, action=action, cost=cost, heuristic=heuristic)
                    self.frontier.add(child)

        raise Exception("No solution")