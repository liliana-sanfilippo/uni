def d_edit(a: str, b: str) -> int:
    """
    Compute the Levenshtein edit distance between two strings.

    The edit distance is the minimum number of insertions,
    deletions, and substitutions required to transform
    string `a` into string `b`.
    """
    len_a = len(a)
    len_b = len(b)

    # Create (len_a + 1) x (len_b + 1) matrix initialized with 0
    dp = [[0] * (len_b + 1) for _ in range(len_a + 1)]

    # Initialize first column (transform a -> empty string)
    for i in range(len_a + 1):
        dp[i][0] = i

    # Initialize first row (transform empty string -> b)
    for j in range(len_b + 1):
        dp[0][j] = j

    # Fill the dynamic programming table
    for i in range(1, len_a + 1):
        for j in range(1, len_b + 1):
            insertion = dp[i][j - 1] + 1
            deletion = dp[i - 1][j] + 1
            substitution = dp[i - 1][j - 1]

            if a[i - 1] != b[j - 1]:
                substitution += 1

            dp[i][j] = min(insertion, deletion, substitution)

    return dp[len_a][len_b]
