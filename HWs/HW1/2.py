def load_pam250():
    '''
        Load the PAM250 scoring matrix
    '''
    pam250 = {}
    with open("pam250.txt") as file:
        amino_acids = file.readline().split()
        for line in file:
            parts = line.split()
            pam250[parts[0]] = {amino_acids[i]: int(parts[i + 1]) for i in range(len(amino_acids))}
    return pam250

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

def local_alignment(s, t, scoring_matrix, gap_penalty):
    '''
        Local alignment using the Smith-Waterman algorithm
    '''
    len_s = len(s)
    len_t = len(t)
    dp = [[0] * (len_t + 1) for _ in range(len_s + 1)]
    max_score = 0
    max_pos = None

    # Fill the DP table and track the maximum score position
    for i in range(1, len_s + 1):
        for j in range(1, len_t + 1):
            match = dp[i - 1][j - 1] + scoring_matrix[s[i - 1]][t[j - 1]]
            delete = dp[i - 1][j] - gap_penalty
            insert = dp[i][j - 1] - gap_penalty
            dp[i][j] = max(0, match, delete, insert)
            if dp[i][j] > max_score:
                max_score = dp[i][j]
                max_pos = (i, j)

    # Backtrack to find the optimal local alignment
    i, j = max_pos
    aligned_s = []
    aligned_t = []
    while i > 0 and j > 0 and dp[i][j] > 0:
        if dp[i][j] == dp[i - 1][j - 1] + scoring_matrix[s[i - 1]][t[j - 1]]: # match
            aligned_s.append(s[i - 1])
            aligned_t.append(t[j - 1])
            i -= 1
            j -= 1
        elif dp[i][j] == dp[i - 1][j] - gap_penalty: # delete
            aligned_s.append(s[i - 1])
            # aligned_t.append('-')
            i -= 1
        else:  # insert:    dp[i][j] == dp[i][j - 1] - gap_penalty
            # aligned_s.append('-')
            aligned_t.append(t[j - 1])
            j -= 1

    return max_score, ''.join(reversed(aligned_s)), ''.join(reversed(aligned_t))

def main():
    '''
        Main function to compute local alignment
    '''

    # Parse sequences from the input file
    sequences = parse_fasta_from_file("rosalind_local.txt")
    s = sequences[0]
    t = sequences[1]
    
    # Load the PAM250 matrix
    scoring_matrix = load_pam250()
    
    # Define the linear gap penalty
    linear_gap_penalty = 5
    
    # Calculate and print the maximum alignment score and substrings
    max_score, aligned_s, aligned_t = local_alignment(s, t, scoring_matrix, linear_gap_penalty)
    
    # print results
    print(max_score)
    print(aligned_s)
    print(aligned_t)

# Run the main function
if __name__ == "__main__":
    main()
