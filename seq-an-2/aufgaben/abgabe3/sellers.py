from typing import List, Tuple

from anaconda_project.internal.conda_api import result


def sellers(text: str, query: str, threshold: int) -> List[Tuple[int, int]]:
    """
    Compute all approximate matches of `query` in `text`
    using Sellers' algorithm.

    Returns:
        A list of tuples (end_index, score) where:
        - end_index is the last index of the match in `text`
        - score is the edit distance
        Only matches with score <= threshold are returned.

    Example:
        sellers("ATA", "ATT", 1) == [(2, 1)]
    """
    results: List[Tuple[int, int]] = []

    #initialize start column
    start_column = []
    for i in range(len(query)+1):
        start_column.append(i)
        i+=1


    for index, character in enumerate(text):
        #compute next column from current column and character
            column = [0] * (len(query)+1)
            for i in range(1,len(query)+1):
                sub = start_column[i-1]+1
                indel = start_column[i]+1
                delin = column[i-1]+1
                if text[index]==query[i-1]:
                    sub = sub-1
                column[i] = min(sub, indel, delin)
            if column[len(query)] <= threshold:
                results.append((index, column[len(query)]))

            start_column = column

    return results


def sellers_cutoff(text: str, query: str, threshold: int) -> List[Tuple[int, int]]:
    """
    Optimized version of `sellers` using threshold-based cutoff.

    Only computes values that can still reach a score <= threshold.
    Returns the same output as `sellers`.
    """
    results: List[Tuple[int, int]] = []

    # initialize start column
    start_column = []
    firstLEI = min(len(query),threshold)
    i=0
    while i<= firstLEI:
        start_column.append(i)
        i += 1

    last_essential_index = max(
        (i for i, value in enumerate(start_column) if value <= threshold),
        default=-1,
    )

    for index, character in enumerate(text):
        #   - compute next column
        #   - update last_essential_index
        #   - compute only necessary values

        #straight aus dem skript raus
        #index = j, i = i, m = len(query)

        column = [0]
        i = 1
        currLEI = 0

        #Zone 1: Drei Vorgänger
        while i <= last_essential_index:
            sub = start_column[i - 1] + 1
            indel = start_column[i] + 1
            delin = column[i - 1] + 1
            if text[index] == query[i-1]:
                sub = sub - 1
            column.append(min(sub, indel, delin))

            if column[i] <= threshold: currLEI = i
            i += 1
        #Zone 2: Zwei Vorgänger
        if i <= len(query):
            sub = start_column[i - 1] + 1
            delin = column[i - 1] + 1
            if text[index] == query[i-1]:
                sub = sub - 1
            column.append(min(sub, delin))
            if column[i] <= threshold: currLEI = i
            i += 1

            #Zone 3: 1 Vorgänger
            while i <= len(query) and column[i-1]+1<=threshold:
                delin = column[i - 1] + 1
                column.append(delin)
                if column[i]<=threshold: currLEI = i
                i += 1

        if currLEI==len(query) and column[len(query)]<=threshold:
            results.append((index, column[len(query)]))

        start_column = column
        last_essential_index = currLEI

    return results


def filter_to_local_minima(all_hits: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Given a list of (position, score) sorted by position,
    return only those entries whose score is smaller or
    equal to their immediate neighbors (if present).
    """
    # Done: implement local minimum filtering
    results: List[Tuple[int, int]] = []
    for i, (position, score) in enumerate(all_hits):
        if i==0 or score<=all_hits[i-1][1]: #nachbar links
            if i == len(all_hits)-1 or score <= all_hits[i+1][1]: #nachbar rechts
                results.append((position,score))

    return results
