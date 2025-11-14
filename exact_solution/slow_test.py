"""
slow_test.py

THIS FILE IS NOT A UNIT TEST.
It is intentionally slow.

It creates a random dense graph and runs the exact minimum vertex
coloring algorithm. This test is meant to take > 1 minute on typical
hardware to demonstrate NP-hard performance.

Run manually:
    python slow_stress_test.py
"""

import time
import random
from min_vertex_coloring import find_minimum_vertex_coloring


# -------------------------------------------------------------
# CONFIGURATION — Adjust these to make the test easier or harder
# -------------------------------------------------------------

NUM_VERTICES = 50      # 16–20 is good for >1 minute runtime
EDGE_PROBABILITY = 0.7   # 0.50–0.70 makes graphs very hard to color


def generate_random_graph(n, p):
    """
    Generate an undirected random graph G(n, p).
    Graph represented as adjacency dict: {vertex: set(neighbors)}.
    """
    graph = {i: set() for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            if random.random() < p:
                graph[i].add(j)
                graph[j].add(i)
    return graph


def main():
    print("Generating random graph...")
    G = generate_random_graph(NUM_VERTICES, EDGE_PROBABILITY)

    print(f"Graph has {NUM_VERTICES} vertices.")
    approx_edges = sum(len(v) for v in G.values()) // 2
    print(f"Approximate edges: {approx_edges}")
    print("This may take several minutes...\n")

    start = time.time()
    chi, coloring = find_minimum_vertex_coloring(G)
    end = time.time()

    print(f"Chromatic number: {chi}")
    print(f"Coloring (vertex -> color): {coloring}")
    print(f"\nRuntime: {end - start:.2f} seconds")


if __name__ == "__main__":
    main()
