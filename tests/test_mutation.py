"""Unit tests for mutation operations."""
from __future__ import absolute_import
#from builtins import zip
#from builtins import range

import unittest
import random

from . import context

from levis import mutation

class MutationTestCase(unittest.TestCase):

    def test_point_mutation(self):
        random.seed(12345)
        # for _ in range(0, 10):
        #     print random.random()
        #
        # 0.416619872545
        # 0.0101691694571
        # 0.825206509254
        # 0.2986398552
        # 0.368411689488
        # 0.193661349045
        # 0.566008168729
        # 0.161687823929
        # 0.124266884284
        # 0.43293626801

        orig = [1] * 10
        copy = mutation.point(orig, lambda: 0, 0.05)

        self.assertNotEqual(orig, copy)
        self.assertEqual(sum(orig), sum(copy) + 1)
        self.assertEqual(len(orig), len(copy))

    def test_heterogeneous_length_mutation(self):
        random.seed(1000)
        # for _ in range(0, 10):
        #     print random.random()
        #
        # 0.777356642701
        # 0.669825559559
        # 0.0991396039248 *
        # 0.35297051119 *
        # 0.467907742901
        # 0.534683741471
        # 0.978309060912
        # 0.130315350159 *
        # 0.67124346823
        # 0.364229415947 *
        # 0.488835707162
        # 0.203012210734 *

        orig = [1] * 10
        copy = mutation.heterogeneous_length(orig, lambda: 0, 0.4)

        self.assertNotEqual(orig, copy)
        self.assertEqual(5, sum(copy))

    def test_toggle_mutation(self):
        random.seed(12345)
        # for _ in range(0, 10):
        #     print random.random()
        #
        # 0.416619872545
        # 0.0101691694571
        # 0.825206509254
        # 0.2986398552
        # 0.368411689488
        # 0.193661349045
        # 0.566008168729
        # 0.161687823929
        # 0.124266884284
        # 0.43293626801

        orig = 1023
        copy = mutation.toggle(orig, 10, 0.05)

        self.assertNotEqual(orig, copy)

        # This is faster than bit twiddling...
        # http://stackoverflow.com/questions/9829578/fast-way-of-counting-non-zero-bits-in-python
        self.assertEqual(bin(copy).count("1"), 9)

    def test_swap_mutation(self):
        random.seed(12345)

        orig = [i for i in range(10, 21)]
        copy = mutation.swap(orig, 0.05)

        swapped = [1 for t in zip(orig, copy) if t[0] != t[1]]

        self.assertNotEqual(orig, copy)
        self.assertEqual(len(orig), len(copy))
        self.assertEqual(sum(orig), sum(copy))
        self.assertEqual(len(swapped), 2)


if __name__ == '__main__':
    unittest.main()
