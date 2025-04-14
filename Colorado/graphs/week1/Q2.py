def num_connected_components(g): # g is an UndirectedGraph class
    # Initialize a counter for connected components
    connected_components = 0
    
    # Create a list to track visited nodes
    visited = [False] * g.n

    # Helper function to perform DFS and mark visited nodes
    def dfs(node):
        # Use a stack for iterative DFS
        stack = [node]
        while stack:
            current = stack.pop()
            if not visited[current]:
                visited[current] = True
                # Add unvisited neighbors to the stack
                stack.extend(neighbor for neighbor in g.get_neighboring_vertices(current) if not visited[neighbor])

    # Iterate through all nodes in the graph
    for i in range(g.n):
        if not visited[i]:  # If the node is not visited, it's a new component
            connected_components += 1
            dfs(i)  # Perform DFS to mark all nodes in this component as visited

    return connected_components

if __name__ == "__main__":
    # create the graph from problem 1A
    g = UndirectedGraph(5)
    g.add_edge(0,1)
    g.add_edge(0,2)
    g.add_edge(0,4)
    g.add_edge(2,3)
    g.add_edge(2,4)
    g.add_edge(3,4)
    
    result_a = num_connected_components(g)
    print(f'Test A: g has {result_a} connected component(s).')

    g2 = UndirectedGraph(7)
    g2.add_edge(0,1)
    g2.add_edge(0,2)
    g2.add_edge(0,4)
    g2.add_edge(2,3)
    g2.add_edge(2,4)
    g2.add_edge(3,4)
    g2.add_edge(5,6)

    result_b = num_connected_components(g2)
    print(f'Test B: g2 has {result_b} connected component(s).')

    g3 = UndirectedGraph(8)
    g3.add_edge(0,1)
    g3.add_edge(0,2)
    g3.add_edge(0,4)
    g3.add_edge(2,3)
    g3.add_edge(2,4)
    g3.add_edge(3,4)
    g3.add_edge(5,6)

    result_c = num_connected_components(g3)
    print(f'Test C: g3 has {result_c} connected component(s).')

    g3.add_edge(7,5)
    result_d = num_connected_components(g3)
    print(f'Test D: g3 now has {result_d} connected component(s).')
