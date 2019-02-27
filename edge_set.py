import numpy as np

def edge_set(graph_matrix):
    """
    Generate the set of edges as a list of tuples
    
    Args:
        graph_matrix (numpy.ndarray): adjacency matrix for graph
        
    Returns:
        List of tuples
    """
    
    edgelist=[]
    for i in range(graph_matrix.shape[0]):
        for j in range(i):
            if graph_matrix[i,j]==1:
                edgelist.append((i,j))
    return edgelist