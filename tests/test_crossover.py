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

        for child in ch:
            self.assertEqual(len(child), len(p2))
            self.assertNotEqual(child, p1)
            self.assertNotEqual(child, p2)

        for i in range(0, 5):
            self.assertTrue(ch[0][i] == p1[i], "Locus %i mismatched" % i)
            self.assertTrue(ch[1][i] == p2[i], "Locus %i mismatched" % i)

        for i in range(5, 10):
            self.assertTrue(ch[0][i] == p2[i], "Locus %i mismatched" % i)
            self.assertTrue(ch[1][i] == p1[i], "Locus %i mismatched" % i)

    def test_cut_and_splice(self):
        p1 = [1] * 10
        p2 = [2] * 5
        ch = crossover.cut_and_splice(p1, p2, [5, 1])

        for child in ch:
            #self.assertEqual(len(child), len(p2))
            self.assertNotEqual(child, p1)
            self.assertNotEqual(child, p2)
        # more to do here!

    def test_random_point_crossover(self):
        p1 = [1] * 10
        p2 = [2] * 10
        ch = crossover.single_point(p1, p2)

        for child in ch:
            self.assertEqual(len(child), len(p2))
            self.assertNotEqual(child, p1)
            self.assertNotEqual(child, p2)

        def check(child, parent1, parent2):
            switched = False
            parent = parent1
            for i, a in enumerate(child):
                if parent[i] != a:
                    if not switched:
                        parent = parent2
                    else:
                        self.fail("Locus %i mismatched" % i)

                self.assertEqual(parent[i], a)

        check(ch[0], p1, p2)

    def test_random_points_crossover(self):
        p1 = [1] * 10
        p2 = [2] * 10
        children = crossover.multiple_points(p1, p2, points=2)

        for ch in children:
            self.assertEqual(len(ch), len(p2))
            self.assertNotEqual(ch, p1)
            self.assertNotEqual(ch, p2)
            self.validate_ancestry(ch, p1, p2)

    def test_multiple_points_crossover(self):
        p1 = [1] * 10
        p2 = [2] * 10
        children = crossover.multiple_points(p1, p2, loci=[3, 7])

        for ch in children:
            self.assertEqual(len(ch), len(p2))
            self.assertNotEqual(ch, p1)
            self.assertNotEqual(ch, p2)
            self.validate_ancestry(ch, p1, p2)

    def test_uniform(self):
        p1 = [1] * 10
        p2 = [2] * 10
        children = crossover.uniform(p1, p2)

        for ch in children:
            self.assertEqual(len(p1), len(ch))
            for allele in ch:
                self.assertTrue(allele == 1 or allele == 2)

    def test_uniform_bin(self):
        parent1 = 992
        parent2 = 31
        children = crossover.uniform_bin(parent1, parent2, 10)

        def check(ch, p1, p2):
            b1 = bin(p1)[2:].zfill(10)
            b2 = bin(p2)[2:].zfill(10)
            bc = bin(ch)[2:].zfill(10)

            for c, m, f in zip(bc, b1, b2):
                self.assertTrue(c == m or c == f)

        for ch in children:
            check(ch, parent1, parent2)

    def test_single_point_bin_crossover(self):
        p1 = 992
        p2 = 31
        children = crossover.single_point_bin(p1, p2, 10, 5)

        for ch in children:
            self.assertNotEqual(ch, p1)
            self.assertNotEqual(ch, p2)

        self.assertEqual(children[0], 1023)
        self.assertEqual(children[1], 0)

    def test_single_point_bin_crossover_by_locus(self):
        p1 = 992
        p2 = 31
        children = crossover.single_point_bin(p1, p2, locus=5)

        for ch in children:
            self.assertNotEqual(ch, p1)
            self.assertNotEqual(ch, p2)

        self.assertEqual(children[0], 1023)
        self.assertEqual(children[1], 0)

    def test_single_point_bin_crossover_by_length(self):
        parent1 = 992
        parent2 = 31
        children = crossover.single_point_bin(parent1, parent2, length=10)

        def check(ch, p1, p2):
            self.assertNotEqual(ch, p1)
            self.assertNotEqual(ch, p2)

            b1 = bin(p1)[2:].zfill(10)
            b2 = bin(p2)[2:].zfill(10)
            bc = bin(ch)[2:].zfill(10)

            for c, m, f in zip(bc, b1, b2):
                self.assertTrue(c == m or c == f, "%s, %s, %s" % (c, m, f))

        for ch in children:
            check(ch, parent1, parent2)

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
        children = crossover.partially_matched(p1, p2)
        for ch in children:
            self.validate_ordered(ch, p1, p2)

    def test_ordered(self):
        p1, p2 = permutated_set()
        children = crossover.ordered(p1, p2)
        for ch in children:
            self.validate_ordered(ch, p1, p2)

    def test_ero(self):
        p1, p2 = permutated_set()
        ch = crossover.edge_recombination(p1, p2)[0]
        self.validate_ordered(ch, p1, p2)


if __name__ == '__main__':
    unittest.main()
