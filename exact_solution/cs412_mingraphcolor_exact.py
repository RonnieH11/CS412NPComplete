#!/usr/bin/env python3
"""
cs412_mingraphcoloring_exact.py

Exact (guaranteed optimal) solver for the minimum vertex coloring problem.

Output format (to stdout):

    <k>
    <vertex_name> <color>
    <vertex_name> <color>
    ...

Where:
    - k is the chromatic number (minimum number of colors),
    - vertex_name is the vertex id from the input (here assumed 0..n-1),
    - color is an integer in {0, 1, ..., k-1}.

Input format (from file or stdin):

    n
    u1 v1
    u2 v2
    ...
    (edges until EOF)

OR

    n m
    u1 v1
    u2 v2
    ...
    um vm

Where:
    - n is the number of vertices (vertices are 0,1,...,n-1),
    - m is the number of edges (can be ignored when reading),
    - each ui vi is an undirected edge between ui and vi.
"""

import sys


def read_graph(stream):
    """
    Read an undirected graph with numeric vertex labels 0..n-1
    from the given text stream (file or stdin).

    Supports both header formats:
        n
        n m

    Returns:
        graph          : dict[int, set[int]] adjacency list
        index_to_label : list[str] where index_to_label[i] = str(i)
    """
    header = stream.readline()
    if not header:
        # Empty input
        return {}, []

    header = header.strip()
    if not header:
        # Skip empty lines at start if any
        while header == "":
            header = stream.readline()
            if not header:
                return {}, []
            header = header.strip()

    parts = header.split()
    if len(parts) == 1:
        n = int(parts[0])
    elif len(parts) == 2:
        n = int(parts[0])
        # m = int(parts[1])  # we don't actually need m
    else:
        raise ValueError("First line must be 'n' or 'n m'")

    # Initialize adjacency list for all vertices 0..n-1
    graph = {i: set() for i in range(n)}

    # Read edges until EOF
    for line in stream:
        line = line.strip()
        if not line:
            continue
        tokens = line.split()
        if len(tokens) != 2:
            # Ignore malformed lines silently; or raise if your spec demands
            continue
        u_str, v_str = tokens
        u = int(u_str)
        v = int(v_str)
        if u == v:
            continue
        if 0 <= u < n and 0 <= v < n:
            graph[u].add(v)
            graph[v].add(u)
        else:
            # Ignore out-of-range vertices; or raise if required
            continue

    index_to_label = [str(i) for i in range(n)]
    return graph, index_to_label


def is_safe_to_color(graph, vertex_order, index, color_assignment, color):
    v = vertex_order[index]
    for neighbor in graph[v]:
        if neighbor in color_assignment and color_assignment[neighbor] == color:
            return False
    return True


def backtrack_with_k_colors(graph, vertex_order, index, color_assignment, max_colors):
    if index == len(vertex_order):
        return True

    v = vertex_order[index]

    for c in range(max_colors):
        if is_safe_to_color(graph, vertex_order, index, color_assignment, c):
            color_assignment[v] = c
            if backtrack_with_k_colors(
                graph, vertex_order, index + 1, color_assignment, max_colors
            ):
                return True
            del color_assignment[v]

    return False


def find_minimum_vertex_coloring(graph):
    """
    Exact minimum coloring by trying k = 1..n with backtracking.

    Returns:
        (chi, color_assignment) where:
          chi              : int, chromatic number
          color_assignment : dict[int, int], mapping vertex -> color
    """
    if not graph:
        return 0, {}

    vertices = sorted(graph.keys())
    n = len(vertices)

    for k in range(1, n + 1):
        color_assignment = {}
        if backtrack_with_k_colors(graph, vertices, 0, color_assignment, k):
            return k, color_assignment

    # Theoretically unreachable: every graph is n-colorable
    raise RuntimeError(
        "Unreachable: failed to color graph with up to n colors.")


def main():
    # If a filename is provided, read from that file. Otherwise, read from stdin.
    if len(sys.argv) >= 2:
        with open(sys.argv[1], "r") as f:
            graph, index_to_label = read_graph(f)
    else:
        graph, index_to_label = read_graph(sys.stdin)

    chi, coloring = find_minimum_vertex_coloring(graph)

    # Print chromatic number
    print(chi)

    # Print vertex-color assignments in order 0..n-1
    for i in range(len(index_to_label)):
        # Every vertex should have a color
        c = coloring.get(i, 0)
        print(f"{index_to_label[i]} {c}")


if __name__ == "__main__":
    main()
