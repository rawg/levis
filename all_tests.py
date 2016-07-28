#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.abspath('.'))

import unittest

suite = unittest.TestLoader().discover(".")
status = unittest.TextTestRunner(verbosity=1).run(suite).wasSuccessful()
sys.exit(not status)
