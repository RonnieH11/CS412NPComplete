"""
cs412_mingraphcoloring_approx.py

Approximation algorithm to solve min
vertex color problem in polynomial time.

Analytical Runtime: O(V + E)
"""


import random

def main():
    # Number of edges
    num_segs = int(input())

    # Build adjacency list
    adj_list = {}
    for _ in range(num_segs):
        u, v = input().split()
        if u not in adj_list:
            adj_list[u] = set()
        if v not in adj_list:
            adj_list[v] = set()

        adj_list[u].add(v)
        adj_list[v].add(u)
    
    # get the colors for each vertex
    vertex_colors = min_graph_coloring_approx(adj_list)

    # Number of colors used (+ 1 because values start at 0)
    num_colors = max(vertex_colors.values()) + 1
    print(num_colors)

    # Print each vertex and its color
    for v in sorted(vertex_colors.keys()):
        print(f"{v} {vertex_colors[v]}")

    

# Greedy choice, For each vertex, give it the 
# smallest color that is not used by its neighbors
def min_graph_coloring_approx(adj_list):
    # Shuffle the vertices to reduce worst case behavior
    vertices = list(adj_list.keys())
    random.shuffle(vertices)

    vertex_colors = {}

    # For each vertex
    # O(V)
    for v in vertices:
        # Find all the colors adjacent to v
        seen_colors = set()
        # Degree of E O(E)
        for neighbor in adj_list[v]:
            if neighbor in vertex_colors:
                seen_colors.add(vertex_colors[neighbor])

        # Assign the lowest color that isn't used by the neighbors
        color = 0
        # O(E)
        while color in seen_colors:
            color += 1
        vertex_colors[v] = color
    
    return vertex_colors


if __name__ == "__main__":
    main()