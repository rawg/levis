"""Additional behaviors for genetic algorithms.


"""
from __future__ import division

import math

from . import GeneticAlgorithm


class FittestTriggerGA(GeneticAlgorithm):
    """A GA that triggers ``new_best`` when a new high score is observed."""

    def __init__(self, config={}):
        super(FittestTriggerGA, self).__init__(config)
        self.best_score = (0, None)

    def fitness(self, chromosome):
        """Check the score of a chromosome.

        Triggers ``new_best`` if there's a winner.
        """
        score = super(FittestTriggerGA, self).fitness(chromosome)
        if score > self.best_score[0]:
            self.new_best(score, chromosome)
            self.best_score = (score, chromosome)

        return score

    def new_best(self, score, chromosome):
        """Triggered when a new best fitness score is seen."""
        pass

    def best(self):
        return self.best_score[1]


class FittestInGenerationGA(FittestTriggerGA):
    """A behavior that stores the best score from each generation."""

    def __init__(self, config={}):
        super(FittestInGenerationGA, self).__init__(config)
        self.best_scores = []

    def pre_generate(self):
        super(FittestInGenerationGA, self).pre_generate()
        self.best_score = (0, None)

    def post_generate(self):
        super(FittestInGenerationGA, self).post_generate()
        self.best_scores.append(self.best_score[0])


class FinishWhenSlowGA(FittestInGenerationGA):
    """A GA that stops if progress hasn't been made."""

    def __init__(self, config={}):
        super(FinishWhenSlowGA, self).__init__(config)
        self.threshold = self.config.setdefault("threshold", 0.05)
        self.lookback = self.config.setdefault("lookback", 5)

    def is_finished(self):
        exceeded_duration = self.iteration >= self.max_iterations

        if len(self.best_scores) > self.lookback:
            first = self.best_scores[-self.lookback]
            last = self.best_scores[-1]
            gain = (last - first) / first

            return gain <= self.threshold or exceeded_duration

        else:
            return exceeded_duration


class ElitistGA(GeneticAlgorithm):
    """A GA that preserves the fittest solutions for crossover."""

    def __init__(self, config={}):
        super(ElitistGA, self).__init__(config)

        pct = self.config.setdefault("elitism_pct", 0.02)
        self.elitism_pct = pct
        self.num_elites = int(math.ceil(pct * self.population_size))
        self.elites = []

    def fitness(self, chromosome):
        """Add a chromosome to the population of elite solutions."""

        score = super(ElitistGA, self).fitness(chromosome)

        if self.num_elites > 0:

            if len(self.elites) > 0:
                sentry = self.elites[-1][0]
            else:
                sentry = 0

            if (score > sentry or len(self.elites) < self.num_elites):

                add = (score, chromosome)
                pos = None

                for i in range(0, len(self.elites)):
                    if score > self.elites[i][0]:
                        pos = i

                if pos is None:
                    self.elites.append(add)
                elif pos == 0:
                    self.elites = [add] + self.elites
                else:
                    self.elites = self.elites[0:pos] + [add] + self.elites[pos:-1]

                if len(self.elites) > self.num_elites:
                    self.elites = self.elites[0:-1]

        return score

    @classmethod
    def arg_parser(cls):
        parser = super(ElitistGA, cls).arg_parser()
        parser.add_argument("--elitism", "-e", type=float,
                            help="Percentage of the population to preserve in "
                            "elitism (0.0-1.0)")
        return parser

    def pre_generate(self):
        """Create a new generation using elitism with crossover and mutation.

        This method uses the base `fill_population` method, but seeds the
        generation with the fittest members of the current generation. Scoring
        the population is also invoked here.
        """
        super(ElitistGA, self).pre_generate()

        if len(self.elites) > 0:
            self.next_generation += [elite[1] for elite in self.elites]
