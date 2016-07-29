# coding=utf-8
"""Logging traits for genetic algorithms.

Contents
--------

:FitnessLoggingGA:
    A trait that logs the minimum, mean, and maximum score of all or a sample
    of generations.
:PopulationLoggingGA: A trait that logs each chromosome in a generation.

"""
from __future__ import division

import logging
import random

from . import base


# pylint: disable=abstract-method
class FitnessLoggingGA(base.GeneticAlgorithm):
    """A trait that logs the min, mean, and max score of each generation.

    Enable fitness logging by mixing this trait into your GA and setting
    ``log_fitness`` to true in the ``config`` object. Once enabled, statistics
    will be written to any ``logging`` handlers bound to the ``levis.stats``.

    If the ``stats_file``/``--stats-file`` option is set, logging is
    automatically enabled and a ``FileHandler`` created.

    Statistics for each generation are logged as a CSV format with the
    following fields:

      1. GA Instance ID, a UUID created in ``base.GeneticAlgorithm.__init__``.
      2. Generation number.
      3. Best score in the generation.
      4. Mean score for the generation.
      5. Worst score for the generation.

    By default, statistics will be logged for each generation. This requires
    calling ``score_generation``. In a GA that uses proportionate selection,
    every member of each generation is already scored, and so there is no
    overhead (calls to ``score_generation`` are memoized in
    ``selection.ProportionateGA`` and its descendants). But in tournament
    selection - one of the advantages to which is invoking the fitness function
    less often - this may increase the clock time of your algorithm. To avoid
    rescoring each population, you can provide a probability to log each
    generation by assigning the ``stats_frequency``/``--stats-freq`` option a
    float between 0.0 and 1.0. For instance, to log half of all generations,
    sets ``stats_freq`` to 0.5.
    """

    def __init__(self, config={}):
        super(FitnessLoggingGA, self).__init__(config)

        self.stats_frequency = self.config.setdefault("stats_frequency", 1.0)

        self.log_fitness = self.config.setdefault("log_fitness", True)
        self.stats_logger = logging.getLogger("levis.stats")
        self.stats_logger.setLevel(logging.INFO)
        self.stats_logger.addHandler(logging.NullHandler())

        if "stats_file" in self.config:
            self.log_fitness = True
            fhstats = logging.FileHandler(self.config["stats_file"])
            logging.getLogger("levis.stats").addHandler(fhstats)

    @classmethod
    def arg_parser(cls):
        parser = super(FitnessLoggingGA, cls).arg_parser()
        parser.add_argument("--stats-file", "-sf",
                            help="Path to the stats log file, if any")
        parser.add_argument("--stats-freq", default=1.0, type=float,
                            help="Frequency at which to log statistics")
        return parser

    def post_generate(self):
        super(FitnessLoggingGA, self).post_generate()

        if self.log_fitness and self.random.random() <= self.stats_frequency:
            self.log_stats()

    def log_stats(self):
        """Write generation statistics to a logger."""
        scores = [t[1] for t in self.score_population()] #.sort(reverse=True)
        if len(scores) == 0:
            stats = (0.0, 0.0, 0.0)
        else:
            stats = (scores[0], sum(scores) / len(scores), scores[-1])

        self.stats_logger.info(
            "%s,%i,%f,%f,%f",
            self.id,
            self.iteration,
            stats[0],
            stats[1],
            stats[2]
        )


class PopulationLoggingGA(base.GeneticAlgorithm):
    """A trait that logs each chromosome in every generation.

    A representation of each chromosome is created using ``chromosome_str``.

    Enable population logging by mixing this trait into your GA and setting
    ``log_population`` to true in the ``config`` object. Once enabled, the
    contents of each generation will be written to any ``logging`` handlers
    bound to the ``levis.population``.

    If the ``population_file``/``--population-file`` option is set, logging is
    automatically enabled and a ``FileHandler`` created.
    """

    def __init__(self, config={}):
        super(PopulationLoggingGA, self).__init__(config)
        self.log_pop = self.config.setdefault("log_population", False)
        self.population_logger = logging.getLogger("levis.population")
        self.population_logger.setLevel(logging.INFO)
        self.population_logger.addHandler(logging.NullHandler())

        if "population_file" in self.config:
            self.log_pop = True
            fhpop = logging.FileHandler(self.config["population_file"])
            logging.getLogger("levis.population").addHandler(fhpop)

    @classmethod
    def arg_parser(cls):
        parser = super(PopulationLoggingGA, cls).arg_parser()
        parser.add_argument("--population-file", "-pf",
                            help="Path to a log of each generation")
        return parser

    def seed(self):
        super(PopulationLoggingGA, self).seed()
        self.log_population()

    def post_generate(self):
        super(PopulationLoggingGA, self).post_generate()

        if self.log_pop:
            self.log_population()

    def log_population(self):
        """Write the current population to a logger."""
        chromos = [self.chromosome_str(chromo) for chromo in self.population]
        population = "[%s]" % ", ".join(chromos)
        self.population_logger.info("%s: %i: %s", self.id, self.iteration,
                                    population)
