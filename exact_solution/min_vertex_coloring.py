"""
min_vertex_coloring.py

Exact (optimal) solver for minimum vertex coloring.

Representation:
    - A graph is a dict: {vertex: set_of_neighbors}
      Example:
        G = {
            0: {1, 2},
            1: {0, 2},
            2: {0, 1}
        }  # triangle, chromatic number = 3
"""


def greedy_coloring(graph, order=None):
    """
    Simple greedy coloring to get an upper bound on the chromatic number.

    Parameters:
        graph: dict[int, set[int]]
        order: optional list of vertices specifying the coloring order.
               If None, uses sorted(graph.keys()).

    Returns:
        (num_colors, color_assignment_dict)
    """
    if not graph:
        return 0, {}

    if order is None:
        order = sorted(graph.keys())

    color = {}
    for v in order:
        # Colors used by neighbors
        neighbor_colors = {color[u] for u in graph[v] if u in color}
        # Assign the smallest non-conflicting color (0,1,2,...)
        c = 0
        while c in neighbor_colors:
            c += 1
        color[v] = c

    num_colors = max(color.values()) + 1 if color else 0
    return num_colors, color


def _order_vertices_by_degree(graph):
    """
    Return a list of vertices ordered by descending degree.
    This helps branch and bound prune faster.
    """
    return sorted(graph.keys(), key=lambda v: len(graph[v]), reverse=True)


def _is_color_valid(graph, vertex, c, color_assignment):
    """
    Check whether assigning color c to vertex is valid
    given current color_assignment (partial).
    """
    for neighbor in graph[vertex]:
        if color_assignment.get(neighbor) == c:
            return False
    return True


def _backtrack_coloring(graph, order, index, color_assignment,
                        used_colors, best_num_colors, best_assignment):
    """
    Recursive backtracking with branch-and-bound.

    Parameters:
        graph: dict[int, set[int]]
        order: list[int], fixed vertex order
        index: current index in 'order'
        color_assignment: dict[int, int], partial coloring
        used_colors: current number of distinct colors used so far
        best_num_colors: list with one element: current best known min
        best_assignment: list with one element: best coloring found so far

    Returns:
        None (results are stored in best_num_colors[0] and best_assignment[0])
    """
    # All vertices colored
    if index == len(order):
        if used_colors < best_num_colors[0]:
            best_num_colors[0] = used_colors
            best_assignment[0] = color_assignment.copy()
        return

    # Already using as many or more colors than best known -> prune
    if used_colors >= best_num_colors[0]:
        return

    v = order[index]

    # Try assigning existing colors first
    for c in range(used_colors):
        if _is_color_valid(graph, v, c, color_assignment):
            color_assignment[v] = c
            _backtrack_coloring(graph, order, index + 1,
                                color_assignment, used_colors,
                                best_num_colors, best_assignment)
            del color_assignment[v]  # backtrack

    # Try a new color, if that cannot exceed best_num_colors
    if used_colors + 1 < best_num_colors[0]:
        new_color = used_colors
        if _is_color_valid(graph, v, new_color, color_assignment):
            color_assignment[v] = new_color
            _backtrack_coloring(graph, order, index + 1,
                                color_assignment, used_colors + 1,
                                best_num_colors, best_assignment)
            del color_assignment[v]


def find_minimum_vertex_coloring(graph):
    """
    Compute an optimal vertex coloring for the given graph.

    Parameters:
        graph: dict[int, set[int]]

    Returns:
        (chi, color_assignment_dict)

        chi: integer chromatic number (minimum number of colors needed)
        color_assignment_dict: mapping vertex -> color index (0..chi-1)
    """
    # Trivial cases
    if not graph:
        return 0, {}

    # Get an upper bound with greedy coloring (fast but not necessarily optimal)
    greedy_order = _order_vertices_by_degree(graph)
    upper_bound, greedy_assignment = greedy_coloring(graph, greedy_order)

    # Initialize best with greedy solution
    best_num_colors = [upper_bound]
    best_assignment = [greedy_assignment.copy()]

    # Now run exact backtracking using the same order
    _backtrack_coloring(graph,
                        greedy_order,
                        0,
                        {},
                        0,
                        best_num_colors,
                        best_assignment)

    return best_num_colors[0], best_assignment[0]


def main():
    """
    Example usage from the command line:
    (This is just a demo; for serious testing, see the test file.)

    - Defines a small triangle and path graph and prints their chromatic numbers.
    """
    # Triangle K3: needs 3 colors
    G_triangle = {
        0: {1, 2},
        1: {0, 2},
        2: {0, 1},
    }

    # Path on 4 vertices: needs 2 colors
    G_path4 = {
        0: {1},
        1: {0, 2},
        2: {1, 3},
        3: {2},
    }

    chi_tri, col_tri = find_minimum_vertex_coloring(G_triangle)
    print("Triangle K3: chi =", chi_tri, ", coloring =", col_tri)

    chi_path, col_path = find_minimum_vertex_coloring(G_path4)
    print("Path P4: chi =", chi_path, ", coloring =", col_path)


if __name__ == "__main__":
    main()
