"""Functions for mutation operations.

Contents
--------

Mutation operators are implemented as functions. The available operators and
their suitability to encoding types is listed below.

=========   ======  ====  ===========
Operation   Binary  List  Permutation
=========   ======  ====  ===========
point       No      Yes   No
toggle      Yes     No    No
swap        No      Yes   Yes
=========   ======  ====  ===========

"""

import random


def point(chromosome, generator, probability):
    """Return a mutant made through point mutation.

    In this scheme, mutated alleles will be replaced with a value provided by
    calling ``generator``. It is suitable for use with list or value encoding.

    Args:
        chromosome (List): The source chromosome for mutation.
        generator (Callable[[], Any]): A function that will provide a value to
            assign to a random locus. It should be selected at random, but if
            you are sure of yourself you may select it from a non-uniform
            distribution.
        probability (float): The mutation rate or the probability that an
            allele will be mutated.

    Returns:
        List: A mutant (maybe) chromosome.
    """
    mutant = list(chromosome)
    for locus in range(0, len(chromosome)):
        if random.random() < probability:
            mutant[locus] = generator()
    return mutant

def heterogeneous_length(chromosome, generator, probability):
    """Return a mutant made through point mutation that may grow or shrink.

    In this scheme, mutated alleles will be replaced with a value provided by
    calling ``generator``. It is suitable for use with list encoding. Be warned
    that this will lead to chromosomes of heterogenous length.

    Args:
        chromosome (List): The source chromosome for mutation.
        generator (Callable[[], Any]): A function that will provide a value to
            assign to a random locus. It should be selected at random, but if
            you are sure of yourself you may select it from a non-uniform
            distribution.
        probability (float): The mutation rate or the probability that an
            allele will be mutated.

    Returns:
        List: A mutant (maybe) chromosome.
    """
    mutant = point(chromosome, generator, probability)
    if random.random() < probability:
        mutant.append(generator())

    if random.random() < probability:
        locus = random.randint(0, len(mutant) - 1)
        del mutant[locus]

    return mutant

def swap(chromosome, probability):
    """Return a mutated chromosome made through swap mutation.

    This chooses two random points in a list and swaps their values. It is
    suitable for use with list, value, and permutation encoding, but designed
    for the latter.

    Args:
        chromosome (List): The source chromosome for mutation.
        probability (float): The mutation rate or the probability that an
            allele will be mutated.

    Returns:
        List: A mutant chromosome.

    """
    mutant = list(chromosome)
    changes = 0
    offset = probability

    for locus1 in range(0, len(chromosome)):
        if random.random() < offset:
            locus2 = locus1
            while locus2 == locus1:
                locus2 = random.randint(0, len(chromosome) - 1)

            mutant[locus1], mutant[locus2] = mutant[locus2], mutant[locus1]
            changes += 2
            offset = probability / changes

    return mutant


def toggle(chromosome, length, probability):
    """Return a mutated chromosome made through inverting a random bit.

    This chooses a random bit in a binary string and toggles it.

    Args:
        chromosome (int): The source chromosome for mutation.
        length (int): The number of bits in use by the encoding scheme.
        probability (float): The mutation rate or the probability that an
            allele will be mutated.

    Returns:
        int: A mutant chromosome.
    """
    for locus in range(0, length):
        if random.random() < probability:
            chromosome = chromosome ^ 2 ** locus

    return chromosome
