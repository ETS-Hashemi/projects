from collections import deque
import heapq

class BFS:
    """Breadth-First Search with time-based reservations"""
    @staticmethod
    def solve(maze, start, goal, reservation=None):
        queue = deque([(start, [start], 0)])  # (position, path, time)
        visited = set([(start, 0)])  # (position, time)
        exploration_trace = []

        while queue:
            position, path, time = queue.popleft()
            exploration_trace.append(position)

            if position == goal:
                return path, exploration_trace

            for neighbor in maze.neighbors(position):
                if reservation and reservation.is_reserved(neighbor, time + 1):  # Use is_reserved
                    continue
                if (neighbor, time + 1) not in visited:
                    visited.add((neighbor, time + 1))
                    queue.append((neighbor, path + [neighbor], time + 1))

            # Waiting in place is also an option
            if not reservation or not reservation.is_reserved(position, time + 1):  # Use is_reserved
                if (position, time + 1) not in visited:
                    visited.add((position, time + 1))
                    queue.append((position, path + [position], time + 1))

        return [start], exploration_trace


class DFS:
    """Depth-First Search with time-based reservations"""
    @staticmethod
    def solve(maze, start, goal, reservation=None):
        stack = [(start, [start], 0)]  # (position, path, time)
        visited = set([(start, 0)])  # (position, time)
        exploration_trace = []
        MAX_DEPTH = 100

        while stack:
            position, path, time = stack.pop()
            exploration_trace.append(position)

            if position == goal:
                return path, exploration_trace

            if len(path) > MAX_DEPTH:
                continue

            neighbors = list(maze.neighbors(position))
            neighbors.reverse()

            valid_moves = []
            for neighbor in neighbors:
                if reservation and reservation.is_reserved(neighbor, time + 1):  # Use is_reserved
                    continue
                if (neighbor, time + 1) not in visited:
                    valid_moves.append(neighbor)

            if valid_moves:
                for neighbor in valid_moves:
                    visited.add((neighbor, time + 1))
                    stack.append((neighbor, path + [neighbor], time + 1))
            else:
                if not reservation or not reservation.is_reserved(position, time + 1):  # Use is_reserved
                    if (position, time + 1) not in visited:
                        visited.add((position, time + 1))
                        stack.append((position, path + [position], time + 1))

        return [start], exploration_trace


class AStar:
    """A* Search with time-based reservations"""
    @staticmethod
    def solve(maze, start, goal, reservation=None):
        open_set = [(0, 0, start, [start], [])]  # (f, time, position, path, exploration)
        closed_set = set()
        g_score = {(start, 0): 0}
        exploration_trace = []

        while open_set:
            f, time, current, path, exploration = heapq.heappop(open_set)
            exploration_trace = exploration + [current]

            if current == goal:
                return path, exploration_trace

            if (current, time) in closed_set:
                continue

            closed_set.add((current, time))

            for neighbor in maze.neighbors(current) + [current]:
                if reservation and reservation.is_reserved(neighbor, time + 1):  # Use is_reserved
                    continue
                if (neighbor, time + 1) in closed_set:
                    continue

                g = g_score.get((current, time), float('inf')) + 1
                if (neighbor, time + 1) not in g_score or g < g_score[(neighbor, time + 1)]:
                    g_score[(neighbor, time + 1)] = g
                    h = abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])
                    f = g + h
                    heapq.heappush(open_set, (f, time + 1, neighbor, path + [neighbor], exploration_trace.copy()))

        return [start], exploration_trace


class Greedy:
    """Greedy Best-First Search with time-based reservations"""
    @staticmethod
    def solve(maze, start, goal, reservation=None):
        open_set = [(0, 0, start, [start], [])]  # (h, time, position, path, exploration)
        visited = set([(start, 0)])
        exploration_trace = []

        while open_set:
            h, time, current, path, exploration = heapq.heappop(open_set)
            exploration_trace = exploration + [current]

            if current == goal:
                return path, exploration_trace

            for neighbor in maze.neighbors(current) + [current]:
                if reservation and reservation.is_reserved(neighbor, time + 1):  # Use is_reserved
                    continue
                if (neighbor, time + 1) not in visited:
                    visited.add((neighbor, time + 1))
                    h = abs(neighbor[0] - goal[0]) + abs(neighbor[1] - goal[1])
                    heapq.heappush(open_set, (h, time + 1, neighbor, path + [neighbor], exploration_trace.copy()))

        return [start], exploration_trace