import numpy as np

def calculate_total_distances(distance_matrix):
    """Calculate the total distance for each row in the distance matrix."""
    return [sum(row) for row in distance_matrix]

def construct_nj_matrix(distance_matrix, total_distances):
    """Construct the Neighbor-Joining matrix."""
    n = len(distance_matrix)
    nj_matrix = np.zeros_like(distance_matrix)
    for x in range(n):
        for y in range(n):
            if x != y:
                nj_matrix[x][y] = (n - 2) * distance_matrix[x][y] - total_distances[x] - total_distances[y]
    return nj_matrix

def find_min_non_diagonal(matrix):
    """Find the indices of the minimum non-diagonal element in a matrix."""
    min_value = np.inf
    min_indices = (-1, -1)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i != j and matrix[i][j] < min_value:
                min_value = matrix[i][j]
                min_indices = (i, j)
    return min_indices

def update_distance_matrix(distance_matrix, idx_i, idx_j):
    """Update the distance matrix with a new row/column."""
    n = len(distance_matrix)
    new_row = [
        0.5 * (distance_matrix[idx_i][k] + distance_matrix[idx_j][k] - distance_matrix[idx_i][idx_j])
        for k in range(n) if k != idx_i and k != idx_j
    ]
    
    updated_matrix = []
    for x in range(n):
        if x != idx_i and x != idx_j:
            updated_row = [
                distance_matrix[x][y] for y in range(n) if y != idx_i and y != idx_j
            ]
            updated_matrix.append(updated_row)
    
    updated_matrix.append(new_row)
    for i, row in enumerate(updated_matrix):
        if len(row) < len(updated_matrix):
            row.append(new_row[i] if i < len(new_row) else 0)
    
    return np.array(updated_matrix)

def neighbor_joining(distance_matrix, num_leaves):
    """Perform the Neighbor-Joining algorithm."""
    tree_edges = []
    active_nodes = list(range(num_leaves))
    next_internal_node = num_leaves  # Start numbering internal nodes after leaves

    while len(distance_matrix) > 2:
        # Step 1: Compute total distances for each node
        total_distances = calculate_total_distances(distance_matrix)

        # Step 2: Construct the Neighbor-Joining matrix
        nj_matrix = construct_nj_matrix(distance_matrix, total_distances)

        # Step 3: Find the pair of nodes to merge
        node_i, node_j = find_min_non_diagonal(nj_matrix)

        # Step 4: Compute limb lengths
        delta_value = (total_distances[node_i] - total_distances[node_j]) / (len(distance_matrix) - 2)
        limb_i = 0.5 * (distance_matrix[node_i][node_j] + delta_value)
        limb_j = 0.5 * (distance_matrix[node_i][node_j] - delta_value)

        # Step 5: Add edges to the tree
        tree_edges.append((active_nodes[node_i], next_internal_node, round(limb_i, 3)))
        tree_edges.append((next_internal_node, active_nodes[node_i], round(limb_i, 3)))
        tree_edges.append((active_nodes[node_j], next_internal_node, round(limb_j, 3)))
        tree_edges.append((next_internal_node, active_nodes[node_j], round(limb_j, 3)))

        # Step 6: Update the distance matrix
        distance_matrix = update_distance_matrix(distance_matrix, node_i, node_j)

        # Step 7: Update the active nodes
        active_nodes.append(next_internal_node)
        active_nodes = [node for idx, node in enumerate(active_nodes) if idx != node_i and idx != node_j]
        next_internal_node += 1

    # Step 8: Add the final edge
    tree_edges.append((active_nodes[0], active_nodes[1], round(distance_matrix[0][1], 3)))
    tree_edges.append((active_nodes[1], active_nodes[0], round(distance_matrix[0][1], 3)))

    return tree_edges

def format_tree_edges(tree_edges):
    """Format the adjacency list for output."""
    tree_edges.sort(key=lambda edge: (edge[0], edge[1]))
    formatted = [f"{edge[0]}->{edge[1]}:{edge[2]:.3f}" for edge in tree_edges]
    return "\n".join(formatted)

n = int(input())
distance_matrix = []
for __ in range(0, n, 1):
    distance_matrix.append(list(map(int, input().split())))

resulting_tree = neighbor_joining(np.array(distance_matrix), n)
print(format_tree_edges(resulting_tree))
