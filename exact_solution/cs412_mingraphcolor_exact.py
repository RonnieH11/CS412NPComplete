"""
cs412_mingraphcoloring_exact.py

Exact (optimal) solver for minimum vertex coloring problem.

"""

import sys


def read_graph(stream):
    # Read first non-empty line
    header = stream.readline()
    if not header:
        return {}, []

    header = header.strip()
    while header == "":
        header = stream.readline()
        if not header:
            return {}, []
        header = header.strip()

    parts = header.split()

    edges = []
    vertex_labels = set()
    header_n = None   # number of vertices from header
    header_m = None   # number of edges from header

    def add_edge(u_lbl, v_lbl):
        # skip self loops
        if u_lbl == v_lbl:
            return
        vertex_labels.add(u_lbl)
        vertex_labels.add(v_lbl)
        edges.append((u_lbl, v_lbl))

    # Helper to read up to m edges or until EOF
    def read_m_edges(m):
        read_edges = 0
        while read_edges < m:
            line = stream.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue
            tokens = line.split()
            if len(tokens) != 2:
                continue
            u_lbl, v_lbl = tokens
            add_edge(u_lbl, v_lbl)
            read_edges += 1

    # Parse header
    if len(parts) == 2 and all(p.lstrip("-").isdigit() for p in parts):
        # n m format
        header_n = int(parts[0])
        header_m = int(parts[1])
        read_m_edges(header_m)

    elif len(parts) == 1 and parts[0].lstrip("-").isdigit():
        # Single int, treat as edge count m
        header_m = int(parts[0])
        read_m_edges(header_m)

    elif len(parts) == 2:
        # treat as first edge u v
        u_lbl, v_lbl = parts
        add_edge(u_lbl, v_lbl)
        for line in stream:
            line = line.strip()
            if not line:
                continue
            tokens = line.split()
            if len(tokens) != 2:
                continue
            u_lbl, v_lbl = tokens
            add_edge(u_lbl, v_lbl)

    else:
        raise ValueError("Unexpected header format")

    # If we saw no vertices but do know n, assume isolated vertices 0..n-1
    if not vertex_labels and header_n is not None:
        vertex_labels.update(str(i) for i in range(header_n))

    # Empty graph.
    if not vertex_labels:
        return {}, []

    # Map original labels -> 0..N-1, with numeric labels sorted numerically
    def label_key(lbl: str):
        s = lbl.lstrip("-")
        if s.isdigit():
            return (0, int(lbl))
        return (1, lbl)

    labels_sorted = sorted(vertex_labels, key=label_key)
    label_to_index = {lbl: i for i, lbl in enumerate(labels_sorted)}
    index_to_label = labels_sorted[:]  # preserve order

    # Build adjacency list on indices
    graph = {i: set() for i in range(len(labels_sorted))}
    for u_lbl, v_lbl in edges:
        u = label_to_index[u_lbl]
        v = label_to_index[v_lbl]
        if u == v:
            continue
        graph[u].add(v)
        graph[v].add(u)

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
