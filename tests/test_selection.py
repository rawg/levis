"""Unit tests for the base GeneticAlgorithm class.

"""
from __future__ import absolute_import


import unittest

from . import context
from . import harness

from levis.selection import *


class ProportionateGAUT(ProportionateGA, harness.DummyBinaryGA):
    pass


class ScalingProportionateGAUT(ScalingProportionateGA, harness.DummyBinaryGA):
    pass


class TournamentGAUT(TournamentGA, harness.DummyBinaryGA):
    pass


class ProportionateGATestCase(harness.BaseGATestCase):
    def gacls(self):
        return ProportionateGAUT


class TournamentGATestCase(harness.BaseGATestCase):
    def gacls(self):
        return TournamentGAUT


class ScalingProportionateGATestCase(harness.BaseGATestCase):
    def gacls(self):
        return ScalingProportionateGAUT


class ElitistGAUT(ElitistGA, harness.DummyBinaryGA):
    pass

class ElitistGATestCase(harness.BaseGATestCase):
    def gacls(self):
        return ElitistGAUT

    def test_init(self):
        ga = self.mkga({"population_size": 10, "elitism_pct": .5})
        self.assertEqual(ga.num_elites, 5)

    def test_insert(self):
        ga = self.mkga({"population_size": 10, "elitism_pct": .4})
        ga.fitness(50)
        self.assertEqual(ga.elites[0][1], 50)

        ga.fitness(100)
        self.assertEqual(ga.elites[0][1], 100)
        self.assertEqual(ga.elites[1][1], 50)

        ga.fitness(75)
        self.assertEqual(ga.elites[0][1], 100)
        self.assertEqual(ga.elites[1][1], 75)
        self.assertEqual(ga.elites[2][1], 50)

        ga.fitness(60)
        ga.fitness(80)
        self.assertEqual(len(ga.elites), 4)
        self.assertEqual(ga.elites[3][1], 60)



if __name__ == '__main__':
    unittest.main()
