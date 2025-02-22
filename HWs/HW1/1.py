from Bio.Align import substitution_matrices
# substitution_matrix = substitution_matrices.load('BLOSUM62')  # Load BLOSUM62

def load_blosum62():
    '''
        Load the BLOSUM62 scoring matrix from a text file
    '''
    blosum62 = {}
    with open("blosum62.txt") as file:
        amino_acids = file.readline().split()
        for line in file:
            parts = line.split()
            blosum62[parts[0]] = {amino_acids[i]: int(parts[i + 1]) for i in range(len(amino_acids))}
    return blosum62

def parse_fasta_from_file(filename):
    '''
        Parse FASTA format strings from a file
    '''
    sequences = []
    seq = ''
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('>'):
                if seq:
                    sequences.append(seq)
                    seq = ''
            else:
                seq += line.strip()
        if seq:
            sequences.append(seq)
    return sequences

def global_alignment_affine_gap(s, t, scoring_matrix, gap_open_penalty, gap_extend_penalty):
    '''
        Global alignment with an affine gap penalty
    '''
    n = len(s)
    m = len(t)
    
    # Initialization of scoring matrices
    M = [[0] * (m + 1) for _ in range(n + 1)]  # Match matrix (Stores the maximum score for aligning s[:j] and t[:i])
    s_gaps = [[0] * (m + 1) for _ in range(n + 1)]  # Gap in s (Tracks scores for gaps in sequence s)
    t_gaps = [[0] * (m + 1) for _ in range(n + 1)]  # Gap in t (Tracks scores for gaps in sequence t)
    
    for i in range(1, n + 1):
        M[i][0] = float('-inf')
        s_gaps[i][0] = -gap_open_penalty - (i - 1) * gap_extend_penalty
        t_gaps[i][0] = float('-inf')
    
    for j in range(1, m + 1):
        M[0][j] = float('-inf')
        s_gaps[0][j] = float('-inf')
        t_gaps[0][j] = -gap_open_penalty - (j - 1) * gap_extend_penalty
    
    # Fill the DP tables
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            # Match/mismatch score
            score = scoring_matrix[s[i - 1]][t[j - 1]]
            
            # Update M matrix
            M[i][j] = max(
                M[i - 1][j - 1] + score,
                s_gaps[i - 1][j - 1] + score,
                t_gaps[i - 1][j - 1] + score
            )
            
            # Update s_gaps matrix
            s_gaps[i][j] = max(
                M[i - 1][j] - gap_open_penalty,
                s_gaps[i - 1][j] - gap_extend_penalty
            )
            
            # Update t_gaps matrix
            t_gaps[i][j] = max(
                M[i][j - 1] - gap_open_penalty,
                t_gaps[i][j - 1] - gap_extend_penalty
            )
    
    # The maximum score for the alignment
    max_score = max(M[n][m], s_gaps[n][m], t_gaps[n][m])
    
    return max_score

def main():
    '''
        Main function to compute alignment score
    '''

    # Load and parse the FASTA input file
    sequences = parse_fasta_from_file("rosalind_gcon.txt")
    s = sequences[0]
    t = sequences[1]
    
    # Load blosum62
    scoring_matrix = load_blosum62()
    
    # Define gap penalties
    gap_open_penalty = 5
    gap_extend_penalty = 0
    
    # Calculate the alignment score
    max_score = global_alignment_affine_gap(s, t, scoring_matrix, gap_open_penalty, gap_extend_penalty)
    # max_score = global_alignment_affine_gap(s, t, substitution_matrix, gap_open_penalty, gap_extend_penalty)

    print(max_score)

main()