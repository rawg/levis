"""Additional behaviors for genetic algorithms.


"""
from __future__ import division

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
        self.last_progress_iter = 0
        self.threshold = self.config.setdefault("threshold", 0.05)
        self.lookback = self.config.setdefault("lookback", 5)

    def is_finished(self):
        exceeded_duration = self.iteration >= self.max_iterations

        if len(self.best_scores) > self.lookback:
            first = self.best_scores[-self.lookback]
            last = self.best_scores[-1]
            gain = (last - first) / first

            return gain < self.threshold or exceeded_duration

        else:
            return exceeded_duration
