"""Logging traits for genetic algorithms.

- **LoggingGA**: A big trait that enables logging the entire contents of each
  generation, as well as performance stats at configurable intervals. Note that
  to enable the ``--verbose`` command line argument, your GA must extend this
  class.
- **LoggingProportionateGA**: A logging trait that takes advantage of the
  cached scores calculated after each generation in a ``ProportionateGA``.

"""
from __future__ import division

import logging
import random

from . import base


# pylint: disable=abstract-method
class FitnessLoggingGA(base.GeneticAlgorithm):
    """The base trait for logging behavior in GAs."""

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

        if self.log_fitness and random.random() <= self.stats_frequency:
            self.log_stats()

    def log_stats(self):
        """Write generational statistics to a logger."""
        scores = [t[1] for t in self.score_population()] #.sort(reverse=True)
        avg_score = sum(scores) / len(scores)

        self.stats_logger.info(
            "%s,%i,%f,%f,%f",
            self.id,
            self.iteration,
            scores[0],
            avg_score,
            scores[-1]
        )


class PopulationLoggingGA(base.GeneticAlgorithm):
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
        self.population_logger.info("%s: %i: %s", self.id, self.iteration, population)
