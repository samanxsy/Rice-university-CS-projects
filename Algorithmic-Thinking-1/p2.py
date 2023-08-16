# Rice University
#
# Algorithmic Thinking - P2
#
# Written for Python 2 
#
# Saman Saybani


import random
from collections import deque


def bfs_visited(ugraph, start_node):
    '''
    This function takes an undirected graph and returns set of nodes that are visited
    '''
    queue = deque()
    visited_node = set([start_node])
    queue.append(start_node)
    
    while len(queue) > 0:
        node = queue.popleft()

        for i in ugraph[node]:
            if i not in visited_node:
                visited_node.add(i)
                queue.append(i)

    return visited_node


def cc_visited(ugraph):
    '''
    This function takes an undirected graph and returns list of sets where each set consists of all the nodes in a connected component
    '''
    un_visited_node = ugraph.keys()
    un_visited_node = set(un_visited_node)
    connected = []

    while len(un_visited_node) > 0:
        node = random.sample(un_visited_node, 1)[0]
        current_node = bfs_visited(ugraph, node)
        connected.append(current_node)

        for i in current_node:
            un_visited_node.remove(i)

    return connected


def largest_cc_size(ugraph):
    '''
    This function takes an undirected graph and returns the size of largest connected component
    '''
    size = 0
    connection = cc_visited(ugraph)

    for comp in connection:
        if len(comp) > size:
            size = len(comp)

    return size


def compute_resilience(ugraph, attack_order):
    '''
    Takes in undirected graph and a list of nodes
    '''
    size_list = []
    graph = ugraph.copy()

    size_list.append(largest_cc_size(graph))

    for i in attack_order:
        graph.pop(i)

        for nodes in graph:
            graph[nodes].discard(i)

        size_list.append(largest_cc_size(graph))

    return size_list
