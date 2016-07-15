"""Unit tests for the base GeneticAlgorithm class.

"""


import unittest

import context
import harness

from levis.selection import ProportionateGA, ScalingProportionateGA, TournamentGA


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


if __name__ == '__main__':
    unittest.main()
