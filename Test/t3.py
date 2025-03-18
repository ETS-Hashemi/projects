import networkx as nx

def get_dfs_path(graph, start, target):
    # Get predecessors from DFS traversal
    predecessors = nx.dfs_predecessors(graph, source=start)

    # Reconstruct the path from target to start
    path = []
    node = target
    while node != start:
        path.append(node)
        if node not in predecessors:
            return None  # No path found
        node = predecessors[node]
    path.append(start)
    
    return path[::-1]  # Reverse to get start → target path

# Example Graph
G = nx.Graph()
edges = [(0, 1), (0, 2), (1, 3), (4, 6), (2, 5), (2, 6)]
G.add_edges_from(edges)

# Find DFS path from node 0 to node 5
path = get_dfs_path(G, 0, 6)
print("DFS Path:", path)
