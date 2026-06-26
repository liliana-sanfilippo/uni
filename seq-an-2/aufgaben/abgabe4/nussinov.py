from typing import Dict, Tuple


RNA_ALPHABET = "ACGU"

# initialize all pairs with -infinity
DEFAULT_SCORE = {
    (x, y): float("-inf")
    for x in RNA_ALPHABET
    for y in RNA_ALPHABET
}

# allowed base pairs
#DEFAULT_SCORE[("G", "C")] = 3
#DEFAULT_SCORE[("C", "G")] = 3

#DEFAULT_SCORE[("A", "U")] = 2
#DEFAULT_SCORE[("U", "A")] = 2

#DEFAULT_SCORE[("G", "U")] = 1
#DEFAULT_SCORE[("U", "G")] = 1

DEFAULT_SCORE[("G", "C")] = 1
DEFAULT_SCORE[("C", "G")] = 1

DEFAULT_SCORE[("A", "U")] = 0
DEFAULT_SCORE[("U", "A")] = 0

DEFAULT_SCORE[("G", "U")] = 1
DEFAULT_SCORE[("U", "G")] = 1



def nussinov_matrix(rna: str, delta : float = 1.0, score_scheme : Dict[(Tuple[str,str],float)] = DEFAULT_SCORE) -> float:
    # TODO Implement the Nussinov algorithm
    result: Dict[(Tuple[int,int],float)] = {}
    n = len(rna)

    # mit Nullen initialisieren, damit nichts leer ist und meckert
    for i in range(0, n):
        for j in range(0, n):
            result[(i, j)] = 0

    # statt for i in range(2, len(str)) um eines verschieben, wegen 0 Start
    for i in range(1, n):
        #print((i, i-1))
        result[(i, i-1)] = 0

    for d in range(0, int(delta)):
        for i in range(0, n):
            #print((i, i+d))
            j = i+d
            if j-i <= delta:
                result[(i, j)] = 0
            else:
                result[(i, i+d)] = max(
                    result[(i+1,j)],
                    result[(i,j-1)],
                    result[(i+1,j-1)] + DEFAULT_SCORE[(rna[i], rna[j])]
                )

    for d in range(int(delta)+1, n):
        for i in range(0, n-d):
            j = i+d
            if j-i <= delta:
                result[(i, j)] = 0
            else:
                if j-i > delta+1:
                    split = max(
                        result[(i,k-1)] + result[(k,j)]
                        for k in range(i+2,j)
                    )
                else:
                    split = 0

                result[(i, j)] = max(
                    result[(i+1,j)],
                    result[(i,j-1)],
                    result[(i+1,j-1)] + DEFAULT_SCORE[(rna[i], rna[j])],
                    split
                )

    print_matrix(result, n)
    print(result[(0, n-1)])
    return result[(0, n-1)]


def print_matrix(result, n):
    for i in range(n):
        for j in range(n):
            print(result[(i,j)], end="\t")
        print()