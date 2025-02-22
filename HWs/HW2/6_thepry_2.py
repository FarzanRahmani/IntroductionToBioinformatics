import numpy as np
import pandas as pd

# Define the distance matrix again
labels = ["A", "B", "C", "D", "E", "F", "G"]
matrix = np.array([
    [0, 5, 9, 9, 8, 7, 12],  # A
    [5, 0, 10, 10, 7, 4, 11], # B
    [9, 10, 0, 8, 7, 10, 6],  # C
    [9, 10, 8, 0, 3, 9, 5],   # D
    [8, 7, 7, 3, 0, 6, 4],    # E
    [7, 4, 10, 9, 6, 0, 9],   # F
    [12, 11, 6, 5, 4, 9, 0]   # G
])

# Create a DataFrame for easier handling
dist_df = pd.DataFrame(matrix, index=labels, columns=labels)

def upgma_weighted(distance_matrix):
    """
    Perform UPGMA clustering using weighted average.

    Parameters:
    - distance_matrix: DataFrame representing the distance matrix.

    Returns:
    - clustering_steps: List of tuples showing clustering steps.
    """
    clusters = {label: [label] for label in distance_matrix.index}
    cluster_sizes = {label: 1 for label in distance_matrix.index}
    distances = distance_matrix.copy()
    steps = []
    
    while len(clusters) > 1:
        # Find the closest pair of clusters
        min_dist = np.inf
        closest_pair = None
        for i in distances.index:
            for j in distances.columns:
                if i != j and distances.at[i, j] < min_dist:
                    min_dist = distances.at[i, j]
                    closest_pair = (i, j)
        
        # Merge the closest clusters
        c1, c2 = closest_pair
        new_cluster = f"({c1},{c2})"
        new_size = cluster_sizes[c1] + cluster_sizes[c2]
        clusters[new_cluster] = clusters.pop(c1) + clusters.pop(c2)
        cluster_sizes[new_cluster] = new_size
        steps.append((new_cluster, min_dist / 2))
        
        # Update the distance matrix using weighted average
        for cluster in distances.index:
            if cluster not in closest_pair:
                size_c1 = cluster_sizes[c1]
                size_c2 = cluster_sizes[c2]
                weighted_distance = (
                    size_c1 * distances.at[c1, cluster] +
                    size_c2 * distances.at[c2, cluster]
                ) / new_size
                distances.at[new_cluster, cluster] = weighted_distance
                distances.at[cluster, new_cluster] = weighted_distance
        
        distances = distances.drop(index=[c1, c2], columns=[c1, c2])
        distances.at[new_cluster, new_cluster] = 0

        print(distances)
        print("-----------------------------------")
    
    return steps

print(dist_df)
print("-----------------------------------")
# Perform UPGMA with weighted average
upgma_weighted_steps = upgma_weighted(dist_df)
print("steps:")
i = 1
for step in upgma_weighted_steps:
    print(f"step {i}:", step)
    i += 1


