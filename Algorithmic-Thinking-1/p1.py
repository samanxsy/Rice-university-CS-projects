# Algortihmic Thinking - Rice University
#
# Written for python 2
#
# Saman Saybani


def make_complete_graph(num_nodes):
    '''
    This function takes number of nodes and returns dictionary with complete directed graph.
    '''
    graph = {}

    for node in range(num_nodes):
        nodes = set([])

        for i in range(num_nodes):
            if node != i:
                nodes.add(i)

        graph[node] = nodes

    return graph


def compute_in_degrees(digraph):
    '''
    This Function takes in a digraph and computes the in-degrees for each node.
    '''
    degree = dict.fromkeys(digraph, 0)
    
    for node in digraph:
        for edge in digraph[node]:
            degree[edge] += 1

    return degree


def in_degree_distribution(digraph):
    '''
    This function takes in a digraph and computes the unnormalized distribution for the in-degrees
    '''
    computer = compute_in_degrees(digraph)
    distro = {}

    for node in computer:
        degree = computer[node]

        if degree not in distro:
            distro[degree] = 1

        else:
            distro[degree] += 1

    return distro
