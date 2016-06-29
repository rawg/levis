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

import math
import random

from . import base


class ProportionateGA(base.GeneticAlgorithm):
    """Behaviors for a GA to use fitness proportionate selection."""

    def __init__(self, config={}):
        super(ProportionateGA, self).__init__(config)
        self.scored = None
        self.elitism_pct = self.config.setdefault("elitism_pct", 0.02)
        self.elites = int(math.ceil(self.elitism_pct * self.population_size))

    def add_arguments(self, parser):
        super(ProportionateGA, self).add_arguments(parser)
        parser.add_argument("--elitism", "-e", type=float,
                            help="Percentage of the population to preserve in "
                            "elitism (0.0-1.0)")

    def proportion_population(self):
        """Return a scored and ranked copy of the population.

        This scores the fitness of each member of the population and returns
        the complete population as `[(member, score, weighted fitness)]`.
        """

        ranked = self.score_population()
        shares = float(sum([t[1] for t in ranked]))

        self.scored = []
        tally = 0
        for tupl in ranked:
            if tupl[1] > 0:
                share = tupl[1] / shares
                tally = tally + share
                # chromosome, score, share range
                self.scored.append((tupl[0], tupl[1], tally))

    def select(self):
        """Select a member of the population in a fitness-proportionate way."""
        number = random.random()
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

        if self.elites > 0:
            self.next_generation += [a[0] for a in self.scored[0:self.elites]]

        #self.population = self.fill_population(generation)

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

        ranked = self.score_population()
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

        sample_size = int(self.population_size * 0.02)
        self.tournament_size = self.config.setdefault("tournament_size",
                                                      sample_size)

    def add_arguments(self, parser):
        super(TournamentGA, self).add_arguments(parser)
        parser.add_argument("--tournament-size", type=int,
                            help="Number of chromosomes to sample in a"
                            "tournament.")

    def select(self):
        """Return the best genotype found in a random sample."""
        pop = [random.choice(self.population)
               for _ in range(0, self.tournament_size)]
        scored = [(geno, self.score(geno)) for geno in pop]
        scored.sort(key=lambda n: n[1])
        scored.reverse()

        return scored[0][0]
