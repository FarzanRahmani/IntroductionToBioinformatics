def load_blosum62():
    '''
        Load the BLOSUM62 scoring matrix
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
    with open(filename, 'r') as file:
        sequences = []
        seq = ''
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

# def global_alignment_affine_gap(s, t, scoring_matrix, gap_open, gap_extend):
#     '''
#         Global alignment with affine gap penalties using dynamic programming
#     '''

#     len_s = len(s)
#     len_m = len(t)
    
#     # Initialize DP matrices
#     M = [[0] * (len_m + 1) for _ in range(len_s + 1)]  # Match matrix (Stores the maximum score for aligning s[:j] and t[:i])
#     s_gaps = [[0] * (len_m + 1) for _ in range(len_s + 1)]  # Gap in s (Tracks scores for gaps in sequence s)
#     t_gaps = [[0] * (len_m + 1) for _ in range(len_s + 1)]  # Gap in t (Tracks scores for gaps in sequence t)
    
#     # Track paths for traceback
#     M_tb = [[None] * (len_m + 1) for _ in range(len_s + 1)]
#     s_gaps_tb = [[None] * (len_m + 1) for _ in range(len_s + 1)]
#     t_gaps_tb = [[None] * (len_m + 1) for _ in range(len_s + 1)]
    
#     # Initialize first row and column with gap penalties
#     for i in range(1, len_s + 1):
#         s_gaps[i][0] = -gap_open - (i - 1) * gap_extend
#         M[i][0] = -float('inf')
#         t_gaps[i][0] = -float('inf')
#     for j in range(1, len_m + 1):
#         t_gaps[0][j] = -gap_open - (j - 1) * gap_extend
#         M[0][j] = -float('inf')
#         s_gaps[0][j] = -float('inf')
    
#     # Fill DP matrices
#     for i in range(1, len_s + 1):
#         for j in range(1, len_m + 1):
#             match_score = scoring_matrix[s[i - 1]][t[j - 1]]
            
#             # Calculate scores for M, s_gaps, and t_gaps matrices
#             M[i][j] = max(M[i - 1][j - 1] + match_score, s_gaps[i - 1][j - 1] + match_score, t_gaps[i - 1][j - 1] + match_score)
#             s_gaps[i][j] = max(M[i - 1][j] - gap_open, s_gaps[i - 1][j] - gap_extend)
#             t_gaps[i][j] = max(M[i][j - 1] - gap_open, t_gaps[i][j - 1] - gap_extend)
            
#             # Track the path for traceback
#             if M[i][j] == M[i - 1][j - 1] + match_score:
#                 M_tb[i][j] = ('M', i - 1, j - 1)
#             elif M[i][j] == s_gaps[i - 1][j - 1] + match_score:
#                 M_tb[i][j] = ('s_gaps', i - 1, j - 1)
#             else:
#                 M_tb[i][j] = ('t_gaps', i - 1, j - 1)
            
#             if s_gaps[i][j] == M[i - 1][j] - gap_open:
#                 s_gaps_tb[i][j] = ('M', i - 1, j)
#             else:
#                 s_gaps_tb[i][j] = ('s_gaps', i - 1, j)
            
#             if t_gaps[i][j] == M[i][j - 1] - gap_open:
#                 t_gaps_tb[i][j] = ('M', i, j - 1)
#             else:
#                 t_gaps_tb[i][j] = ('t_gaps', i, j - 1)
    
#     # Find the maximum score at the bottom-right corner (last element)
#     max_score = max(M[len_s][len_m], s_gaps[len_s][len_m], t_gaps[len_s][len_m])
    
#     if max_score == M[len_s][len_m]:
#         matrix = 'M'
#     elif max_score == s_gaps[len_s][len_m]:
#         matrix = 's_gaps'
#     else:
#         matrix = 't_gaps'
    
#     # Traceback to find the aligned sequences
#     aligned_s = []
#     aligned_t = []
#     i, j = len_s, len_m

#     while i > 0 or j > 0:
#         if matrix == 'M':
#             prev_matrix, i, j = M_tb[i][j]
#         elif matrix == 's_gaps':
#             prev_matrix, i, j = s_gaps_tb[i][j]
#             aligned_t.append('-')
#             aligned_s.append(s[i])
#         elif matrix == 't_gaps':
#             prev_matrix, i, j = t_gaps_tb[i][j]
#             aligned_s.append('-')
#             aligned_t.append(t[j])
#         matrix = prev_matrix
    
#     # Reverse the alignments to get the final result
#     aligned_s = ''.join(reversed(aligned_s))
#     aligned_t = ''.join(reversed(aligned_t))
    
#     return max_score, aligned_s, aligned_t

