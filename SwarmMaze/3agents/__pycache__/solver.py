from maze import Node

def plan_with_reservation(agent_start, goal, maze, reservation):
    open_set = [Node(state=agent_start, parent=None, action=None, cost=0, heuristic=0)]
    explored = set()

    while open_set:
        node = open_set.pop(0)
        t = node.cost

        if node.state == goal:
            path = []
            while node:
                path.append(node.state)
                node = node.parent
            return path[::-1]

        explored.add((node.state, t))

        for action, state in maze.neighbors(node.state):
            if (state, t + 1) not in explored and state not in reservation.get(t + 1, set()):
                h = abs(state[0] - goal[0]) + abs(state[1] - goal[1])
                child = Node(state=state, parent=node, action=action, cost=t + 1, heuristic=h)
                open_set.append(child)

        open_set.sort(key=lambda x: x.cost + x.heuristic)  # Sort by cost + heuristic

    # If no path is found, return a path with only the start position
    return [agent_start]

def solve_maze_for_agents(starts, goal, maze):
    reservation = {}
    agent_paths = []

    for agent_id, start in starts.items():
        try:
            path = plan_with_reservation(start, goal, maze, reservation)
            for t, pos in enumerate(path):
                if t not in reservation:
                    reservation[t] = set()
                reservation[t].add(pos)
            agent_paths.append(path)
        except Exception as e:
            print(f"Error planning path for agent {agent_id}: {e}")
            agent_paths.append([start])  # Add just the start position as a fallback

    return agent_paths