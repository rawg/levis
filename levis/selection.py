"""Selection strategies for genetic algorithms.

Included is an implementation of a fitness proportionate strategy as well as
tournament selection.

ProportionateGA
  Proportionate selection scores all chromosomes in each generation and gives
  more fit chromosomes an advantage in selection for reproduction that is
  proportionate to the fitness scores. For instance, a chromosome with a score
  of 10 will be twice as likely to be selected as one with a score of 5.

  With proportionate selection comes the advantages of convergence in fewer
  generations and elitism, ensuring the best members of a generation live on
  unchanged to the next.

ScalingProportionateGA
  This is proportionate selection, but one that scales the reproductive
  advantage by using the minimum non-zero score as the lower end of a scale. If
  the highest score in a generation is 100 and the lowest is 30, then scores
  will be scaled from 1 to 70 to increase the advantage of more fit
  individuals.

TournamentGA
  Tournament selection scores a random sample of the population and always
  promotes the member with the best score for reproduction. Elitism is moot,
  since there is no guarantee that the highest scored members of a generation
  are the most fit, but convergence can come in fewer CPU cycles when the
  fitness function is expensive, and it has the advantage of being agnostic to
  the scale of scores.

"""
from __future__ import division
#from builtins import range

import math
import random

from . import base


class ProportionateGA(base.GeneticAlgorithm):
    """Behaviors for a GA to use fitness proportionate selection."""

    def __init__(self, config={}):
        super(ProportionateGA, self).__init__(config)
        self.scored = None

    def proportion_population(self):
        """Return a scored and ranked copy of the population.

        This scores the fitness of each member of the population and returns
        the complete population as `[(member, score, weighted fitness)]`.
        """

        ranked = super(ProportionateGA, self).score_population()
        shares = float(sum([t[1] for t in ranked]))

        self.scored = []
        tally = 0
        for tupl in ranked:
            if tupl[1] > 0:
                share = tupl[1] / shares
                tally = tally + share
                # chromosome, score, share range
                self.scored.append((tupl[0], tupl[1], tally))

    def score_population(self):
        """Return a scored and ranked copy of the population.

        For efficiency, the scores calculated across each generation for
        selection are reused."""
        return self.scored

    def select(self):
        """Select a member of the population in a fitness-proportionate way."""
        number = self.random.random()
        for ticket in self.scored:
            if number < ticket[2]:
                return ticket[0]

        raise Exception("Failed to select a parent. Begin troubleshooting by "
                        "checking your fitness function.")

    def pre_generate(self):
        """Create a new generation using elitism with crossover and mutation.

        This method uses the base `fill_population` method, but seeds the
        generation with the fittest members of the current generation. Scoring
        the population is also invoked here.
        """
        super(ProportionateGA, self).pre_generate()

        # First iteration
        if self.scored is None:
            self.proportion_population()

    def post_generate(self):
        super(ProportionateGA, self).post_generate()
        self.proportion_population()

    def best(self):
        return self.scored[0][0]


class ScalingProportionateGA(ProportionateGA):
    """A proportionate selection strategy that scales scores."""

    def proportion_population(self):
        """Return a scored and ranked copy of the population.

        This scores the fitness of each member of the population and returns
        the complete population as `[(member, score, weighted fitness)]`.
        """

        ranked = super(ProportionateGA, self).score_population()
        scores = [t[1] for t in ranked if t[1] > 0]
        worst = min(scores)
        shares = float(sum([t[1] - worst for t in ranked]))

        self.scored = []
        tally = 0
        for tupl in ranked:
            if tupl[1] > 0:
                share = tupl[1] / shares
                tally = tally + share
                # chromosome, score, share range
                self.scored.append((tupl[0], tupl[1], tally))


class TournamentGA(base.GeneticAlgorithm):
    """Behaviors for tournament selection in a GA."""

    def __init__(self, config={}):
        super(TournamentGA, self).__init__(config)

        sample_size = int(math.ceil(self.population_size * 0.02))
        self.config.setdefault("tournament_size", sample_size)

        self.tournament_size = self.config["tournament_size"]

    @classmethod
    def get_parser(cls):
        parser = super(TournamentGA, cls).get_parser()
        parser.add_argument("--tournament-size", type=int,
                            help="Number of chromosomes to sample in a"
                            "tournament.")
        return parser

    def select(self):
        """Return the best genotype found in a random sample."""
        pop = [self.random.choice(self.population)
               for _ in range(0, self.tournament_size)]

        scored = [(geno, self.fitness(geno)) for geno in pop]
        scored.sort(key=lambda n: n[1])
        scored.reverse()

        return scored[0][0]


class ElitistGA(base.GeneticAlgorithm):
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
                        break

                if pos is None:
                    self.elites.append(add)
                elif pos == 0:
                    self.elites = [add] + self.elites
                else:
                    self.elites = self.elites[0:pos] + [add] + self.elites[pos:]

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
