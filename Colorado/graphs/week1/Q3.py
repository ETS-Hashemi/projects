def find_all_nodes_in_cycle(g): # g is an UndirectedGraph class
    set_of_nodes = set()
    
    # Perform DFS traversal to find back edges
    dfs_timer = DFSTimeCounter()
    discovery_times = [None] * g.n
    finish_times = [None] * g.n
    dfs_tree_parents = [None] * g.n
    dfs_back_edges = []

    # Helper function to perform DFS and collect back edges
    def dfs_visit(i):
        discovery_times[i] = dfs_timer.get()
        dfs_timer.increment()
        for j in sorted(g.get_neighboring_vertices(i)):
            if discovery_times[j] is None:  # If j is not discovered yet
                dfs_tree_parents[j] = i
                dfs_visit(j)
            elif finish_times[j] is None and dfs_tree_parents[i] != j:  # Back edge
                dfs_back_edges.append((i, j))
        finish_times[i] = dfs_timer.get()
        dfs_timer.increment()

    # Traverse the graph to collect back edges
    for i in range(g.n):
        if discovery_times[i] is None:
            dfs_visit(i)

    # Process each back edge to find nodes in cycles
    for u, v in dfs_back_edges:
        # Trace back from u and v to find the cycle
        cycle_nodes = set()
        current = u
        while current is not None and current != v:
            cycle_nodes.add(current)
            current = dfs_tree_parents[current]
        cycle_nodes.add(v)
        set_of_nodes.update(cycle_nodes)

    return set_of_nodes

