from enum import Enum
from typing import Dict, List, Tuple

AA_ALPHABET = ['A', 'R', 'N', 'D', 'C', 'Q', 'E', 'G', 'H', 'I', 'L', 'K', 'M', 'F', 'P', 'S', 'T', 'W', 'Y', 'V']

SIMPLE_SCORE_SCHEME = dict((a, dict((b, -1 if b != a else 1) for b in AA_ALPHABET)) for a in AA_ALPHABET)


class Traceback(Enum):
    TB_ALIGNMENT_START = 1

    TB_LEFT = 2

    TB_UP = 3

    TB_DIAG = 4


class WEResult:
    def __init__(self, score: float, alignment: List[Tuple[str, str]], used_diagonals: List[Tuple[int, int]]):
        self.score = score
        self.alignment = alignment
        self.used_diagonals = used_diagonals


def get_used_diagonals(traceback: List[List[Traceback]], start_coordinate: Tuple[int, int]) -> List[Tuple[int, int]]:
    # TODO: trace back the alignment from the start coordinate to Traceback.TB_ALIGNMENT_START return all used diagonal steps
    i = start_coordinate[0]
    j = start_coordinate[1]
    result: List[Tuple[int, int]] = []
    #print("## start_coordinate: " + str(start_coordinate))
    #print("## traceback[13][10]: " + str(traceback[13][10]))
    while True:
        result.insert(0, (i, j))
        #print("## result: " + str(result))
        #print("## traceback[i][j]: " + str(traceback[i][j]))
        if traceback[i][j] == Traceback.TB_DIAG:
            (i, j) = (i - 1, j - 1)
        elif traceback[i][j] == Traceback.TB_UP:
            i = i - 1
        elif traceback[i][j] == Traceback.TB_LEFT: j = j - 1

        elif traceback[i][j] == Traceback.TB_ALIGNMENT_START:
            break
        else:
            raise NotImplementedError
    return result

def get_alignment(traceback: List[List[Traceback]], start_coordinate: Tuple[int, int]) -> List[Tuple[str, str]]:
    # TODO: trace back the alignment from the start coordinate to Traceback.TB_ALIGNMENT_START and return the full alignment
    i = start_coordinate[0]
    j = start_coordinate[1]
    result: List[Tuple[str, str]] = []
    while True:
        #print(print("(i,j): " + str((i,j))))
        result.insert(0, (i, j))
        if traceback[i][j] == Traceback.TB_DIAG:
            (i, j) = (i - 1, j - 1)
        elif traceback[i][j] == Traceback.TB_UP:
            i = i - 1
        elif traceback[i][j] == Traceback.TB_LEFT: j = j - 1

        elif traceback[i][j] == Traceback.TB_ALIGNMENT_START:
            break
        else:
            raise NotImplementedError
    return result


def local_align(a: str, b: str, score_scheme: Dict[str, Dict[str, float]] = SIMPLE_SCORE_SCHEME,
                gap_score: float = -7.0, forbidden_diagonals: List[Tuple[int, int]] = []) -> WEResult:
    len_a = len(a)
    len_b = len(b)

    # Create (len_a + 1) x (len_b + 1) matrix initialized with 0
    dp = [[0] * (len_b + 1) for _ in range(len_a + 1)]
    traceback = [[Traceback.TB_ALIGNMENT_START] * (len_b + 1) for _ in range(len_a + 1)]
    # Initialize first column (transform a -> empty string)
    for i in range(len_a + 1):
        dp[i][0] = i * gap_score

    # Initialize first row (transform empty string -> b)
    for j in range(len_b + 1):
        dp[0][j] = j * gap_score

    # TODO: Fill the dynamic programming matrix, make sure to not use any forbidden diagonal steps
    max_value = 0
    start_coordinate = (0,0)
    for i in range(1, len_a+1):
        for j in range(1, len_b+1):
            if (i, j) in forbidden_diagonals:
                dp[i][j] = 0
            else:
                diag = dp[i - 1][j - 1] + score_scheme[a[i-1]][b[j-1]]
                up = dp[i - 1][j] - gap_score
                left = dp[i][j - 1] - gap_score

                erg = max(0, int(diag), int(up), int(left))
                #print("Erg: " + str(erg))
                dp[i][j] = erg
                if erg > max_value:
                    max_value = erg
                    start_coordinate = (i,j)

                if (erg == diag):
                    traceback[i][j] = Traceback.TB_DIAG
                elif (erg == up):
                    traceback[i][j] = Traceback.TB_UP
                elif (erg == left):
                    traceback[i][j] = Traceback.TB_LEFT
                else:
                    raise NotImplementedError
    print("max_value: " + str(max_value))
    print("start_coordinate: " + str(start_coordinate))
    # TODO: use get_used_diagonals to find which diagonals are used in the optimal alignment
    used_diagonals = get_used_diagonals(traceback, start_coordinate)
    print("used_diagonals: " + str(used_diagonals))
    # TODO: use get_alignment to get the alignment and combine the result to a WEResult object
    num_alignment = get_alignment(traceback, start_coordinate)
    alignment: List[Tuple[str, str]] = []
    for item in num_alignment:
        i: int = int(item[0])
        j: int = int(item[1])
        new_item = (a[i-1],b[j-1])
        alignment.append(new_item)
    print("alignment: " + str(alignment))

    we_res =  WEResult(max_value, alignment, used_diagonals)
    return we_res

def waterman_eggert(a: str, b: str, top_n=1) -> List[WEResult]:
    results: List[WEResult] = []
    for i in range(top_n):
        print(i)
        # TODO: calculate the best top_n local alignments without diagonal re-use using the local alignment function
        if i > 0:
            forbidden_diagonals = results[i-1].used_diagonals
        else:
            forbidden_diagonals = []
        print(forbidden_diagonals)
        results.append(local_align(a,b, SIMPLE_SCORE_SCHEME, -7.0, forbidden_diagonals))
    return results


if __name__ == "__main__":
    a = "AACCTTTTTTTCA"
    b = "ACTTGGTGCA"
    for result in waterman_eggert(a, b):
        print(result.alignment)
