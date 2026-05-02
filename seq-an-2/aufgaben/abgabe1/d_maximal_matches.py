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
    partition = []
    i = 0
    current = ""

    while i < len(x):
        longest_match = y_suffix_tree.search_prefix(x[i:])
        long_len = len(longest_match)

        # wenn match und aktuelles match nicht leer
        if long_len > 0 and current:
            zsm = current[-1] + longest_match[0]
            # ist neue kombo in y?
            check = y_suffix_tree.search_prefix(zsm)
            # wenn kombi in y und nicht leer
            if len(check) == len(zsm):
                # hinzufügen
                partition.append(current)
                # das x[i] ist dann der seperator, das was bi im Skript ist
                partition.append(x[i])
                current = ""
                i += 1
                continue

        # wenn match aber aktuelle sleer
        if long_len > 0:
            # aktuelles nicht leer machen
            current += longest_match
            i += long_len

        # wenn kein match ist es sep
        else:
            partition.append(current)
            partition.append(x[i])
            current = ""
            i += 1

    partition.append(current)

    return partition


def partition_size(partition: List[str]) -> int:
    """
    Compute the partition size as defined in the lecture notes.

    :param partition: An alternating list of substrings and characters.
    :return: The size of the partition.
    """
    # DONE: Calculate and return the partition size
    if len(partition) == 0 or (len(partition) == 1 and partition[0] == ""):
        return 0

    count = 0
    # jedes zweite halt
    for i in range(1, len(partition), 2):
        count += 1

    return count


def d_maximal_matches(x: str, y: str) -> int:
    """
    Compute the maximal matches distance δ(x || y).

    :param x: The source string.
    :param y: The reference string.
    :return: The maximal matches distance.
    """
    # DONE: Compute the maximal matches distance
    partition = left_to_right_partition(x, y)
    return partition_size(partition)