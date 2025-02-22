import numpy as np

# Sequences
x = "GCAC"
y = "GCC"

# Scoring system
match_score = 2
mismatch_score = -2
gap_open = -5
gap_extend = -1

# Matrix dimensions
m, n = len(x), len(y)

# Initialize matrices: M, Ix, Iy
M = np.zeros((m + 1, n + 1))
Ix = np.zeros((m + 1, n + 1))
Iy = np.zeros((m + 1, n + 1))

# Initialize gap matrices with negative infinity initially
M.fill(-np.inf)
Ix.fill(-np.inf)
Iy.fill(-np.inf)

# Setting the initial values
M[0, 0] = 0
for i in range(1, m + 1):
    Ix[i, 0] = gap_open + (i - 1) * gap_extend
    M[i, 0] = gap_open + (i - 1) * gap_extend
for j in range(1, n + 1):
    Iy[0, j] = gap_open + (j - 1) * gap_extend
    M[0, j] = gap_open + (j - 1) * gap_extend

# Fill matrices using dynamic programming
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if x[i - 1] == y[j - 1]:
            score = match_score
        else:
            score = mismatch_score
        
        Ix[i, j] = max(Ix[i - 1, j] + gap_extend, M[i - 1, j] + gap_open)
        Iy[i, j] = max(Iy[i, j - 1] + gap_extend, M[i, j - 1] + gap_open)
        M[i, j] = max(M[i - 1, j - 1] + score, Ix[i, j], Iy[i, j])

# Extracting the final alignment score
alignment_score = M[m, n]
print(alignment_score)
print("M")
print(M)
print("Ix")
print(Ix)
print("Iy")
print(Iy)