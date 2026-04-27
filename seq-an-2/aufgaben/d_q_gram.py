from typing import List
import math

# Alphabet size; We presume DNA + 'N' here.
ASIZE = 5

# Mapping for DNA alphabet
CHAR_TO_CODE = {
    "A": 0,
    "C": 1,
    "G": 2,
    "T": 3,
    "N": 4,
}


def get_code(char: str) -> int:
    """
    Convert a character to its numeric code.
    Unknown characters are mapped to "N".
    """
    return CHAR_TO_CODE.get(char, CHAR_TO_CODE["N"])


def get_rank(qgram: str, q: int) -> int:
    """
    Compute the rank of a q-gram interpreted as a number
    in base ASIZE.

    DONE
    Implement the rank computation. Decide whether to use rising or falling ranking.
    The rank corresponds to interpreting the q-gram as a
    number in base ASIZE.
    """
    rank=0
    p=1
    pos = 0
    while pos < q:
        #print("POS: " + str(pos))
        #print("Q: " + str(q))
        # Die erste Position bekommt die Gewichtung 1
        rank+= get_code(qgram[pos]) * p
        # Die Gewichtung wird erhöht
        p *= ASIZE
        # Da die Gewichtung erhöht wird, ist es ein aufsteigendes Ranking
        # Am Ende ist p = p ^ {Q}
        pos += 1
    return rank


def update_rank(
    prev_rank: int,
    left_char: str,
    new_char: str,
    q: int,
) -> int:
    """
    Update the rank when sliding the q-gram window by one position.

    Removes left_char and appends new_char.

    DONE:
    Compute the new rank from the previous rank in O(1) time.
    Note: Use the same system (rising/falling) as in get_rank.

    """

    return (prev_rank//ASIZE) + get_code(new_char) *  int(math.pow(ASIZE, (q-1)))



def get_profile(s: str, q: int) -> List[int]:
    """
    Compute the q-gram profile of string s.

    The profile is a frequency vector containing
    the counts of all possible q-grams.
    """

    # DONE: Compute the maximum possible rank
    max_rank = math.pow(ASIZE , q)
    profile = [0] * int(max_rank)

    if len(s) < q:
        return profile

    # First q-gram.
    # DONE: Compute the rank of the first q-gram and update the profile.
    rank=get_rank(s[0:q], q)
    profile[rank] += 1
    # Remaining q-grams (sliding window).
    # DONE: Iterate over all remaining q-grams.
    # Use update_rank to compute the next rank efficiently
    # and update the profile.

    old_rank = rank
    index = 1
    while index < len(s)-q+1:
        # neuen Rank updaten aus altem
        new_rank = update_rank(old_rank, s[index - 1], s[index + q-1], q )
        # neuen Rank in Array
        profile[new_rank] += 1
        # Neuen alten Rank speichern
        old_rank = new_rank
        index += 1

    return profile



def d_q_gram(a: str, b: str, q: int = 7) -> int:

    """
    Compute the q-gram distance between two strings.

    The distance is the L1 distance between the two
    q-gram profiles.

    DONE:
    Implement the computation of the q-gram distance.
    """
    # Profil des 1 strings berechnen - entspricht pq(a)z
    pa = get_profile(a, q)
    # Profil des 2 Strings berechnen pq(b)z
    pb = get_profile(b, q)
    result = 0
    index = 0
    while index < len(pa) and index < len(pb):                                                   #Summe berechnen
        result += abs(pa[index] - pb[index])
        index += 1

    return result
