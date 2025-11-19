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
    - vertex_name is exactly the name used in the input file,
    - color is an integer in {0, 1, ..., k-1}.

Input format (from file):

    n m
    u1 v1
    u2 v2
    ...
    um vm

Where:
    - n is the number of vertices,
    - m is the number of edges,
    - each ui vi is an undirected edge between vertex ui and vertex vi.
    - ui, vi are arbitrary vertex labels (e.g., a, b, c or 0, 1, 2).
"""

import sys


def read_graph_from_file(path):
    """
    Read an undirected graph with arbitrary vertex labels.

    Returns:
        graph          : dict[int, set[int]]
                         adjacency list on internal indices 0..n-1
        index_to_label : list[str]
                         index_to_label[i] is the original vertex label
                         corresponding to internal index i
    """
    with open(path, "r") as f:
        header = f.readline().strip()
        if not header:
            raise ValueError("Empty input file")

        parts = header.split()
        if len(parts) != 2:
            raise ValueError("First line must contain exactly two tokens: n m")

        n = int(parts[0])
        m = int(parts[1])

        raw_edges = []
        labels = set()

        for _ in range(m):
            line = f.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            u_label, v_label = line.split()

            if u_label == v_label:
                # Ignore self-loops if present
                continue

            raw_edges.append((u_label, v_label))
            labels.add(u_label)
            labels.add(v_label)

    # Create a deterministic mapping from labels to internal indices
    # Sort labels so output order is lexicographic by original vertex name
    sorted_labels = sorted(labels)

    # NOTE: if len(sorted_labels) != n, the file header and actual labels
    # don't match; we still proceed, but this indicates malformed input.
    # If your grading requires strict checking, you could raise here.

    label_to_index = {lab: i for i, lab in enumerate(sorted_labels)}
    index_to_label = sorted_labels[:]  # index -> original label

    # Build adjacency list on internal indices
    graph = {i: set() for i in range(len(index_to_label))}
    for u_lab, v_lab in raw_edges:
        u = label_to_index[u_lab]
        v = label_to_index[v_lab]
        graph[u].add(v)
        graph[v].add(u)

    return graph, index_to_label


def is_safe_to_color(graph, vertex_order, index, color_assignment, color):
    """
    Check whether 'color' can be assigned to vertex vertex_order[index]
    without conflicting with already-colored neighbors.
    """
    v = vertex_order[index]
    for neighbor in graph[v]:
        if neighbor in color_assignment and color_assignment[neighbor] == color:
            return False
    return True


def backtrack_with_k_colors(graph, vertex_order, index, color_assignment, max_colors):
    """
    Backtracking search to try to color all vertices using colors 0..max_colors-1.
    """
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

            # Backtrack
            del color_assignment[v]

    return False


def find_minimum_vertex_coloring(graph):
    """
    Exact minimum coloring by trying k = 1..n with backtracking.

    Returns:
        (chi, color_assignment) where:
          chi              : int, chromatic number
          color_assignment : dict[int, int], mapping internal index -> color
    """
    if not graph:
        return 0, {}

    vertices = list(graph.keys())
    n = len(vertices)

    for k in range(1, n + 1):
        color_assignment = {}
        if backtrack_with_k_colors(graph, vertices, 0, color_assignment, k):
            return k, color_assignment

    # Theoretically unreachable: every graph is n-colorable
    raise RuntimeError(
        "Unreachable: failed to color graph with up to n colors.")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 cs412_mingraphcoloring_exact.py <graph_file>")
        sys.exit(1)

    graph_file = sys.argv[1]
    graph, index_to_label = read_graph_from_file(graph_file)

    chi, coloring = find_minimum_vertex_coloring(graph)

    # First line: chromatic number
    print(chi)

    # Next lines: vertex_name color
    # Sort by original vertex label to get a consistent order.
    idxs_sorted_by_label = sorted(
        range(len(index_to_label)), key=lambda i: index_to_label[i]
    )

    for i in idxs_sorted_by_label:
        if i in coloring:
            v_label = index_to_label[i]
            print(f"{v_label} {coloring[i]}")


if __name__ == "__main__":
    main()
