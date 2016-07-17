
############################################
Levis: Programming by the Seat of Your Genes
############################################

A toolkit for genetic algorithms in Python, written as a companion to a
technical talk.


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

Levis currently has no external dependencies for basic use. Image rendering in
the examples, when implemented, relies on ``svgwrite``, and some data
generation needs ``Faker``.::

  $ pip install svgwrite
  $ pip install fake-factory


Installing
~~~~~~~~~~
Install by cloning the git repository. Installation via PyPI is coming soon.::

  $ git clone https://github.com/rawg/levis


Running Examples
~~~~~~~~~~~~~~~~

If you're looking at this project, you're probably more interested in the
example implementations than in the core genetic behaviors. Each ``*.py`` file
in  the ``examples/`` folder should respond to a ``-h`` argument to list its
options. All should run without any options, but you'll want to tweak the
parameters to better understand each algorithm.::

  $ cd examples/
  $ python knapsack01.py -h
  $ python knapsack01.py --iterations=10 --population-size=5


Testing
-------

Running the Unit Tests
~~~~~~~~~~~~~~~~~~~~~~
To run all tests:::

  $ python all_tests.py

If you wish to run individual tests, you'd best know PEP 328 inside and out!


Testing Code Style
~~~~~~~~~~~~~~~~~~

The code is run through ``pylint``, if that sort of thing interests you. Note
that many pylint warnings are currently ignored, but it's good to know your
faults.


Future Items
------------

- [ ] Cycle crossover
- [ ] Merge crossover
- [ ] Explicit "cut-and-splice" crossover (use n-point in the meantime)

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
