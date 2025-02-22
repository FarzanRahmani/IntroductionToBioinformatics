#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to perform overlap alignment
void perform_overlap_alignment(const char *seq1, const char *seq2, int match_score, int mismatch_penalty, int gap_penalty) {
    int len1 = strlen(seq1);
    int len2 = strlen(seq2);

    // Initialize DP table and backtracking direction table
    int **score_matrix = (int **)malloc((len1 + 1) * sizeof(int *));
    char **backtrack_matrix = (char **)malloc((len1 + 1) * sizeof(char *));
    for (int i = 0; i <= len1; i++) {
        score_matrix[i] = (int *)malloc((len2 + 1) * sizeof(int));
        backtrack_matrix[i] = (char *)malloc((len2 + 1) * sizeof(char));
    }

    int max_score = -2147483648; // Integer.MIN_VALUE equivalent
    int end_i = 0, end_j = 0;

    // Fill DP table and backtrack table
    for (int i = 1; i <= len1; i++) {
        for (int j = 1; j <= len2; j++) {
            int match = (seq1[i - 1] == seq2[j - 1]) ? score_matrix[i - 1][j - 1] + match_score : score_matrix[i - 1][j - 1] + mismatch_penalty;
            int insert = score_matrix[i][j - 1] + gap_penalty;  // Gap in seq1
            int delete = score_matrix[i - 1][j] + gap_penalty;  // Gap in seq2

            if (match >= insert && match >= delete) {
                score_matrix[i][j] = match;
                backtrack_matrix[i][j] = 'D'; // Diagonal (match/mismatch)
            } else if (insert >= delete) {
                score_matrix[i][j] = insert;
                backtrack_matrix[i][j] = 'L'; // Left (gap in seq1)
            } else {
                score_matrix[i][j] = delete;
                backtrack_matrix[i][j] = 'U'; // Up (gap in seq2)
            }

            if (i == len1 || j == len2) {
                if (score_matrix[i][j] > max_score || (score_matrix[i][j] == max_score && (i > end_i || j > end_j))) {
                    max_score = score_matrix[i][j];
                    end_i = i;
                    end_j = j;
                }
            }
        }
    }

    // Backtracking to find the optimal alignment
    char *aligned_seq1 = (char *)malloc((len1 + len2 + 1) * sizeof(char));
    char *aligned_seq2 = (char *)malloc((len1 + len2 + 1) * sizeof(char));
    int index1 = 0, index2 = 0;
    int current_i = end_i, current_j = end_j;

    while (current_i > 0 && current_j > 0) {
        if (backtrack_matrix[current_i][current_j] == 'D') {
            aligned_seq1[index1++] = seq1[current_i - 1];
            aligned_seq2[index2++] = seq2[current_j - 1];
            current_i--;
            current_j--;
        } else if (backtrack_matrix[current_i][current_j] == 'L') {
            aligned_seq1[index1++] = '-';
            aligned_seq2[index2++] = seq2[current_j - 1];
            current_j--;
        } else { // 'U'
            aligned_seq1[index1++] = seq1[current_i - 1];
            aligned_seq2[index2++] = '-';
            current_i--;
        }
    }

    aligned_seq1[index1] = '\0';
    aligned_seq2[index2] = '\0';

    // Reverse the aligned sequences since we built them from end to start
    for (int i = 0; i < index1 / 2; i++) {
        char temp = aligned_seq1[i];
        aligned_seq1[i] = aligned_seq1[index1 - 1 - i];
        aligned_seq1[index1 - 1 - i] = temp;
    }
    for (int i = 0; i < index2 / 2; i++) {
        char temp = aligned_seq2[i];
        aligned_seq2[i] = aligned_seq2[index2 - 1 - i];
        aligned_seq2[index2 - 1 - i] = temp;
    }

    // Trim the aligned sequences to find the actual overlap
    int start_index1 = strcspn(aligned_seq1, "-");
    int start_index2 = strcspn(aligned_seq2, "-");
    int end_index1 = strlen(aligned_seq1) - strspn(aligned_seq1, "-");
    int end_index2 = strlen(aligned_seq2) - strspn(aligned_seq2, "-");

    int start_index = (start_index1 > start_index2) ? start_index1 : start_index2;
    int end_index = (end_index1 < end_index2) ? end_index1 : end_index2;

    aligned_seq1[end_index] = '\0';
    aligned_seq2[end_index] = '\0';

    // Output results
    printf("Max Alignment Score: %d\n", max_score);
    printf("Aligned Sequence 1: %s\n", aligned_seq1);
    printf("Aligned Sequence 2: %s\n", aligned_seq2);

    // Free dynamically allocated memory
    free(aligned_seq1);
    free(aligned_seq2);
    for (int i = 0; i <= len1; i++) {
        free(score_matrix[i]);
        free(backtrack_matrix[i]);
    }
    free(score_matrix);
    free(backtrack_matrix);
}

// Main function to read input and display output
int main() {
    char seq1[1000], seq2[1000];

    // Read sequences from input
    printf("Enter first sequence: ");
    fgets(seq1, sizeof(seq1), stdin);
    seq1[strcspn(seq1, "\n")] = '\0';  // Remove the newline character

    printf("Enter second sequence: ");
    fgets(seq2, sizeof(seq2), stdin);
    seq2[strcspn(seq2, "\n")] = '\0';  // Remove the newline character

    // Run overlap alignment
    perform_overlap_alignment(seq1, seq2, 1, -2, -2);

    return 0;
}
