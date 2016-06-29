"""Unit tests for mutation operations."""

import unittest
import random

import context

from levis import crossover

class CrossoverTestCase(unittest.TestCase):

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

    def test_single_point_bin_crossover(self):
        p1 = 992
        p2 = 31
        ch = crossover.single_point_bin(p1, p2, 5)

        self.assertNotEqual(ch, p1)
        self.assertNotEqual(ch, p2)
        self.assertEqual(ch, 1023)

    def test_pmx(self):
        p1 = [random.randint(0, 999) for _ in range(0, 10)]
        p2 = list(p1)
        random.shuffle(p2)

        ch = crossover.partially_matched(p1, p2)
        self.assertEqual(len(ch), 10)

        unique = sorted(list(set(ch)))
        p2.sort()
        p1.sort()

        self.assertEqual(unique, p2)
        self.assertEqual(unique, p1)




if __name__ == '__main__':
    unittest.main()
