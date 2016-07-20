"""Unit tests for the base GeneticAlgorithm class.

"""
from __future__ import absolute_import
from builtins import range


import unittest

from . import context
from . import harness

from levis.behavior import *


class FittestTriggerGAUT(FittestTriggerGA, harness.DummyBinaryGA):
    def __init__(self, config={}):
        super(FittestTriggerGAUT, self).__init__(config)
        self.bests = []

    def new_best(self, score, chromosome):
        best = (score, chromosome)
        self.bests.append(best)

class FittestTriggerGATestCase(harness.BaseGATestCase):
    def gacls(self):
        return FittestTriggerGAUT

    def test_best(self):
        ga = self.mkga()
        solution = ga.solve()
        self.assertEqual(solution, ga.best())

    def test_new_best(self):
        ga = self.mkga()
        ga.iterate()
        self.assertTrue(len(ga.bests) > 0)
        for i in range(1, len(ga.bests)):
            self.assertTrue(ga.bests[i] > ga.bests[i - 1])


class FittestInGenerationGAUT(FittestInGenerationGA, harness.DummyBinaryGA):
    pass

class ForgetsGenerationGA(FittestInGenerationGAUT):
    def generate(self):
        chromosome = self.max_iterations - self.iteration
        # Need to invoke ``fitness`` to keep score. Normally done in
        # ``ProportionateGA.post_generate`` or ``TournamentGA.select``.
        self.fitness(chromosome)
        for _ in range(0, self.population_size):
            self.next_generation.append(chromosome)


class FittestInGenerationGATestCase(harness.BaseGATestCase):
    def gacls(self):
        return FittestInGenerationGAUT

    def test_keeps_scores(self):
        ga = self.mkga()
        ga.solve()
        self.assertEqual(len(ga.best_scores), ga.iteration)

    def test_forgets_generation(self):
        ga = ForgetsGenerationGA()
        ga.solve()

        for i in range(1, len(ga.best_scores)):
            self.assertTrue(ga.best_scores[i] < ga.best_scores[i - 1])


class FinishWhenSlowGAUT(FinishWhenSlowGA, harness.DummyBinaryGA):
    pass

# TODO: validate that is_finished() returns True under the right conditions
class FinishWhenSlowGATestCase(harness.BaseGATestCase):
    def gacls(self):
        return FinishWhenSlowGAUT

    def test_finishes_when_slow(self):
        ga = self.mkga()
        ga.best_scores = [10, 13, 15, 16, 16, 16, 16, 16]
        self.assertTrue(ga.is_finished())

    def test_doesnt_finish_when_fast(self):
        ga = self.mkga()
        ga.best_scores = [10, 13, 15, 17, 18, 18, 19]
        self.assertFalse(ga.is_finished())

    def test_finishes_at_max_iterations(self):
        ga = self.mkga({"max_iterations": 10})
        ga.best_scores = [1, 5, 6, 10, 13, 15, 17, 18, 20, 22, 24]
        ga.iteration = 11
        self.assertTrue(ga.is_finished())


if __name__ == '__main__':
    unittest.main()
