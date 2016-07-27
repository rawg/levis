"""Functions for crossover operations.

Contents
--------

This module provides the following classes:

:ConfigurableCrossoverGA:
    A class that accepts a configuration parameter,
    ``crossover_operator``/``--crossover-operator`` to change the crossover
    operator at runtime. Useful for comparing performance.

In addition, crossover operations are implemented as functions. The available
operations and their suitability for encoding types is listed below.

==================  ======  ====  ===========
Operation           Binary  List  Permutation
==================  ======  ====  ===========
single_point        No      Yes   No
single_point_bin    Yes     No    No
multiple_points     No      Yes   No
uniform             No      Yes   No
uniform_bin         Yes     No    No
ordered             No      No    Yes
partially_matched   No      No    Yes
edge_recombination  No      No    Yes
==================  ======  ====  ===========
"""
from __future__ import division
from __future__ import absolute_import
#from builtins import range


import random
import re

from . import ero
from . import base


def single_point(parent1, parent2, locus=None):
    """Return a new chromosome created with single-point crossover.

    This is suitable for use with list or value encoding.

    Args:
        parent1 (List): A parent chromosome.
        parent2 (List): A parent chromosome.
        locus (int): The locus at which to crossover or ``None`` for a randomly
            selected locus.

    Returns:
        Tuple[List]: A new chromosome descended from the given parents.
    """
    if len(parent1) > len(parent2):
        parent1, parent2 = parent2, parent1

    if locus is None:
        locus = int(random.triangular(1, len(parent1) / 2, len(parent1) - 2))

    return (parent1[0:locus] + parent2[locus:])


def single_point_bin(parent1, parent2, length=None, locus=None):
    """Return a new chromosome through a single-point crossover.

    This is suitable for use with binary encoding.

    Args:
        parent1 (List): A parent chromosome.
        parent2 (List): A parent chromosome.
        locus (int): The crossover point or ``None`` to choose one at random.
            If ``None``, then ``length`` must be the number of bits used in the
            parent chromosomes.
        length(int): The number of bits used. Not used if a locus is provided.

    Returns:
        Tuple[int]: A new chromosome descended from the given parents.

    Raises:
        ValueError: if neither ``locus`` or ``length`` is specified.
    """

    if locus is None and length is None:
        raise ValueError("Either the length or a locus is required.")

    if locus is None:
        locus = int(random.triangular(1, length / 2, length - 2))

    if length is None:
        length = 2 * locus

    maskr = 2 ** locus - 1
    maskl = (2 ** length - 1) & ~maskr

    return (parent1 & maskl | parent2 & maskr)


def multiple_points(parent1, parent2, loci=None, points=2):
    """Return a new chromosome using crossover at multiple points.

    This is suitable for value and list encoded GAs.

    `loci` should be an iterable list of loci at which to cutover, or `None` to
    select points at random. If `loci` is `None`, then `points` should be the
    number of random points to select.

    When choosing random points, the chromosomes are divided into `points`
    sections, and a crossover point is selected at random from within that
    section.

    Args:
        parent1 (List): A parent chromosome.
        parent2 (List): A parent chromosome.
        loci (List[int]): The crossover point or ``None`` to choose at random.
        points (int): The number of points.

    Returns:
        Tuple[List]: A new chromosome descended from the given parents.

    Raises:
        ValueError: if too many points are requested for the chromosome length.
    """
    child = []
    prev = 0

    if loci is None:
        if 3 * points > len(parent1):
            raise ValueError("Too many points for chromosome length")

        loci = []
        for i in range(0, points):
            floor = int(i / points * len(parent1)) + 1
            ceil = int((i + 1) / points * len(parent1)) + 1
            point = random.randint(floor, ceil)

            loci.append(point)

    for locus in loci:
        child = child + parent1[prev:locus]
        prev = locus
        parent2, parent1 = parent1, parent2

    child = child + parent1[prev:len(parent1)]

    return (child)


def uniform(parent1, parent2):
    """Return a new chromosome using uniform crossover.

    This is suitable for value encoded GAs.

    Args:
        parent1 (List): A parent chromosome.
        parent2 (List): A parent chromosome.

    Returns:
        Tuple[List]: A new chromosome descended from the given parents.
    """
    chromosome = []
    for locus in range(0, len(parent1)):
        if random.randint(0, 1) == 1:
            chromosome.append(parent1[locus])
        else:
            chromosome.append(parent2[locus])

    return (chromosome)


