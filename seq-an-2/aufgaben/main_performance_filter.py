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
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    xs = []
    ys = []
    for a,b in RANDOM_PAIRS:
        start=time.time()
        d_edit(a,b)
        end=time.time()
        xs.append(len(a))
        ys.append(end-start)
    ax1.plot(xs, ys, label="Edit Distance", marker='o')

    # DONE: Plot the runtimes for the other distances and for adversarial inputs
    # Q-gram Distance (Random)
    xs_qgram = []
    ys_qgram = []
    for a, b in RANDOM_PAIRS:
        start = time.time()
        d_q_gram(a, b, q=7)
        end = time.time()
        xs_qgram.append(len(a))
        ys_qgram.append(end - start)
    ax1.plot(xs_qgram, ys_qgram, label="Q-gram Distance", marker='s')

    # Maximal Matches Distance (Random)
    xs_maximal = []
    ys_maximal = []
    for a, b in RANDOM_PAIRS:
        start = time.time()
        d_maximal_matches(a, b)
        end = time.time()
        xs_maximal.append(len(a))
        ys_maximal.append(end - start)
    ax1.plot(xs_maximal, ys_maximal, label="Maximal Matches", marker='^')

    ax1.set_xlabel("String length")
    ax1.set_ylabel("Runtime [s]")
    ax1.set_title("Random String Pairs")
    ax1.legend()
    ax1.grid(True)

    # Edit Distance (Adversarial)
    xs_edit_adv = []
    ys_edit_adv = []
    for a, b in ADVERSARIAL_PAIRS:
        start = time.time()
        d_edit(a, b)
        end = time.time()
        xs_edit_adv.append(len(a))
        ys_edit_adv.append(end - start)
    ax2.plot(xs_edit_adv, ys_edit_adv, label="Edit Distance", marker='o')

    # Q-gram Distance (Adversarial)
    xs_qgram_adv = []
    ys_qgram_adv = []
    for a, b in ADVERSARIAL_PAIRS:
        start = time.time()
        d_q_gram(a, b, q=7)
        end = time.time()
        xs_qgram_adv.append(len(a))
        ys_qgram_adv.append(end - start)
    ax2.plot(xs_qgram_adv, ys_qgram_adv, label="Q-gram Distance", marker='s')

    # Maximal Matches Distance (Adversarial)
    xs_maximal_adv = []
    ys_maximal_adv = []
    for a, b in ADVERSARIAL_PAIRS:
        start = time.time()
        d_maximal_matches(a, b)
        end = time.time()
        xs_maximal_adv.append(len(a))
        ys_maximal_adv.append(end - start)
    ax2.plot(xs_maximal_adv, ys_maximal_adv, label="Maximal Matches", marker='^')

    ax2.set_xlabel("String length")
    ax2.set_ylabel("Runtime [s]")
    ax2.set_title("Adversarial String Pairs (Identical Homogeneous)")
    ax2.legend()
    ax2.grid(True)


    plt.tight_layout()
    plt.show()
