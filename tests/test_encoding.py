"""Unit tests for encoding helpers.

"""
from __future__ import absolute_import


import unittest

from . import harness

from levis.encoding import *


class BinaryGAUT(harness.DummyBinaryGA, BinaryGA):
    def num_bits(self):
        return 8

class BinaryGATestCase(harness.BaseGATestCase):
    def gacls(self):
        return BinaryGAUT

# TODO Tests for value, list, and permutation classes, which don't work with
#      the DummyBinaryGA.
