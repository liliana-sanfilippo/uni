from typing import List

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

    TODO:
    Implement the rank computation. Decide whether to use rising or falling ranking.
    The rank corresponds to interpreting the q-gram as a
    number in base ASIZE.
    """
    raise NotImplementedError


def update_rank(
    prev_rank: int,
    left_char: str,
    new_char: str,
    q: int,
) -> int:
    """
    Update the rank when sliding the q-gram window by one position.

    Removes left_char and appends new_char.

    TODO:
    Compute the new rank from the previous rank in O(1) time.
    Note: Use the same system (rising/falling) as in get_rank.

    """
    pass


def get_profile(s: str, q: int) -> List[int]:
    """
    Compute the q-gram profile of string s.

    The profile is a frequency vector containing
    the counts of all possible q-grams.
    """

    # TODO: Compute the maximum possible rank
    raise NotImplementedError
    max_rank = None
    profile = [0] * max_rank

    if len(s) < q:
        return profile

    # First q-gram.
    # TODO:
    # Compute the rank of the first q-gram and update the profile.

    # Remaining q-grams (sliding window).
    # TODO:
    # Iterate over all remaining q-grams.
    # Use update_rank to compute the next rank efficiently
    # and update the profile.

    return profile


def d_q_gram(a: str, b: str, q: int = 7) -> int:
    """
    Compute the q-gram distance between two strings.

    The distance is the L1 distance between the two
    q-gram profiles.

    TODO:
    Implement the computation of the q-gram distance.
    """
    raise NotImplementedError
