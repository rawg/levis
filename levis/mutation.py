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


def point(chromosome, value):
    """Return a mutant made through point mutation.

    This chooses a random point in a list and replaces it with ``value``. It is
    suitable for use with list and value encoding.

    Args:
        chromosome (List): The source chromosome for mutation.
        value (Any): A value to assign to a random locus. It should be selected
            at random before invoking this method.

    Returns:
        List: A mutant chromosome.

    """
    locus = random.randint(0, len(chromosome) - 1)
    mutant = list(chromosome)
    mutant[locus] = value
    return mutant


def swap(chromosome):
    """Return a mutated chromosome made through swap mutation.

    This chooses two random points in a list and swaps their values. It is
    suitable for use with list, value, and permutation encoding, but designed
    for the latter.

    Args:
        chromosome (List): The source chromosome for mutation.

    Returns:
        List: A mutant chromosome.

    """
    l1 = random.randint(0, len(chromosome) - 1)
    l2 = l1
    while l2 == l1:
        l2 = random.randint(0, len(chromosome) - 1)

    mutant = list(chromosome)
    mutant[l1], mutant[l2] = mutant[l2], mutant[l1]

    return mutant


def toggle(chromosome, length):
    """Return a mutated chromosome made through inverting a random bit.

    This chooses a random bit in a binary string and toggles it.

    Args:
        chromosome (int): The source chromosome for mutation.
        length (int): The number of bits in use by the encoding scheme.

    Returns:
        int: A mutant chromosome.
    """
    locus = random.randint(0, length - 1)
    return chromosome ^ 2 ** locus