def uniform_bin(parent1, parent2, bits):
    """Return a new chromosome using uniform crossover on a binary string.

    This is suitable for binary encoding.

    Args:
        parent1 (int): A parent chromosome.
        parent2 (int): A parent chromosome.
        bits (int): The number of bits used in the encoding.

    Returns:
        Tuple[List]: A new chromosome descended from the given parents.
    """
    child = 0
    for locus in range(0, bits):
        mask = 2 ** locus
        child = mask & parent1 | child
        parent1, parent2 = parent2, parent1

    return child


def ordered(parent1, parent2, point=None):
    """Return a new chromosome using ordered crossover (OX).

    This crossover method, also called order-based crossover, is suitable for
    permutation encoding. Ordered crossover respects the relative position of
    alleles.

    Args:
        parent1 (List): A parent chromosome.
        parent2 (List): A parent chromosome.
        points (int): The point at which to cross over.

    Returns:
        Tuple[List]: A new chromosome descended from the given parents.
    """
    if point is None:
        point = random.randint(0, len(parent1) - 1)

    child = parent1[0:point]

    for value in parent2:
        if value not in child:
            child.append(value)

    return (child)


def partially_matched(parent1, parent2):
    """Return a new chromosome created via partially matched crossover (PMX).

    This is suitable for permutation encoded GAs. Partially matched crossover
    respects the absolute position of alleles.

    Args:
        parent1 (List): A parent chromosome.
        parent2 (List): A parent chromosome.

    Returns:
        Tuple[List]: A new chromosome descended from the given parents.
    """
    third = len(parent1) // 3
    l1 = int(random.triangular(1, third, third * 2))
    l2 = int(random.triangular(third, third * 2, len(parent1) - 1))

    if l2 < l1:
        l1, l2 = l2, l1

    matching = parent2[l1:l2]
    displaced = parent1[l1:l2]
    child = parent1[0:l1] + matching + parent1[l2:]

    tofind = [item for item in displaced if item not in matching]
    tomatch = [item for item in matching if item not in displaced]

    for k, v in enumerate(tofind):
        subj = tomatch[k]
        locus = parent1.index(subj)
        child[locus] = v

    return (child)


def edge_recombination(parent1, parent2):
    """Return a new chromosome created using an edge recombination operation.

    This is suitable for permutation encoded GAs.
    """
    return (ero.recombine(parent1, parent2))


class ConfigurableCrossoverGA(base.GeneticAlgorithm):
    """A GA trait that makse the crossover method configurable.

    This helps to compare the performance of different operators.

    When using binary operators, the ``chromosome_length`` property of the GA
    object must be set.
    """

    operators = {
        "single_point": single_point,
        "single_point_bin": single_point_bin,
        "multiple_points": multiple_points,
        "uniform": uniform,
        "uniform_bin": uniform_bin,
        "ordered": ordered,
        "partially_matched": partially_matched,
        "edge_recombination": edge_recombination,
    }
    """A mapping of operator names to functions."""


    def __init__(self, config={}):
        super(ConfigurableCrossoverGA, self).__init__(config)

        operator = self.config.setdefault("crossover_operator", None)
        self.is_binary = False

        if operator is not None:
            self.xop = ConfigurableCrossoverGA.operators[operator]

            is_binary = re.compile("^.*_bin$")
            if is_binary.match(operator):
                self.is_binary = True

        else:
            self.xop = None

    @classmethod
    def arg_parser(cls):
        parser = super(ConfigurableCrossoverGA, cls).arg_parser()
        parser.add_argument("--crossover-operator", "-cx",
                            help="Crossover operator")
        return parser

    def crossover(self):
        if self.xop is None:
            raise Exception("Crossover operator has not been configured.")

        if self.is_binary and not self.chromosome_length:
            raise Exception("Missing required property ``chromosome_length``.")

        parent1 = self.select()
        parent2 = self.select()

        if self.is_binary:
            return self.xop(parent1, parent2, self.chromosome_length)
        else:
            return self.xop(parent1, parent2)
