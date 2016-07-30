
############################################
Levis: Programming by the Seat of Your Genes
############################################

.. image:: https://travis-ci.org/rawg/levis.svg?branch=master
    :target: https://travis-ci.org/rawg/levis
.. image:: https://badge.fury.io/py/levis.svg
    :target: https://badge.fury.io/py/levis

A toolkit for genetic algorithms in Python. Pronounce it like the denim pants,
because ``levis`` lets you program by the seat of your genes!


Overview
--------
The ``levis`` package contains a collection of genetic traits meant
to be composed to achieve a desired algorithm behavior.

To implement your own GA, you will probably want to extend from one of the
classes in ``selection`` and one of the classes in ``logger``. The former will
give you proportionate or tournament selection, and the latter will enable
logging (including verbosity).

You'll also want to override the ``crossover()`` and ``mutate()`` methods with
implementations from the packages by the same name.

The examples each have three components: a genetic solution, a method to
generate data, and a ``main`` method to wire in command line arguments. The
examples will respond to a ``-h`` flag to display help.


Getting Started
---------------

Prerequisites
~~~~~~~~~~~~~

One of levis' design goals is to be runnable on the default Mac OS Python
installation. As a result, levis targets Python 2.7+ and 3.2+. There are no
dependencies to work with levis, but image rendering in the examples, when
implemented, relies on ``svgwrite``, and some data generation needs ``Faker``.
::

  $ pip install svgwrite
  $ pip install fake-factory


Installing
~~~~~~~~~~
Installation is now available via PyPI.
::

  $ pip install levis


Running Examples
~~~~~~~~~~~~~~~~

If you're looking at this project, you're probably more interested in the
example implementations than in the core genetic behaviors. Each ``*.py`` file
in  the ``examples/`` folder should respond to a ``-h`` argument to list its
options. All should run without any options, but you'll want to tweak the
parameters to better understand each algorithm.
::

  $ cd examples/
  $ python knapsack01.py -h
  $ python knapsack01.py --iterations=10 --population-size=5


Testing
-------

Running the Unit Tests
~~~~~~~~~~~~~~~~~~~~~~
The examples of running the unit tests below should be run from the project's
root directory.

To run all tests:
::

  $ python all_tests.py

Running an individual test method:
::

  $ python -m tests.test_behavior FinishWhenSlowGATestCase.test_doesnt_finish_when_fast

Running a single test case:
::

  $ python -m tests.test_behavior FinishWhenSlowGATestCase

Running a single test file:
::

  $ python -m tests.test_behavior


Testing Code Style
~~~~~~~~~~~~~~~~~~

The code is periodically checked with ``pylint``, if that sort of thing
interests you. Note that several ``pylint`` warnings are currently ignored, but
it's good to know your faults.


Planned Changes
---------------

You can expect the following in future releases:

- Additional crossover operators, such as cycle and merge crossover.
- Additional traits for crossover and mutation operators.
- The examples will be moved to another repository and several more will be
  added.
- API documentation and a user's guide will be available (probably at
  readthedocs.org)

Please be aware that the API is in flux, and changes between versions may still
introduce breaking changes.


Change Log
----------

:v0.5.1: Fixing an off by one error when randomly selecting points in
         ``crossover.multiple_points``.

:v0.5.0: This version changes some behaviors to match more canonical
         implementations. Specifically:

         - All crossover operators return a list of children. Most operators
           create two children from two parents.
         - Mutation rate is now expressed as the probability of a mutation to
           *any* allele, not the probability that a chromosome will undergo a
           mutation.
         
         Additionally, a cut and splice crossover operator and a point mutation
         that may add or shrink chromosomes has been added for better support
         for list encoding schemes of heterogeneous length.

:v0.4.0: A big step toward a stable API, this version includes decomposed
         logging traits, an implementation of elitism that works with
         tournament selection, a number of bug fixes and minor improvements,
         and installation via ``pip``/PyPI.


Versioning
----------
Version numbers follow the `SemVer <http://semver.org/>`_ scheme. For the
versions available, see the `tags on this repository
<https://github.com/your/project/tags>`_. 


Authors
-------
Only one soul can be blamed for this:

- Jeremy Fisher, `@thisisroot <https://twitter.com/thisisroot>`_.


License
-------
This project is licensed under the MIT License - see
the `LICENSE.md <LICENSE.md>`_ file for details.