def global_alignment_affine_gap(s, t, scoring_matrix, gap_open, gap_extend):
    '''
        Global alignment with affine gap penalties using dynamic programming
    '''

    len_s = len(s)
    len_t = len(t)
    
    # Initialize DP matrices
    M = [[0] * (len_t + 1) for _ in range(len_s + 1)]  # Match matrix (Stores the maximum score for aligning s[:j] and t[:i])
    s_gaps = [[0] * (len_t + 1) for _ in range(len_s + 1)]  # Gap in s (Tracks scores for gaps in sequence s)
    t_gaps = [[0] * (len_t + 1) for _ in range(len_s + 1)]  # Gap in t (Tracks scores for gaps in sequence t)

    # Track paths for traceback
    M_tb = [[None] * (len_t + 1) for _ in range(len_s + 1)]
    s_gaps_tb = [[None] * (len_t + 1) for _ in range(len_s + 1)]
    t_gaps_tb = [[None] * (len_t + 1) for _ in range(len_s + 1)]
    
    # Initialize first row and column with gap penalties
    for i in range(1, len_s + 1):
        s_gaps[i][0] = -gap_open - (i - 1) * gap_extend
        M[i][0] = -float('inf')
        t_gaps[i][0] = -float('inf')
    for j in range(1, len_t + 1):
        t_gaps[0][j] = -gap_open - (j - 1) * gap_extend
        M[0][j] = -float('inf')
        s_gaps[0][j] = -float('inf')
    
    # Fill DP matrices
    for i in range(1, len_s + 1):
        for j in range(1, len_t + 1):
            match_score = scoring_matrix[s[i - 1]][t[j - 1]]
            
            # Calculate scores for M, s_gaps, and t_gaps matrices
            M[i][j] = max(M[i - 1][j - 1] + match_score, s_gaps[i - 1][j - 1] + match_score, t_gaps[i - 1][j - 1] + match_score)
            s_gaps[i][j] = max(M[i - 1][j] - gap_open, s_gaps[i - 1][j] - gap_extend)
            t_gaps[i][j] = max(M[i][j - 1] - gap_open, t_gaps[i][j - 1] - gap_extend)
            
            # Track the path for traceback
            if M[i][j] == M[i - 1][j - 1] + match_score:
                M_tb[i][j] = ('M', i - 1, j - 1)
            elif M[i][j] == s_gaps[i - 1][j - 1] + match_score:
                M_tb[i][j] = ('s_gaps', i - 1, j - 1)
            else:
                M_tb[i][j] = ('t_gaps', i - 1, j - 1)
            
            if s_gaps[i][j] == M[i - 1][j] - gap_open:
                s_gaps_tb[i][j] = ('M', i - 1, j)
            else:
                s_gaps_tb[i][j] = ('s_gaps', i - 1, j)
            
            if t_gaps[i][j] == M[i][j - 1] - gap_open:
                t_gaps_tb[i][j] = ('M', i, j - 1)
            else:
                t_gaps_tb[i][j] = ('t_gaps', i, j - 1)
    
    # Find the maximum score at the bottom-right corner (last element)
    max_score = max(M[len_s][len_t], s_gaps[len_s][len_t], t_gaps[len_s][len_t])
    
    # Determine the starting matrix for traceback
    if max_score == M[len_s][len_t]:
        matrix = 'M'
    elif max_score == s_gaps[len_s][len_t]:
        matrix = 's_gaps'
    else:
        matrix = 't_gaps'
    
    # Traceback to find the aligned sequences
    aligned_s = []
    aligned_t = []
    i, j = len_s, len_t

    while i > 0 or j > 0:
        if matrix == 'M':
            aligned_s.append(s[i - 1])
            aligned_t.append(t[j - 1])
            prev_matrix, i, j = M_tb[i][j]
        elif matrix == 's_gaps':
            aligned_s.append(s[i - 1])
            aligned_t.append('-')
            prev_matrix, i, j = s_gaps_tb[i][j]
        elif matrix == 't_gaps':
            aligned_s.append('-')
            aligned_t.append(t[j - 1])
            prev_matrix, i, j = t_gaps_tb[i][j]
        matrix = prev_matrix
    
    # Reverse the alignments to get the final result
    aligned_s = ''.join(reversed(aligned_s))
    aligned_t = ''.join(reversed(aligned_t))
    
    return max_score, aligned_s, aligned_t


def main():
    '''
        Main function to compute alignment score
    '''
    # Parse sequences from the input file
    sequences = parse_fasta_from_file("rosalind_gaff.txt")
    s = sequences[0]
    t = sequences[1]
    
    # Load the BLOSUM62 matrix
    scoring_matrix = load_blosum62()
    
    # Define gap opening and extension penalties (affine gap penalty)
    gap_open_penalty = 11
    gap_extend_penalty = 1
    
    # Calculate the maximum alignment score and the aligned sequences
    max_score, aligned_s, aligned_t = global_alignment_affine_gap(s, t, scoring_matrix, gap_open_penalty, gap_extend_penalty)
    
    # Print the results
    print(max_score)
    print(aligned_s)
    print(aligned_t)

if __name__ == "__main__":
    main()
