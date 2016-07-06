"""
Genetic solution to the 0/1 Knapsack Problem.

    usage: knapsack01.py [-h] [--data-file DATA_FILE]
                         [--population-size POPULATION_SIZE]
                         [--iterations MAX_ITERATIONS] [--mutation MUTATION_PROB]
                         [--crossover CROSSOVER_PROB] [--seed SEED]
                         [--stats-file STATS_FILE]
                         [--population-file POPULATION_FILE] [--verbose]
                         [--elitism ELITISM] [--uniform_cx] [--generate]
                         [--items NUM_ITEMS]

"""

import math
import random

# pylint: disable=unused-import,relative-import
from . import context

import levis
from levis import configuration
from levis import crossover
from levis import mutation


class Knapsack01GA(levis.ProportionateFitnessLoggingGA, levis.ProportionateGA):
    """Genetic solution to the 0/1 Knapsack Problem."""

    def __init__(self, config={}):
        """Initialize a 0/1 knapsack solver.

        Raises:
            AttributeError: If ``items`` is not in the configuration dict.
        """
        super(self.__class__, self).__init__(config)

        self.max_weight = self.config.setdefault("max_weight", 15)
        self.items = self.config.setdefault("items", [])
        self.chromosome_length = len(self.items)
        self.uniform_cx = config.setdefault("uniform_cx", False)

        for i, item in enumerate(self.items):
            item["mask"] = 2 ** i

    def assess(self, chromosome):
        """Return a 2-tuple of the total weight and value of a chromosome."""
        weight = 0
        value = 0

        # pylint: disable=unused-variable
        for locus, _ in enumerate(self.items):
            if chromosome & 2 ** locus:
                item = self.items[locus]
                weight += item["weight"]
                value += item["value"]

        return (weight, value)

    def score(self, chromosome):
        weight, value = self.assess(chromosome)

        if weight > self.max_weight:
            return 0.0

        return value

    def create(self):
        # The below generates chromosomes, but the majority are too heavy
        # return random.randint(0, 2 ** self.chromosome_length - 1)
        items = list(self.items)
        random.shuffle(items)
        weight = 0
        chromosome = 0

        for i in items:
            if weight + i["weight"] <= self.max_weight:
                weight += i["weight"]
                chromosome |= i["mask"]

        return chromosome

    def crossover(self):
        parent1 = self.select()
        parent2 = self.select()
        length = self.chromosome_length

        if self.uniform_cx:
            return crossover.uniform_bin(parent1, parent2, length)
        else:
            return crossover.single_point_bin(parent1, parent2, length)

    def mutate(self, chromosome):
        return mutation.toggle(chromosome, self.chromosome_length)

    def chromosome_str(self, chromosome):
        sack = []

        for locus, _ in enumerate(self.items):
            item = self.items[locus]["name"]
            packed= 0

            if chromosome & 2 ** locus:
                packed = 1

            sack.append("%s: %i" % (item, packed))

        weight, value = self.assess(chromosome)

        vals = (weight, value, ", ".join(sack))

        return "{weight: %0.2f, value: %0.2f, contents: [%s]}" % vals

    def chromosome_repr(self, chromosome):
        return bin(chromosome)[2:].zfill(self.chromosome_length)


def create_data(config={}):
    """Create data and write to a JSON file."""
    max_weight = config.setdefault("max_weight", 15)
    items = []

    if "num_items" in config:
        num_items = config["num_items"]
        del config["num_items"]
    else:
        num_items = 32

    # Generate items
    digits = int(math.ceil(math.log(num_items, 16)))
    fmt = "%0" + str(digits) + "X"

    for i in range(0, num_items):
        name = fmt % (i + 1)
        weight = random.triangular(1.0, max_weight / 3, max_weight)
        value = random.random() * 100

        items.append({"name": name, "weight": weight, "value": value})

    config["items"] = items

    configuration.write_file(config)


def main():
    """Main method to parse args and run."""
    defaults = {
        "population_size": 10,
        "max_iterations": 10,
        "elitism_pct": 0.01,
        "population_file": "population.log",
        "stats_file": "stats.csv"
    }

    description = "Genetic solution to the 0/1 Knapsack Problem"
    parent = [Knapsack01GA.arg_parser()]
    parser = configuration.get_parser(description, "knapsack01.json", parent)

    parser.add_argument("--uniform_cx", action="store_true",
                        help="Use uniform crossover instead of single-point")
    parser.add_argument("--generate", action="store_true",
                        help="Generate and store problem data")

    group = parser.add_argument_group("data generation options")
    group.add_argument("--items", type=int, dest="num_items", default=32,
                       help="Number of items to generate")

    args = configuration.read_args(parser)

    if args["generate"]:
        del args["generate"]
        create_data(args)

    else:
        config_file = configuration.read_file(args)
        config = configuration.merge(defaults, config_file, args)

        solver = Knapsack01GA(config)
        solver.solve()
        print(solver.chromosome_str(solver.best()))


if __name__ == "__main__":
    main()
