import numpy as np

# Scoreboard as a dictionary
scoreboard = {
    "-": {"-": 0, "A": -1, "T": -1, "C": -1, "G": -1},
    "A": {"-": -1, "A": 2, "T": 1, "C": 0, "G": 0},
    "T": {"-": -1, "A": 1, "T": 2, "C": -1, "G": 1},
    "C": {"-": -1, "A": 0, "T": -1, "C": 3, "G": 2},
    "G": {"-": -1, "A": 0, "T": 1, "C": 2, "G": 3},
}

# Input sequences
sequences = [
    "ACCCTGAACC",
    "ACTCGGAGC",
    "CTGGAATCT",
    "GCTAGGACC",
]

def compute_pairwise_score(seq1, seq2):
    """
    Compute the alignment score between two sequences using dynamic programming.
    """
    len1, len2 = len(seq1), len(seq2)
    dp = np.zeros((len1 + 1, len2 + 1))
    backtrack = np.zeros((len1 + 1, len2 + 1), dtype=str)

    # Initialize the DP table
    for i in range(len1 + 1):
        # dp[i][0] = i * scoreboard["-"]["-"]
        dp[i][0] = i * -1
        backtrack[i][0] = "U"  # Up (gap in target_seq)
    for j in range(len2 + 1):
        # dp[0][j] = j * scoreboard["-"]["-"]
        dp[0][j] = j * -1
        backtrack[0][j] = "L"  # Left (gap in center_seq)

    # Fill the DP table
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            match = dp[i - 1][j - 1] + scoreboard[seq1[i - 1]][seq2[j - 1]]
            delete = dp[i - 1][j] + scoreboard[seq1[i - 1]]["-"]
            insert = dp[i][j - 1] + scoreboard["-"][seq2[j - 1]]
            dp[i][j] = max(match, delete, insert)

            if dp[i][j] == match:
                backtrack[i][j] = "D"  # Diagonal
            elif dp[i][j] == delete:
                backtrack[i][j] = "U"  # Up
            else:
                backtrack[i][j] = "L"  # Left

    # Backtrack to get alignments
    aligned_seq1 = []
    aligned_seq2 = []
    i, j = len1, len2
    while i > 0 or j > 0:
        if backtrack[i][j] == "D":
            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append(seq2[j - 1])
            i -= 1
            j -= 1
        elif backtrack[i][j] == "U":
            aligned_seq1.append(seq1[i - 1])
            aligned_seq2.append("-")
            i -= 1
        elif backtrack[i][j] == "L":
            aligned_seq1.append("-")
            aligned_seq2.append(seq2[j - 1])
            j -= 1

    ####
    print("------------------------------------------")
    print(f"dp table of '{seq1}' and '{seq2}' :")
    print(dp)
    print("\nAligned Sequences:")
    print("".join(reversed(aligned_seq1)))
    print("".join(reversed(aligned_seq2)))
    print("------------------------------------------")
    ####

    return dp[-1][-1]

def find_center_sequence(sequences):
    """
    Find the center sequence that minimizes the sum of pairwise distances.
    """
    n = len(sequences)
    pairwise_scores = np.zeros((n, n))

    # Compute pairwise alignment scores
    for i in range(n):
        for j in range(i + 1, n):
            pairwise_scores[i][j] = compute_pairwise_score(sequences[i], sequences[j])
            pairwise_scores[j][i] = pairwise_scores[i][j]

    ####
    print("------------------------------------------")
    i = 1
    for seq in sequences:
        print(f"sequence {i} = '{seq}'")
        i += 1
    print("pairwise_scores of sequences from each other:")
    print(pairwise_scores)
    print("------------------------------------------")
    ####

    # Compute sum of scores for each sequence
    sum_scores = pairwise_scores.sum(axis=1)
    # center_index = np.argmin(sum_scores) # distance -> arg min
    center_index = np.argmax(sum_scores) # similarity -> arg max

    ####
    print("------------------------------------------")
    print("sum of scores:")
    print(sum_scores)
    print(f"center_index = {center_index}, center_sequence = {sequences[center_index]}")
    print("------------------------------------------")
    ####

    return center_index, pairwise_scores

def align_to_center(center_seq, target_seq):
    """
    Align a sequence to the center sequence using dynamic programming and return aligned sequences.
    """
    len1, len2 = len(center_seq), len(target_seq)
    dp = np.zeros((len1 + 1, len2 + 1))
    backtrack = np.zeros((len1 + 1, len2 + 1), dtype=str)

    # Initialize the DP table
    dp[0][0] = 0
    for i in range(len1):
        # dp[i][0] = i * -1
        dp[i + 1][0] = scoreboard[center_seq[i]]["-"] + dp[i][0]
        backtrack[i][0] = "U"  # Up (gap in target_seq)
    for j in range(len2):
        # dp[0][j] = j * -1
        dp[0][j + 1] = scoreboard["-"][target_seq[j]] + dp[0][j]
        backtrack[0][j] = "L"  # Left (gap in center_seq)

    # Fill the DP table
    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            match = dp[i - 1][j - 1] + scoreboard[center_seq[i - 1]][target_seq[j - 1]]
            delete = dp[i - 1][j] + scoreboard[center_seq[i - 1]]["-"]
            insert = dp[i][j - 1] + scoreboard["-"][target_seq[j - 1]]

            dp[i][j] = max(match, delete, insert)

            if dp[i][j] == match:
                backtrack[i][j] = "D"  # Diagonal
            elif dp[i][j] == delete:
                backtrack[i][j] = "U"  # Up
            else:
                backtrack[i][j] = "L"  # Left

    # Backtrack to get alignments
    aligned_center = []
    aligned_target = []
    i, j = len1, len2

    while i > 0 or j > 0:
        if backtrack[i][j] == "D":
            aligned_center.append(center_seq[i - 1])
            aligned_target.append(target_seq[j - 1])
            i -= 1
            j -= 1
        elif backtrack[i][j] == "U":
            aligned_center.append(center_seq[i - 1])
            aligned_target.append("-")
            i -= 1
        elif backtrack[i][j] == "L":
            aligned_center.append("-")
            aligned_target.append(target_seq[j - 1])
            j -= 1

    print(f"dp table of '{center_seq}' and '{target_seq}' :")
    print(dp)
    # print("\nAligned Sequences:")
    # print("".join(reversed(aligned_seq1)))
    # print("".join(reversed(aligned_seq2)))

    return "".join(reversed(aligned_center)), "".join(reversed(aligned_target))

def multiple_sequence_alignment(sequences):
    """
    Perform multiple sequence alignment using the described algorithm.
    """
    center_index, _ = find_center_sequence(sequences)
    center_seq = sequences[center_index]

    aligned_sequences = [center_seq]
    step = 1
    for i, seq in enumerate(sequences):
        if i != center_index:
            ####
            print(f"step {step}:")
            step += 1
            ####

            aligned_center, aligned_seq = align_to_center(center_seq, seq)
            aligned_sequences.append(aligned_seq)
            center_seq = aligned_center  # Update center sequence with gaps

            ####
            print(f"aligned_center = {aligned_center}, aligned_seq = {aligned_seq}")
            print("------------------------------------------")
            ####

    ####
    print("------------------------------------------")
    print(f"Multiple Alignment = {center_seq}")
    print("------------------------------------------")
    ####

    return aligned_sequences, center_seq

# Run the MSA algorithm
aligned_sequences, aligned_center_seq = multiple_sequence_alignment(sequences)

# Output the results
print("Aligned Sequences iteratively:")
for seq in aligned_sequences:
    print(seq)
