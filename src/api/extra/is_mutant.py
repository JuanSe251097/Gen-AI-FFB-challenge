def is_mutant(dna):
    def check_sequence(sequence):
        # Check if a sequence contains more than 4 consecutive identical letters
        return any(sequence[i:i+4] == sequence[i] * 4 for i in range(len(sequence) - 3))

    n = len(dna)
    count = 0

    # Check rows (horizontal)
    for row in dna:
        if check_sequence(row):
            count += 1

    # Check columns (vertical)
    for col in range(n):
        column_sequence = ''.join(dna[row][col] for row in range(n))
        if check_sequence(column_sequence):
            count += 1

    # Check diagonals (both directions)
    for d in range(-n + 1, n):
        diag1 = ''.join(dna[i][i + d] for i in range(max(0, -d), min(n, n - d)))
        diag2 = ''.join(dna[i][n - i - d - 1] for i in range(max(0, d), min(n, n - d)))
        if check_sequence(diag1) or check_sequence(diag2):
            count += 1

    return count > 1  # A mutant requires more than one valid sequence


# Example Usage:
dna = ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]
print(is_mutant(dna))  # Output: True

