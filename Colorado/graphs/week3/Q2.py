class UndirectedGraph:
    
    # n is the number of vertices
    # we will label the vertices from 0 to self.n -1 
    # We simply store the edges in a list.
    def __init__(self, n):
        assert n >= 1, 'You are creating an empty graph -- disallowed'
        self.n = n
        self.edges = []
        self.vertex_data = [None]*self.n
       
    def set_vertex_data(self, j, dat):
        assert 0 <= j < self.n
        self.vertex_data[j] = dat
        
    def get_vertex_data(self, j):
        assert 0 <= j < self.n
        return self.vertex_data[j] 
        
    def add_edge(self, i, j, wij):
        assert 0 <= i < self.n
        assert 0 <= j < self.n
        assert i != j
        # Make sure to add edge from i to j with weight wij
        self.edges.append((i, j, wij))
        
    def sort_edges(self):
        # sort edges in ascending order of weights.
        self.edges = sorted(self.edges, key=lambda edg_data: edg_data[2])
        
def compute_scc(g, W):
    # create a disjoint forest with as many elements as number of vertices
    d = DisjointForests(g.n)
    
    # Initialize all vertices in the disjoint forest
    for v in range(g.n):
        d.make_set(v)
    
    # Consider only edges with weights <= W
    for i, j, wij in g.edges:
        if wij <= W:
            d.union(i, j)
    
    # Extract a set of sets from the disjoint forest
    return d.dictionary_of_sets()