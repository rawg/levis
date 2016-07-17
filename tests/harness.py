"""Test implementations and base test cases.

"""
from __future__ import absolute_import
from builtins import zip
from builtins import str

import argparse
import random
import unittest

#from . import context

from levis import GeneticAlgorithm

def unique_ints(amt=10, low=0, high=999):
    found = []
    while len(found) < amt:
        i = random.randint(low, high)
        if i not in found:
            found.append(i)
    return found

def permutated_set(amt=10):
    p1 = unique_ints(amt)
    p2 = list(p1)
    random.shuffle(p2)
    return (p1, p2)


class GAUT(GeneticAlgorithm):
    def iterate(self):
        if self.population is None:
            self.seed()

        self.iteration += 1
        self.pre_generate()
        self.generate()
        self.post_generate()


class DummyBinaryGA(GAUT):
    def __init__(self, config={}):
        super(DummyBinaryGA, self).__init__(config)
        self.chromosome_length = 8

    def create(self):
        return random.randint(0, 255)

    def score(self, chromosome):
        return chromosome * 2

    def select(self):
        chromosome = random.choice(self.population)

        # Need to invoke ``fitness()`` from time to time to mimic
        # tournament/proportionate selection and test behaviors.
        self.fitness(chromosome)

        return chromosome

    def crossover(self):
        p1 = self.select()
        p2 = self.select()
        return (p1 & 240) + (p2 & 15)

    def mutate(self, chromosome):
        bit = 2 ** random.randint(0, 7)
        if random.randint(0, 1) == 1:
            return chromosome | bit
        else:
            return chromosome | (~bit & 255)

    def chromosome_str(self, chromosome):
        return bin(chromosome) + ":" + str(self.score(chromosome))

    def chromosome_repr(self, chromosome):
        return bin(chromosome)


class ObservableGA(GeneticAlgorithm):
    def __init__(self, config={}):
        super(ObservableGA, self).__init__(config)
        self.observers = {}

    def register(self, event, callback):
        self.observers.setdefault(event, [])
        self.observers[event].append(callback)

    def __trigger(self, event):
        if event in self.observers:
            for cb in self.observers[event]:
                cb()

    def pre_generate(self):
        self.__trigger("pre_generate")
        super(ObservableGA, self).pre_generate()

    def post_generate(self):
        super(ObservableGA, self).post_generate()
        self.__trigger("post_generate")


def observable(cls):
    class Watched(ObservableGA, cls):
        def __init__(self, config={}):
            super(Watched, self).__init__(config)

    return Watched


class BaseGATestCase(unittest.TestCase):

    def gacls(self):
        raise NotImplementedError

    def mkga(self, config={}):
        cls = self.gacls()
        return cls(config)

    def mkobservable(self, config={}):
        cls = observable(self.gacls())
        return cls(config)

    def test_parser(self):
        parser = self.gacls().arg_parser()
        self.assertIsInstance(parser, argparse.ArgumentParser)
        self.assertFalse(parser.add_help)

    def test_basic_config(self):
        conf = {
            "population_size": 7,
            "mutation_prob": 0.13,
            "crossover_prob": 0.87,
            "max_iterations": 42
        }

        ga = self.mkga(conf)
        self.assertEqual(ga.population_size, conf["population_size"])
        self.assertEqual(ga.mutation_prob, conf["mutation_prob"])
        self.assertEqual(ga.crossover_prob, conf["crossover_prob"])
        self.assertEqual(ga.max_iterations, conf["max_iterations"])

        ga = self.mkga()
        self.assertIsInstance(ga.population_size, int)
        self.assertTrue(ga.population_size > 0)

        self.assertIsInstance(ga.max_iterations, int)
        self.assertTrue(ga.max_iterations > 0)

        self.assertIsInstance(ga.crossover_prob, float)
        self.assertTrue(ga.crossover_prob > 0)
        self.assertTrue(ga.crossover_prob < 1)

        self.assertIsInstance(ga.mutation_prob, float)
        self.assertTrue(ga.mutation_prob > 0)
        self.assertTrue(ga.mutation_prob < 1)

    def test_seed(self):
        ga = self.mkga({"population_size": 10})
        self.assertEqual(ga.population, None)
        ga.seed()
        self.assertEqual(len(ga.population), 10)

    def test_score_population(self):
        ga = self.mkga()
        ga.iterate()

        scores = ga.score_population()
        self.assertEqual(ga.population_size, len(scores))

        prev = None
        for scored in scores:
            score = scored[1]
            chromosome = scored[0]

            if prev is not None:
                self.assertTrue(prev >= score)
            prev = score

            self.assertIn(chromosome, ga.population)

    def test_chromosome_str(self):
        ga = self.mkga()
        ga.iterate()
        ch = ga.select()
        st = ga.chromosome_str(ch)
        try:
            self.assertTrue(isinstance(st, basestring))
        except NameError:
            self.assertTrue(isinstance(st, str))


    def test_chromosome_repr(self):
        ga = self.mkga()
        ga.iterate()
        ch = ga.select()
        st = ga.chromosome_repr(ch)
        try:
            self.assertTrue(isinstance(st, basestring))
        except NameError:
            self.assertTrue(isinstance(st, str))

    def test_generate_hooks(self):
        counter = [0]
        pre = []
        post = []

        def pre_hook():
            counter[0] += 1
            pre.append(counter[0])

        def post_hook():
            counter[0] += 1
            post.append(counter[0])

        ga = self.mkobservable({"max_iterations": 3, "population_size": 10})
        ga.register("pre_generate", pre_hook)
        ga.register("post_generate", post_hook)

        ga.iterate()

        self.assertEqual(len(pre), ga.iteration)
        self.assertEqual(len(post), ga.iteration)

        for before, after in zip(pre, post):
            self.assertTrue(before < after)
            self.assertEqual(after, before + 1)

    def test_progress(self):
        ga = self.mkobservable({"max_iterations": 2})
        watched = [[], 0]

        def pre_hook():
            watched[0] = ga.population
            watched[1] += 1
            self.assertEqual(ga.iteration, watched[1])

        def post_hook():
            self.assertNotEqual(watched[0], ga.population)
            self.assertEqual(len(ga.population), ga.population_size)

        ga.register("pre_generate", pre_hook)
        ga.register("post_generate", post_hook)

        # might need to be ga.iterate()...
        ga.solve()

    def test_fitness(self):
        ga = self.mkga()
        ga.iterate()
        chromosome = ga.select()
        self.assertEqual(ga.fitness(chromosome), ga.score(chromosome))
