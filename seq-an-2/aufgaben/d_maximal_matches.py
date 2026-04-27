from suffix_tree import SuffixTree
from typing import List


def left_to_right_partition(x: str, y: str) -> List[str]:
    """
    Compute the left-to-right partition of x with respect to y.

    The partition is constructed using the suffix tree of y.

    :param x: The string to partition.
    :param y: The reference string.
    :return: A list of substrings forming the partition of x.
    """
    y_suffix_tree = SuffixTree(y+"$")
    # TODO: Calculate the left-to-right partition of x using y_suffix_tree
    raise NotImplementedError


def partition_size(partition: List[str]) -> int:
    """
    Compute the partition size as defined in the lecture notes.

    :param partition: An alternating list of substrings and characters.
    :return: The size of the partition.
    """
    # TODO: Calculate and return the partition size
    raise NotImplementedError


def d_maximal_matches(x: str, y: str) -> int:
    """
    Compute the maximal matches distance δ(x || y).

    :param x: The source string.
    :param y: The reference string.
    :return: The maximal matches distance.
    """
    # TODO: Compute the maximal matches distance
    raise NotImplementedError