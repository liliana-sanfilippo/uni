"""
Performance comparison of different string distance algorithms.

You will measure and compare the runtime behaviour of:

- d_edit
- d_maximal_matches
- d_q_gram

on randomly generated and adversarial DNA string pairs.
"""

import random
import time
from typing import List, Tuple

import matplotlib.pyplot as plt

from d_edit import d_edit
from d_maximal_matches import d_maximal_matches
from d_q_gram import d_q_gram
import sys
sys.setrecursionlimit(1500)

# ---------------------------------------------------------------------
# Data generation
# ---------------------------------------------------------------------

ALPHABET = "ACGT"
STRING_LENGTHS: List[int] = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]


def random_string(length: int) -> str:
    """
    Generate a random DNA string of given length.
    """
    return "".join(random.choice(ALPHABET) for _ in range(length))


def generate_random_pairs(lengths: List[int]) -> List[Tuple[str, str]]:
    """
    Generate pairs of independent random DNA strings.
    """
    return [(random_string(l), random_string(l)) for l in lengths]


def generate_adversarial_pairs(lengths: List[int]) -> List[Tuple[str, str]]:
    """
    Generate adversarial pairs (identical homogeneous strings).
    """
    return [("A" * l, "A" * l) for l in lengths]


RANDOM_PAIRS = generate_random_pairs(STRING_LENGTHS)
ADVERSARIAL_PAIRS = generate_adversarial_pairs(STRING_LENGTHS)


# ---------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------

if __name__ == "__main__":
    xs = []
    ys = []
    for a,b in RANDOM_PAIRS:
        start=time.time()
        d_edit(a,b)
        end=time.time()
        xs.append(len(a))
        ys.append(end-start)
    plt.plot(xs,ys,label="Edit Distance")
    #TODO: Plot the runtimes for the other distances and for adversarial inputs
    plt.xlabel("String length")
    plt.ylabel("Runtime[s]")
    plt.legend()
    plt.show()
