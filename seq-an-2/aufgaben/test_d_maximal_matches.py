import unittest

from d_maximal_matches import (
    left_to_right_partition,
    partition_size,
    d_maximal_matches,
)


class TestLeftToRightPartition(unittest.TestCase):

    def test_exact_match(self):
        x = "banana"
        y = "banana"
        partition = left_to_right_partition(x, y)

        # Exact match should result in one block
        self.assertEqual(partition, ["banana"])

    def test_no_overlap(self):
        x = "abc"
        y = "xyz"
        partition = left_to_right_partition(x, y)

        # No substring longer than 1 should match
        self.assertEqual(partition,["","a","","b","","c",""])


    def test_partial_overlap(self):
        x = "banana"
        y = "ana"

        partition = left_to_right_partition(x, y)
        self.assertEqual(partition,["","b","ana","n","a"])


    def test_empty_x(self):
        x = ""
        y = "banana"

        partition = left_to_right_partition(x, y)
        self.assertEqual(partition, [""])

    def test_single_character(self):
        x = "a"
        y = "banana"

        partition = left_to_right_partition(x, y)
        self.assertEqual(partition,["a"])


class TestPartitionSize(unittest.TestCase):

    def test_partition_size(self):
        partition = ["ab", "c", "def"]
        self.assertEqual(partition_size(partition), 1)

    def test_empty_partition(self):
        self.assertEqual(partition_size(["abcdefg"]), 0)


class TestMaximalMatchesDistance(unittest.TestCase):

    def test_identical_strings(self):
        x = "banana"
        y = "banana"
        self.assertEqual(d_maximal_matches(x, y), 0)

    def test_simple_case(self):
        x = "abc"
        y = "xyz"

        # Each character must be matched separately
        self.assertEqual(d_maximal_matches(x, y), 3)

    def test_empty_string(self):
        self.assertEqual(d_maximal_matches("", "banana"), 0)


if __name__ == "__main__":
    unittest.main()
