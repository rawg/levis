"""Unit tests for mutation operations."""
from __future__ import absolute_import
#from builtins import zip
#from builtins import range

import random
import unittest

from . import context
from .harness import permutated_set

from levis import crossover

class CrossoverTestCase(unittest.TestCase):

    def setUp(self):
        self.longMessage = True

    def validate_ancestry(self, child, p1, p2):
        for i, allele in enumerate(child):
            msg = "i: %i; child: %s; p1: %s; p2: %s" % (i, child[i], p1[i], p2[i])
            self.assertTrue(child[i] == p1[i] or child[i] == p2[i], msg)

    def test_single_point_crossover(self):
        p1 = [1] * 10
        p2 = [2] * 10
        ch = crossover.single_point(p1, p2, 5)

        self.assertEqual(len(ch), len(p2))
        self.assertNotEqual(ch, p1)
        self.assertNotEqual(ch, p2)

        for i in range(0, 5):
            self.assertTrue(ch[i] == p1[i], "Locus %i mismatched" % i)

        for i in range(5, 10):
            self.assertTrue(ch[i] == p2[i], "Locus %i mismatched" % i)

    def test_random_point_crossover(self):
        p1 = [1] * 10
        p2 = [2] * 10
        ch = crossover.single_point(p1, p2)

        self.assertEqual(len(ch), len(p2))
        self.assertNotEqual(ch, p1)
        self.assertNotEqual(ch, p2)

        switched = False
        parent = p1
        for i, a in enumerate(ch):
            if parent[i] != a:
                if not switched:
                    parent = p2
                else:
                    self.fail("Locus %i mismatched" % i)

            self.assertEqual(parent[i], a)

    def test_random_points_crossover(self):
        p1 = [1] * 10
        p2 = [2] * 10
        ch = crossover.multiple_points(p1, p2, points=2)

        self.assertEqual(len(ch), len(p2))
        self.assertNotEqual(ch, p1)
        self.assertNotEqual(ch, p2)
        self.validate_ancestry(ch, p1, p2)

    def test_multiple_points_crossover(self):
        p1 = [1] * 10
        p2 = [2] * 10
        ch = crossover.multiple_points(p1, p2, loci=[3, 7])

        self.assertEqual(len(ch), len(p2))
        self.assertNotEqual(ch, p1)
        self.assertNotEqual(ch, p2)
        self.validate_ancestry(ch, p1, p2)

    def test_uniform(self):
        p1 = [1] * 10
        p2 = [2] * 10
        ch = crossover.uniform(p1, p2)
        for allele in ch:
            self.assertTrue(allele == 1 or allele == 2)

    def test_uniform_bin(self):
        p1 = 992
        p2 = 31
        ch = crossover.uniform_bin(p1, p2, 10)

        b1 = bin(p1)[2:].zfill(10)
        b2 = bin(p2)[2:].zfill(10)
        bc = bin(ch)[2:].zfill(10)

        for c, m, f in zip(bc, b1, b2):
            self.assertTrue(c == m or c == f)

    def test_single_point_bin_crossover(self):
        p1 = 992
        p2 = 31
        ch = crossover.single_point_bin(p1, p2, 10, 5)

        self.assertNotEqual(ch, p1)
        self.assertNotEqual(ch, p2)
        self.assertEqual(ch, 1023)

    def test_single_point_bin_crossover_by_locus(self):
        p1 = 992
        p2 = 31
        ch = crossover.single_point_bin(p1, p2, locus=5)

        self.assertNotEqual(ch, p1)
        self.assertNotEqual(ch, p2)
        self.assertEqual(ch, 1023)

    def test_single_point_bin_crossover_by_length(self):
        p1 = 992
        p2 = 31
        ch = crossover.single_point_bin(p1, p2, length=10)

        self.assertNotEqual(ch, p1)
        self.assertNotEqual(ch, p2)

        b1 = bin(p1)[2:].zfill(10)
        b2 = bin(p2)[2:].zfill(10)
        bc = bin(ch)[2:].zfill(10)

        for c, m, f in zip(bc, b1, b2):
            self.assertTrue(c == m or c == f, "%s, %s, %s" % (c, m, f))

    def validate_ordered(self, ch, p1, p2):
        msg = "p1: %s, p2: %s, ch: %s" % (p1, p2, ch)
        self.assertEqual(len(ch), 10, msg)

        unique = sorted(list(set(ch)))
        p2.sort()
        p1.sort()

        self.assertEqual(unique, p2, msg)
        self.assertEqual(unique, p1, msg)

    def test_pmx(self):
        p1, p2 = permutated_set()
        ch = crossover.partially_matched(p1, p2)
        self.validate_ordered(ch, p1, p2)

    def test_ordered(self):
        p1, p2 = permutated_set()
        ch = crossover.ordered(p1, p2)
        self.validate_ordered(ch, p1, p2)

    def test_ero(self):
        p1, p2 = permutated_set()
        ch = crossover.edge_recombination(p1, p2)
        self.validate_ordered(ch, p1, p2)


if __name__ == '__main__':
    unittest.main()
