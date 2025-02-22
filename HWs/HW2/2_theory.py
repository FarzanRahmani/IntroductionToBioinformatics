from itertools import permutations

def find_overlap(seq1, seq2):
    """Finds the maximum overlap between suffix of seq1 and prefix of seq2."""
    max_overlap = 0
    overlap_seq = ""
    for i in range(1, min(len(seq1), len(seq2)) + 1):
        if seq1[-i:] == seq2[:i]:
            max_overlap = i
            overlap_seq = seq1 + seq2[i:]
    return max_overlap, overlap_seq

def assemble_sequences(reads):
    """Reconstruct two primary sequences from mixed reads."""
    sequences = list(reads)
    while len(sequences) > 2:
        max_len = -1
        max_seq = None
        seq_to_merge = None
        # Find the pair of sequences with the maximum overlap
        for seq1, seq2 in permutations(sequences, 2):
            overlap_len, merged_seq = find_overlap(seq1, seq2)
            if overlap_len > max_len:
                max_len = overlap_len
                max_seq = merged_seq
                seq_to_merge = (seq1, seq2)
        # Merge the sequences with the maximum overlap
        if seq_to_merge:
            sequences.remove(seq_to_merge[0])
            sequences.remove(seq_to_merge[1])
            sequences.append(max_seq)
    return sequences

# Input mixed reads
reads = [
    "AAGT", "TCTT", "AGTA", "CCAA", "GTAG", "ATCT", "TAGG", 
    "ACCA", "AGGA", "GGAT", "GATT", "ATTT", "ACTC", "CTCG", 
    "TCGC", "TTTG", "GCAT", "CATC", "CTTA", "CGCA", "TTAC", "TACC"
]

# Reconstruct the sequences
primary_sequences = assemble_sequences(reads)

# Output results
for i, seq in enumerate(primary_sequences):
    print(f"Primary Sequence {i+1}: {seq}")