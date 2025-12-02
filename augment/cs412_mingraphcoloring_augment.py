import sys
import numpy as np
import math

def read_graph_from_stdin():
    edges = []
    vertices = set()

    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        parts = line.split()
        if len(parts) != 2:
            continue

        u, v = parts
        vertices.add(u)
        vertices.add(v)
        edges.append((u, v))

    return list(vertices), edges

def build_adjacency_matrix(vertices, edges):
    n = len(vertices)
    index = {v: i for i, v in enumerate(vertices)}

    A = np.zeros((n, n), dtype=float)

    for u, v in edges:
        i = index[u]
        j = index[v]
        A[i][j] = 1.0
        A[j][i] = 1.0

    return A

def hoffman_lower_bound(A):
    if A.size == 0:
        return 1

    eigenvalues = np.linalg.eigvals(A)
    lmax = max(eigenvalues)
    lmin = min(eigenvalues)

    # Hoffman formula
    bound = 1 - (lmax / lmin)
    return max(1, math.ceil(bound.real))

def main():
    vertices, edges = read_graph_from_stdin()
    A = build_adjacency_matrix(vertices, edges)
    lb = hoffman_lower_bound(A)
    print(lb)

if __name__ == "__main__":
    main()
