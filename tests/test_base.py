"""Unit tests for the base GeneticAlgorithm class.

"""
from __future__ import absolute_import


import unittest

from . import harness
#import harness


class GeneticAlgorithmTestCase(harness.BaseGATestCase):

    def mkga(self, config={}):
        return harness.DummyBinaryGA(config)

    def gacls(self):
        return harness.DummyBinaryGA

    def test_finished(self):
        ga = self.mkga({"max_iterations": 10})
        self.assertFalse(ga.is_finished())

        ga.iteration = 10
        self.assertTrue(ga.is_finished())

        ga.iteration = 11
        self.assertTrue(ga.is_finished())

    def test_solve(self):
        ga = self.mkga({"iterations": 3, "population_size": 4})
        solution = ga.solve()
        self.assertIsInstance(solution, int)
        self.assertEqual(ga.iteration, ga.max_iterations)


if __name__ == '__main__':
    print("pkg", __package__)
    if __package__ is None:
        __package__ = "tests.test_base"
        print("setting package")
    print("pkg2", __package__)
    unittest.main()
