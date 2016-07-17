"""Unit tests for mutation operations."""
from __future__ import absolute_import
from builtins import zip
from builtins import range

import unittest

from . import context

from levis import mutation

class MutationTestCase(unittest.TestCase):

    def test_point_mutation(self):
        orig = [1] * 10
        copy = mutation.point(orig, 0)

        self.assertNotEqual(orig, copy)
        self.assertEqual(sum(orig), sum(copy) + 1)
        self.assertEqual(len(orig), len(copy))

    def test_toggle_mutation(self):
        orig = 1023
        copy = mutation.toggle(orig, 10)

        self.assertNotEqual(orig, copy)

        # This is faster than bit twiddling...
        # http://stackoverflow.com/questions/9829578/fast-way-of-counting-non-zero-bits-in-python
        self.assertEqual(bin(copy).count("1"), 9)

    def test_swap_mutation(self):
        # [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20] == [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
        orig = [i for i in range(10, 21)]
        copy = mutation.swap(orig)

        swapped = [1 for t in zip(orig, copy) if t[0] != t[1]]

        self.assertNotEqual(orig, copy)
        self.assertEqual(len(orig), len(copy))
        self.assertEqual(sum(orig), sum(copy))
        self.assertEqual(len(swapped), 2)


if __name__ == '__main__':
    unittest.main()
