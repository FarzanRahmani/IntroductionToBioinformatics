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

def calculate_max_gaps(seq1, seq2):
    '''
        Function to calculate the maximum number of gap symbols in an optimal alignment
    '''
    len_seq1 = len(seq1)
    len_seq2 = len(seq2)

    # Initialize the alignment matrix with zero values
    alignment_matrix = [[0] * (len_seq1 + 1) for _ in range(len_seq2 + 1)] # Using a 2D list (array) of size (m+1) x (n+1) for dynamic programming table

    # Fill the alignment matrix based on LCS matching rules
    for j in range(1, len_seq2 + 1): # Iterate over each character of seq2 (outer loop)
        for i in range(1, len_seq1 + 1): # Iterate over each character of seq1 (inner loop)
            if seq1[i - 1] == seq2[j - 1]:  
                # If characters match, increment the value from the diagonal cell
                alignment_matrix[j][i] = alignment_matrix[j - 1][i - 1] + 1
            else:  
                # If characters do not match, take the maximum from the left or top cell
                alignment_matrix[j][i] = max(alignment_matrix[j][i - 1], alignment_matrix[j - 1][i])

    # The length of the Longest Common Subsequence (LCS) is found at the bottom-right cell
    lcs_length = alignment_matrix[len_seq2][len_seq1]

    # Calculate the maximum number of gaps in the optimal alignment
    # Total gaps = (length of seq1 + length of seq2) - 2 * LCS length
    max_gaps = (len_seq1 + len_seq2) - 2 * lcs_length

    return max_gaps


def main():
    '''
        Main function to run the alignment and find the result
    '''
    # Parse sequences from the input file
    sequences = parse_fasta_from_file("rosalind_mgap.txt")
    s = sequences[0]
    t = sequences[1]

    # Get the maximum number of gaps in the optimal alignment
    max_gaps = calculate_max_gaps(s, t)
    print(max_gaps)

if __name__ == "__main__":
    main()
