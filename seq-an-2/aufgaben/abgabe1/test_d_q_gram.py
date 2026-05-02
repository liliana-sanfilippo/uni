import unittest

from d_q_gram import (
    get_code,
    get_rank,
    update_rank,
    get_profile,
    d_q_gram,
)


class TestQGram(unittest.TestCase):
    """Ranking-order agnostic sanity tests for q-gram implementation."""


    # --------------------------------------------------
    # get_rank properties (ranking-order independent)
    # --------------------------------------------------

    def test_equal_qgrams_have_equal_rank(self) -> None:
        self.assertEqual(get_rank("ACG", 3), get_rank("ACG", 3))

    def test_different_qgrams_have_different_rank(self) -> None:
        self.assertNotEqual(get_rank("AAA", 3), get_rank("AAC", 3))

    # --------------------------------------------------
    # update_rank consistency
    # --------------------------------------------------

    def test_update_rank_matches_get_rank(self) -> None:
        q = 3
        s1 = "ACG"
        s2 = "CGT"  # sliding window result

        r1 = get_rank(s1, q)
        r2 = update_rank(r1, s1[0], s2[-1], q)

        self.assertEqual(r2, get_rank(s2, q))

    # --------------------------------------------------
    # get_profile
    # --------------------------------------------------

    def test_profile_total_count(self) -> None:
        s = "TACATATATTATTATTAG"
        q = 3

        profile = get_profile(s, q)

        # Number of q-grams should be len(s) - q + 1
        expected = len(s) - q + 1
        self.assertEqual(sum(profile), expected)

    def test_profile_short_string(self) -> None:
        profile = get_profile("A", 3)
        self.assertEqual(sum(profile), 0)

    def test_profile_consistency(self) -> None:
        s = "ACGTAC"
        q = 3

        profile = get_profile(s, q)

        # For every q-gram in the string, its rank index
        # must have positive count
        for i in range(len(s) - q + 1):
            qgram = s[i:i + q]
            rank = get_rank(qgram, q)
            self.assertGreater(profile[rank], 0)

    # --------------------------------------------------
    # d_q_gram properties
    # --------------------------------------------------

    def test_distance_identity(self) -> None:
        self.assertEqual(d_q_gram("ACGT", "ACGT", 1), 0)
        self.assertEqual(d_q_gram("ACGT", "ACGT", 2), 0)
        self.assertEqual(d_q_gram("ACGT", "ACGT", 3), 0)
        self.assertEqual(d_q_gram("ACGT", "ACGT", 4), 0)

    def test_distance_symmetry(self) -> None:
        a = "ACGTAC"
        b = "ACGGAC"
        self.assertEqual(d_q_gram(a, b, q=2), 4)
        self.assertEqual(d_q_gram(b, a, q=2), 4)
        self.assertEqual(d_q_gram(a, b, q=3), 6)
        self.assertEqual(d_q_gram(b, a, q=3), 6)

    def test_distance_repeat(self) -> None:
        d = d_q_gram("AAAA", "TTTT", 2)
        self.assertEqual(d,6)


if __name__ == "__main__":
    unittest.main()
