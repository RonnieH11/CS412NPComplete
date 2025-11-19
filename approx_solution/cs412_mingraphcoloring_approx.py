def main():
    num_segs = int(input())

    adj_list = {}

    for _ in range(num_segs):
        u, v = input().split()
        if u not in adj_list:
            adj_list[u] = {}
        if v not in adj_list:
            adj_list[v] = {}

        adj_list[u][v] = None
        adj_list[v][u] = None
    

# Greedy choice, pick node with largest number of
# neighbor colors, break ties with maximum degree
def min_graph_coloring(adj_list):
    pass


if __name__ == "__main__":
    main()