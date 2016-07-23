"""Additional behaviors for genetic algorithms.


Contents
--------
:FittestTriggerGA:
    A GA that triggers an event whenever a new best fitness score is observed.
:FittestInGenerationGA:
    A GA that stores the fittest chromosome from each generation and its score.
:FinishWhenSlowGA:
    A GA that will terminate when it is no longer making progress.

Note that when using strategies that do not score each member of every
generation, such as tournament selection, best scores may go undetected.

Also note that, if using such a strategy, it is possible that adding logging
will create the side effect of squelching this behavior, since some logging
strategies score all chromosomes.

"""
from __future__ import division

import math

from . import GeneticAlgorithm


class FittestTriggerGA(GeneticAlgorithm):
    """A GA with an event for new high scores.

    When a new all-time high score is observed for this instance, the
    ``new_best`` method is invoked.
    """

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
    """A behavior that stores the best score from each generation.

    The fittest chromosome and its score of each generation are stored as a
    2-tuple of ``(score, chromosome)`` in ``self.best_scores``.

    """

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
    """A GA that will terminate when it is no longer making progress.

    To configure this behavior, adjust the ``threshold`` and ``lookback``
    configuration properties.

    If the percentage improvement of progress in ``lookback`` iterations hasn't
    exceeded ``threshold``, then the GA will terminate. The GA will also
    terminate if the number of iterations has exceeded ``max_iterations``.
    """

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
