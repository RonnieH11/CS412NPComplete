import sys
import numpy as np

def read_graph_from_stdin():
    vertices = set()
    edges = []
    for line in sys.stdin:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        u, v = parts[0], parts[1]
        vertices.update([u, v])
        edges.append((u, v))
    vertices = sorted(vertices)
    index = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    A = np.zeros((n, n), dtype=float)
    for u, v in edges:
        i, j = index[u], index[v]
        A[i, j] = 1
        A[j, i] = 1
    return A

def hoffman_lower_bound(A):
    eigenvalues = np.linalg.eigvalsh(A)  
    lambda_max = max(eigenvalues)
    lambda_min = min(eigenvalues)
    if lambda_min == 0:  
        return 1
    bound = 1 + lambda_max / abs(lambda_min)
    return int(np.ceil(bound))  

def main():
    A = read_graph_from_stdin()
    bound = hoffman_lower_bound(A)
    print(bound)

if __name__ == "__main__":
    main()
