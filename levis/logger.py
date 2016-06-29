"""Logging traits for genetic algorithms.

- **LoggingGA**: A big trait that enables logging the entire contents of each
  generation, as well as performance stats at configurable intervals. Note that
  to enable the ``--verbose`` command line argument, your GA must extend this
  class.
- **LoggingProportionateGA**: A logging trait that takes advantage of the
  cached scores calculated after each generation in a ``ProportionateGA``.

"""

import logging
import random
import sys

from . import base


# pylint: disable=abstract-method
class LoggingGA(base.GeneticAlgorithm):
    """The base trait for logging behavior in GAs."""

    def __init__(self, config={}):
        super(LoggingGA, self).__init__(config)

        self.stats_frequency = self.config.setdefault("stats_frequency", 1.0)

        # Configure fitness score logging
        self.log_fitness = self.config.setdefault("log_fitness", True)
        self.stats_logger = logging.getLogger("levis.stats")
        self.stats_logger.setLevel(logging.INFO)
        self.stats_logger.addHandler(logging.NullHandler())

        if "stats_file" in self.config:
            self.log_fitness = True
            fhstats = logging.FileHandler(self.config["stats_file"])
            logging.getLogger("levis.stats").addHandler(fhstats)

        # Configure population logging
        self.log_pop = self.config.setdefault("log_population", False)
        self.population_logger = logging.getLogger("levis.population")
        self.population_logger.setLevel(logging.INFO)
        self.population_logger.addHandler(logging.NullHandler())

        if "population_file" in self.config:
            self.log_pop = True
            fhpop = logging.FileHandler(self.config["population_file"])
            logging.getLogger("levis.population").addHandler(fhpop)

        # Verbosity: logging fitness to stdout
        if self.config.setdefault("verbose", False):
            self.log_fitness = True
            handler = logging.StreamHandler(sys.stdout)
            logging.getLogger("levis.stats").addHandler(handler)

    def add_arguments(self, parser):
        super(LoggingGA, self).add_arguments(parser)
        parser.add_argument("--stats-file", "-sf",
                            help="Path to the stats log file, if any")
        parser.add_argument("--stats-freq", default=1.0, type=float,
                            help="Frequency at which to log statistics")
        parser.add_argument("--population-file", "-pf",
                            help="Path to a log of each generation")
        parser.add_argument("--verbose", "-v", default=False,
                            action="store_const", const=True,
                            help="Log stats and population change to stdout")

    def seed(self):
        super(LoggingGA, self).seed()
        self.log_population()

    def post_generate(self):
        super(LoggingGA, self).post_generate()

        if self.log_pop:
            self.log_population()
        if self.log_fitness and random.random() <= self.stats_frequency:
            self.log_stats()

    def log_stats(self):
        """Write generational statistics to a logger."""
        scores = [t[1] for t in self.score_population()].sort(reverse=True)
        avg_score = sum(scores) / len(scores)

        self.stats_logger.info(
            "%s,%i,%f,%f,%f",
            self.id,
            self.iteration,
            scores[0],
            avg_score,
            scores[-1]
        )

    def log_population(self):
        """Write the current population to a logger."""
        chromos = [self.chromosome_str(chromo) for chromo in self.population]
        population = "[%s]" % ", ".join(chromos)
        self.population_logger.info("%s: %i: %s", self.id, self.iteration, population)


class LoggingProportionateGA(LoggingGA):
    """A logger that uses the cached scores in a ```ProportionateGA``."""

    def log_stats(self):
        """Write generational statistics to a logger."""
        # pylint: disable=no-member
        scores = [t[1] for t in self.scored]
        avg_score = sum(scores) / len(scores)

        self.stats_logger.info(
            "%s,%i,%f,%f,%f",
            self.id,
            self.iteration,
            scores[0],
            avg_score,
            scores[-1]
        )
