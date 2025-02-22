def overlap_alignment(s, t, match_score=1, mismatch_penalty=-2, gap_penalty=-2):
    len_s = len(s)
    len_t = len(t)

    # Initialize DP table and traceback table
    dp = [[0] * (len_t + 1) for _ in range(len_s + 1)]
    traceback = [[None] * (len_t + 1) for _ in range(len_s + 1)]

    # Initialize the scoring for the ends of s (rows) and the beginning of t (columns)
    for i in range(1, len_s + 1):
        dp[i][0] = 0  # No penalty for aligning with an empty prefix of t
        traceback[i][0] = 'up'
    for j in range(1, len_t + 1):
        dp[0][j] = 0  # No penalty for aligning with an empty prefix of s
        traceback[0][j] = 'left'

    # Fill the DP table
    max_score = float('-inf')
    max_position = (0, 0)
    for i in range(1, len_s + 1):
        for j in range(1, len_t + 1):
            match = dp[i - 1][j - 1] + (match_score if s[i - 1] == t[j - 1] else mismatch_penalty)
            delete = dp[i - 1][j] + gap_penalty
            insert = dp[i][j - 1] + gap_penalty

            # Choose the maximum score with priority order
            dp[i][j] = max(match, delete, insert, 0)  # 0 to reset if no alignment is preferable

            if dp[i][j] == match:
                traceback[i][j] = 'diag'
            elif dp[i][j] == delete:
                traceback[i][j] = 'up'
            elif dp[i][j] == insert:
                traceback[i][j] = 'left'

            # Update max score and position if it's at the end of s or the beginning of t
            if i == len_s or j == len_t:
                if dp[i][j] > max_score:
                    max_score = dp[i][j]
                    max_position = (i, j)

    # Backtrack to find the aligned substrings
    i, j = max_position
    aligned_s = []
    aligned_t = []

    while i > 0 and j > 0 and dp[i][j] != 0:
        if traceback[i][j] == 'diag':
            aligned_s.append(s[i - 1])
            aligned_t.append(t[j - 1])
            i -= 1
            j -= 1
        elif traceback[i][j] == 'up':
            aligned_s.append(s[i - 1])
            aligned_t.append('-')
            i -= 1
        elif traceback[i][j] == 'left':
            aligned_s.append('-')
            aligned_t.append(t[j - 1])
            j -= 1

    # Reverse the aligned strings since we constructed them from end to start
    aligned_s.reverse()
    aligned_t.reverse()

    # Print the results
    print(max_score)
    print(''.join(aligned_s))
    print(''.join(aligned_t))

# Read the input strings
s = input().strip()
t = input().strip()

# Run the overlap alignment
overlap_alignment(s, t)