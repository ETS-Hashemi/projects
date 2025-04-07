from maze import Node, StackFrontier, QueueFrontier
import heapq
import random


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


class Dijkstra():
    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer
        self.frontier = PriorityQueueFrontier()
        self.explored = set()

    def solve(self):
        # Start node with cost 0
        start = Node(state=self.maze.start, parent=None, action=None, cost=0)
        self.frontier.add(start)

        while not self.frontier.empty():
            # Remove the node with the lowest cost
            node = self.frontier.remove()

            # If the goal is reached, reconstruct the path
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

            # Mark the node as explored
            self.explored.add(node.state)

            # Add neighbors to the frontier
            for action, state in self.maze.neighbors(node.state):
                if not self.frontier.contains_state(state) and state not in self.explored:
                    cost = node.cost + 1  # Increment cost by 1 for each step
                    child = Node(state=state, parent=node, action=action, cost=cost)
                    self.frontier.add(child)

        raise Exception("No solution")


class GreedyBestFirst():
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
        start = Node(state=self.maze.start, parent=None, action=None, heuristic=self.heuristic(self.maze.start))
        self.frontier.add(start)

        while not self.frontier.empty():
            node = self.frontier.remove()

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
                    heuristic = self.heuristic(state)
                    child = Node(state=state, parent=node, action=action, heuristic=heuristic)
                    self.frontier.add(child)

        raise Exception("No solution")


class RandomWalk():
    def __init__(self, maze, visualizer, max_steps=1000):
        self.maze = maze
        self.visualizer = visualizer
        self.max_steps = max_steps

    def solve(self):
        current = Node(state=self.maze.start, parent=None, action=None)
        steps = 0

        while steps < self.max_steps:
            if current.state == self.maze.goal:
                actions = []
                cells = []
                while current.parent is not None:
                    actions.append(current.action)
                    cells.append(current.state)
                    current = current.parent
                actions.reverse()
                cells.reverse()
                return actions, cells

            # Randomly select a neighbor
            neighbors = self.maze.neighbors(current.state)
            if not neighbors:
                break
            action, state = random.choice(neighbors)
            current = Node(state=state, parent=current, action=action)
            steps += 1

        raise Exception("No solution (max steps reached)")


class BidirectionalSearch():
    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer
        self.frontier_start = QueueFrontier()
        self.frontier_goal = QueueFrontier()
        self.explored_start = set()
        self.explored_goal = set()

    def solve(self):
        start = Node(state=self.maze.start, parent=None, action=None)
        goal = Node(state=self.maze.goal, parent=None, action=None)
        self.frontier_start.add(start)
        self.frontier_goal.add(goal)

        while not self.frontier_start.empty() and not self.frontier_goal.empty():
            # Expand from the start
            node_start = self.frontier_start.remove()
            self.explored_start.add(node_start.state)

            # Check if the two searches meet
            if node_start.state in self.explored_goal:
                return self.reconstruct_path(node_start, self.explored_goal)

            for action, state in self.maze.neighbors(node_start.state):
                if state not in self.explored_start:
                    child = Node(state=state, parent=node_start, action=action)
                    self.frontier_start.add(child)

            # Expand from the goal
            node_goal = self.frontier_goal.remove()
            self.explored_goal.add(node_goal.state)

            # Check if the two searches meet
            if node_goal.state in self.explored_start:
                return self.reconstruct_path(node_goal, self.explored_start)

            for action, state in self.maze.neighbors(node_goal.state):
                if state not in self.explored_goal:
                    child = Node(state=state, parent=node_goal, action=action)
                    self.frontier_goal.add(child)

        raise Exception("No solution")

    def reconstruct_path(self, node, explored):
        actions = []
        cells = []
        while node.parent is not None:
            actions.append(node.action)
            cells.append(node.state)
            node = node.parent
        actions.reverse()
        cells.reverse()
        return actions, cells


class IterativeDeepeningDFS():
    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer

    def solve(self):
        depth = 0
        while True:
            try:
                return self.depth_limited_search(self.maze.start, depth)
            except Exception:
                depth += 1

    def depth_limited_search(self, state, depth):
        if depth == 0:
            if state == self.maze.goal:
                return [], [state]
            else:
                raise Exception("Depth limit reached")
        for action, neighbor in self.maze.neighbors(state):
            try:
                actions, cells = self.depth_limited_search(neighbor, depth - 1)
                return [action] + actions, [state] + cells
            except Exception:
                continue
        raise Exception("No solution")


class HillClimbing():
    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer

    def heuristic(self, state):
        x1, y1 = state
        x2, y2 = self.maze.goal
        return abs(x1 - x2) + abs(y1 - y2)

    def solve(self):
        current = Node(state=self.maze.start, parent=None, action=None)

        while True:
            if current.state == self.maze.goal:
                actions = []
                cells = []
                while current.parent is not None:
                    actions.append(current.action)
                    cells.append(current.state)
                    current = current.parent
                actions.reverse()
                cells.reverse()
                return actions, cells

            # Evaluate neighbors
            neighbors = self.maze.neighbors(current.state)
            if not neighbors:
                raise Exception("No solution (stuck in local minimum)")

            best_neighbor = None
            best_heuristic = float("inf")
            for action, state in neighbors:
                h = self.heuristic(state)
                if h < best_heuristic:
                    best_heuristic = h
                    best_neighbor = Node(state=state, parent=current, action=action)

            if best_heuristic >= self.heuristic(current.state):
                raise Exception("No solution (stuck in local minimum)")

            current = best_neighbor


class MultiAgentSearch():
    def __init__(self, maze, visualizer):
        self.maze = maze
        self.visualizer = visualizer

    def search(self):
        exploration_traces = []
        agent_paths = {}

        for agent_id, start in self.maze.starts.items():
            path, trace = self._search_for_agent(start, self.maze.goal)
            exploration_traces.append(trace)
            agent_paths[agent_id] = path

        return list(self.maze.starts.keys()), exploration_traces, agent_paths

    def _search_for_agent(self, start, goal):
        path = []
        trace = []
        return path, trace