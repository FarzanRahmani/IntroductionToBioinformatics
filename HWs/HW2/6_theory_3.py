import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram
import numpy as np

# Results from UPGMA
steps = [
    ('(D,E)', 1.5),
    ('(B,F)', 2.0),
    ('(G,(D,E))', 2.25),
    ('(A,(B,F))', 3.0),
    ('(C,(G,(D,E)))', 3.5),
    ('((A,(B,F)),(C,(G,(D,E))))', 4.583333333333333)
]

# Mapping labels to numerical indices for visualization
labels = ["A", "B", "C", "D", "E", "F", "G"]
label_map = {label: i for i, label in enumerate(labels)}

# Function to parse clusters correctly considering nested parentheses
def parse_cluster(cluster_str):
    stack = []
    current = []
    for char in cluster_str:
        if char == "(":
            stack.append(current)
            current = []
        elif char == ")":
            if current:
                stack[-1].append("".join(current))
            current = stack.pop()
        elif char == ",":
            if current:
                stack[-1].append("".join(current))
                current = []
        else:
            current.append(char)
    return stack[0] if stack else current

# Convert UPGMA steps to linkage matrix format
linkage_matrix = []
current_cluster_index = len(labels)  # New clusters get indices >= len(labels)

for step in steps:
    cluster, height = step
    parsed_cluster = parse_cluster(cluster)  # Parse the cluster string into its components

    # Ensure cluster has exactly two elements
    assert len(parsed_cluster) == 2, f"Expected 2 elements, got {len(parsed_cluster)}: {parsed_cluster}"

    # Convert parsed cluster labels to indices
    cluster_indices = [
        label_map["(" + ",".join(label.split(",")) + ")"] if label not in label_map else label_map[label]
        for label in parsed_cluster
    ]

    # Determine the size of the new cluster
    size = sum([1 if isinstance(label, int) else len(label.split(",")) for label in parsed_cluster])

    # Append the new step to the linkage matrix
    linkage_matrix.append([cluster_indices[0], cluster_indices[1], height, size])

    # Update mapping for the new cluster
    new_cluster_label = "(" + ",".join(sorted(parsed_cluster)) + ")"
    label_map[new_cluster_label] = current_cluster_index
    current_cluster_index += 1

# Convert linkage_matrix to numpy array
linkage_matrix = np.array(linkage_matrix)

# Plot the dendrogram
plt.figure(figsize=(10, 6))
dendrogram(linkage_matrix, labels=labels)
plt.title("UPGMA Dendrogram")
plt.xlabel("Clusters")
plt.ylabel("Height")
plt.show()
