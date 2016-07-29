# coding=utf-8
"""


"""

from . import mutation
from . import crossover
from . import base

class BinaryGA(base.GeneticAlgorithm):
    """A binary encoded genetic algorithm."""

    def num_bits(self):
        """Return the number of bits used by the encoding scheme.

        Returns:
            int: The number of bits used by the encoding scheme.
        """
        raise NotImplementedError

    def mutate(self, chromosome):
        """Use toggle (bit inversion) mutation on a chromosome."""
        return mutation.toggle(chromosome, self.num_bits(), self.mutation_prob)


class ValueGA(base.GeneticAlgorithm):
    """A list encoded genetic algorithm."""

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


class PermutationGA(base.GeneticAlgorithm):
    """A permutation encoded genetic algorithm."""

    def mutate(self, chromosome):
        return mutation.swap(chromosome, self.mutation_prob)
