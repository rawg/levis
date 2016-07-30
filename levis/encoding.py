# coding=utf-8
"""Traits for various encoding schemes.

Contents
--------
:BinaryGA:

"""

from . import mutation
from . import base
from .crossover import *


class EncodingScheme(base.GeneticAlgorithm):

    @classmethod
    def arg_parser(cls):
        parser = super(ConfigurableCrossoverGA, cls).arg_parser()
        parser.add_argument("--crossover-operator", "-cx",
                            help="Crossover operator")
        return parser

    def crossover(self):
        parent1 = self.select()
        parent2 = self.select()
        self.crossover_operator(parent1, parent2)



class BinaryGA(EncodingScheme):
    """A binary encoded genetic algorithm."""

    def __init__(self, config={}):
        super(BinaryGA, self).__init__(config)

        operator = self.config.setdefault("crossover_operator", "single_point")

        if operator not in ["single_point", "uniform"]:
            raise ValueError("Crossover operator must be `single_point` or "
                             "`uniform`.")

        self.num_cx_children = 2

        if operator is "uniform":
            op = lambda p1, p2: uniform_bin(p1, p2, self.num_bits())
        else:
            op = lambda p1, p2: single_point_bin(p1, p2, self.num_bits())

        self.crossover_operator = op

    def num_bits(self):
        """Return the number of bits used by the encoding scheme.

        Returns:
            int: The number of bits used by the encoding scheme.
        """
        raise NotImplementedError

    def mutate(self, chromosome):
        """Use toggle (bit inversion) mutation on a chromosome."""
        return mutation.toggle(chromosome, self.num_bits(), self.mutation_prob)


class ValueGA(EncodingScheme):
    """A list encoded genetic algorithm."""

    def __init__(self, config={}):
        super(ValueGA, self).__init__(config)

        operator = self.config.setdefault("crossover_operator", "single_point")

        if operator not in ["single_point", "uniform", "multiple_point"]:
            raise ValueError("Crossover operator must be `single_point`, "
                             "`multiple_points`, or `uniform`.")

        self.num_cx_children = 2

        if operator is "uniform":
            op = lambda p1, p2: uniform(p1, p2)
        elif operator is "multiple_points":
            op = lambda p1, p2: multiple_points(p1, p2)
        else:
            op = lambda p1, p2: single_point(p1, p2)

        self.crossover_operator = op

    def get_value(self):
        """Retrieve a valid allele value at random."""
        raise NotImplementedError

    def mutate(self, chromosome):
        return mutation.point(chromosome, self.get_value, self.mutation_prob)


class ListGA(ValueGA):
    """A list encoded genetic algorithm."""

    def mutate(self, chromosome):
        return mutation.heterogeneous_length(chromosome, self.get_value,
                                             self.mutation_prob)


class PermutationGA(EncodingScheme):
    """A permutation encoded genetic algorithm."""

    def __init__(self, config={}):
        super(ValueGA, self).__init__(config)

        operator = self.config.setdefault("crossover_operator", "single_point")

        operators = ["ordered", "partially_matched", "edge_recombination",
                     "ox", "pmx", "ero"]
        if operator not in operators:
            raise ValueError("Crossover operator must be `ordered`, "
                             "`partially_matched`, or `edge_recombination`.")

        if operator is "ordered":
            op = lambda p1, p2: ordered(p1, p2)
            self.num_cx_children = 2
        elif operator is "partially_matched":
            op = lambda p1, p2: partially_matched(p1, p2)
            self.num_cx_children = 2
        else:
            op = lambda p1, p2: edge_recombination(p1, p2)
            self.num_cx_children = 1

        self.crossover_operator = op

    def mutate(self, chromosome):
        return mutation.swap(chromosome, self.mutation_prob)
