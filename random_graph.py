import numpy as np
import numpy.random as rand

def random_graph(n=3, edge_prob=3, seed=None):
    """Generate random Erdos-Renyi graph for MaxCut.

    Args:
        n (int): number of nodes.
        edge_prob (float): probability of edge appearing.


    Returns:
        numpy.ndarray: adjacency matrix.

    """
    
    w = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            if rand.rand() <= edge_prob:
                w[i, j] = 1
    w += w.T

    return w