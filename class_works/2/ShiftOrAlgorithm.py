def approximate_string_matching(S, p):
    n, k = len(S), len(p)
    ALPHABET = {'A', 'C', 'G', 'T'}
    
    # Step 1: Preprocess pattern
    bitmask = {char: 0 for char in ALPHABET}
    for i, char in enumerate(p):
        bitmask[char] |= (1 << i)
    
    # Step 2: Initialize masks
    D_exact = (1 << k) - 1  # All bits set to 1 initially
    D_mismatch = (1 << k) - 1  # All bits set to 1 initially
    
    match_positions = []
    
    # Step 3: Process the string S
    for i in range(n):
        char = S[i]
        # Update the bitmask for exact matches
        D_new_exact = ((D_exact << 1) | bitmask[char]) & ((1 << k) - 1)
        
        # Update the bitmask for one mismatch allowed
        D_new_mismatch = (((D_exact << 1) | bitmask[char]) | (D_mismatch << 1)) & ((1 << k) - 1)
        
        # Update the masks
        D_exact = D_new_exact
        D_mismatch = D_new_mismatch
        
        # Step 4: Check if there is a match
        if D_new_exact & (1 << (k-1)) or D_new_mismatch & (1 << (k-1)):
            match_positions.append(i - k + 1)
    
    return match_positions

S = "AACGTA"
P = "AA"
print(f"String: {S}\nPattern: {P}")
print(approximate_string_matching(S, P))
print()

S = "AACGTAA"
P = "CG"
print(f"String: {S}\nPattern: {P}")
print(approximate_string_matching(S, P))
print()

S = "AACGTTAACGTTAACGTTAA"
P = "CGTT"
print(f"String: {S}\nPattern: {P}")
print(approximate_string_matching(S, P))
print()