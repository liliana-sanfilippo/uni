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

DEFAULT_SCORE[("A", "U")] = 1
DEFAULT_SCORE[("U", "A")] = 1

DEFAULT_SCORE[("G", "U")] = 1
DEFAULT_SCORE[("U", "G")] = 1



def nussinov_matrix(rna: str, delta : float = 1.0, score_scheme : Dict[(Tuple[str,str],float)] = DEFAULT_SCORE) -> float:
    # TODO Implement the Nussinov algorithm
    result: Dict[(Tuple[int,int],float)] = {}
    n = len(rna)+1

    rna = "X" + rna

    # mit Nullen initialisieren, damit nichts leer ist und meckert
    for i in range(1, n):
        for j in range(1, n):
            result[(i, j)] = 0

    # statt for i in range(2, len(str)) um eines verschieben, wegen 0 Start
    for i in range(2, n):
        #print((i, i-1))
        result[(i, i-1)] = 0

    for d in range(0,n-1):
        for i in range(1,n-d):
            j=i+d
            #if i == 1 and j == 4:
            #    print(j - i > delta)
            if j - i > delta:
                #print(str(i) + ", " + str(j) + " sind " + rna[i] + " und " + rna[j] + "")
                pair_score = result[(i+1,j-1)] + score_scheme.get((rna[i], rna[j]), 0)
                if pair_score == float("-inf"):
                    pair_score = 0

                #if i == 1 and j == 4:
                #    print(result[(i+1,j-1)])
                #    print((i+1,j-1))
                #    print(pair_score)

                maxi = {
                    result[(i,k)] + result[(k+1,j)]
                    for k in range(i,j)
                }
                if maxi:
                    split = max(
                        maxi
                    )
                else:
                    split = 0


                result[(i,j)] = max(
                    result[(i+1,j)],
                    result[(i,j-1)],
                    pair_score,
                    split
                )
                #print("from result[(i+1,j)] = " + str(result[(i+1,j)]) + ", result[(i,j-1)] = " + str(result[(i,j-1)])
                #      + ", pair_score = " + str(pair_score) + " und split = " + str(split) + " ist result[(" + str(i) +
                #      "," + str(j) + ")] = " + str(result[(i,j)]) )
            #else:
            #    print("result[(" + str(i) + "," + str(j) + ")] = 0, weil " + str(j) + "-" + str(i) + " = " + str(j-i)
            #          + " <= " + str(delta))

    #print("-----------")
    #print_matrix(result, n)
    print(result[(1, n-1)])
    return result[(1, n-1)]


def print_matrix(result, n):
    for i in range(1,n):
        for j in range(1,n):
            print(result[(i,j)], end="\t")
        print()