from collections import defaultdict, deque

def has_cycle(g):
    """
    Returns True if graph g contains any cycle.
    Undirected graph.
    """

    visited = set()

    for start in g:
        if start not in visited:
            if _dfs_detect_cycle(g, start, None, visited):
                return True
    return False


def _dfs_detect_cycle(g, node, parent, visited):
    visited.add(node)
    for nei in g.get(node, []):
        if nei == node:
            # self loop
            return True
        if nei not in visited:
            if _dfs_detect_cycle(g, nei, node, visited):
                return True
        elif nei != parent:
            # A visited neighbor not equal to parent is a cycle
            return True
    return False


def find_cycle(g):
    """
    Returns a list of nodes representing a cycle,
    with first == last, or None if no cycle.
    """
    visited = set()
    parent = {}

    for start in g:
        if start not in visited:
            cycle = _dfs_find_cycle(g, start, None, visited, parent)
            if cycle is not None:
                return cycle
    return None


def _dfs_find_cycle(g, node, parent, visited, parent_map):
    visited.add(node)
    parent_map[node] = parent

    for nei in g.get(node, []):
        if nei == node:
            # self loop cycle
            return [node, node]

        if nei not in visited:
            parent_map[nei] = node
            cyc = _dfs_find_cycle(g, nei, node, visited, parent_map)
            if cyc is not None:
                return cyc
        elif nei != parent:
            # Found a cycle; reconstruct it
            return _reconstruct_cycle(node, nei, parent_map)

    return None


def _reconstruct_cycle(a, b, parent_map):
    """
    Reconstructs a cycle path between nodes a and b.
    a and b are neighbors and already visited (undirected cycle).
    """

    # Path from a to root
    path_a = []
    x = a
    while x is not None:
        path_a.append(x)
        x = parent_map[x]
    path_a = path_a[::-1]  # reverse to root→a

    # Path from b to root
    path_b = []
    y = b
    while y is not None:
        path_b.append(y)
        y = parent_map[y]
    path_b = path_b[::-1]

    # Find lowest common ancestor (LCA)
    i = 0
    while i < len(path_a) and i < len(path_b) and path_a[i] == path_b[i]:
        i += 1
    i -= 1  # last common index

    lca = path_a[i]

    # Build cycle:
    # LCA → ... → a
    part1 = path_a[i:]
    # LCA → ... → b (reverse direction because cycle closes)
    part2 = path_b[i:]
    part2 = part2[::-1]

    cycle = part1 + part2[1:]  # avoid duplicating LCA
    cycle.append(cycle[0])     # close cycle
    return cycle
