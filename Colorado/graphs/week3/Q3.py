def compute_mst(g):
    # return a tuple of two items
    #   1. list of edges (i,j) that are part of the MST
    #   2. sum of MST edge weights.
    d = DisjointForests(g.n)
    mst_edges = []
    g.sort_edges()
    
    # Initialize all vertices in the disjoint forest
    for v in range(g.n):
        d.make_set(v)
    
    total_weight = 0
    
    # Process edges in ascending order of weights
    for i, j, wij in g.edges:
        if d.find(i) != d.find(j):  # Check if adding this edge forms a cycle
            d.union(i, j)  # Union the sets
            mst_edges.append((i, j, wij))  # Add edge to MST
            total_weight += wij  # Add weight to total
    
    return mst_edges, total_weight


