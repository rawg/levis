"""Edge Recombination Operation.

Edge recombination (ERO) is a fairly complicated crossover operation for
permutation encoded GAs. It is useful when the order of values is more
important than their absolute position. For example, when alleles are vertices
in a graph and the fitness function considers edges between then, as in the
Traveling Salesman Problem.

"""

import random

def recombine(parent1, parent2):
    """Return a new chromosome based on two parents via edge recombination.

    Args:
        parent1 (List): A parent chromosome.
        parent2 (List): A parent chromosome.

    Returns:
        List: A new chromosome descended from the parents.
    """

    # Build a child chromosome
    child = []
    node = parent1[0]
    unused = list(parent1)

    while len(child) < len(parent1):
        # Add a node to the child
        child.append(node)
        unused.remove(node)

        # Remove the node from neighbor lists
        for s in neighbors.values():
            if node in s:
                s.remove(node)

        if len(neighbors[node]):
            node = fewest_neighbors(node, neighbors)

        elif len(unused) > 0:
            # Or pick a node at random if the selected node has no neighbors
            node = random.choice(unused)

    return child


def adjacency_matrix(parent1, parent2):
    """Return the union of parent chromosomes adjacency matrices."""
    neighbors = {}
    end = len(parent1) - 1

    for parent in [parent1, parent2]:
        for k, v in enumerate(parent):
            if v not in neighbors:
                neighbors[v] = set()

            if k > 0:
                left = k - 1
            else:
                left = end

            if k < end:
                right = k
            else:
                right = 0

            neighbors[v].add(parent[left])
            neighbors[v].add(parent[right])

    return neighbors


def fewest_neighbors(node, neighbors):
    """Return the neighbor of this node with the fewest neighbors."""
    edges = [(n, len(neighbors[n])) for n in neighbors[node]]
    edges.sort(key=lambda n: n[1])
    return edges[0][0]
