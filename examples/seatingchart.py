"""
A genetic algorithm to find optimal seating arrangements.

    usage: seatingchart.py [-h] [--data-file DATA_FILE]
                           [--population-size POPULATION_SIZE]
                           [--iterations MAX_ITERATIONS]
                           [--mutation MUTATION_PROB] [--crossover CROSSOVER_PROB]
                           [--seed SEED] [--crossover-operator CROSSOVER_OPERATOR]
                           [--stats-file STATS_FILE]
                           [--population-file POPULATION_FILE] [--verbose]
                           [--elitism ELITISM] [--generate] [--roles ROLES]
                           [--people PEOPLE] [--width WIDTH] [--height HEIGHT]
                           [--attraction ATTRACTION] [--repulsion REPULSION]


"""

import math
import random

# pylint: disable=unused-import,relative-import
import context

import levis
from levis import configuration
from levis import crossover
from levis import spatial
from levis import mutation

# pylint: disable=too-many-instance-attributes, abstract-method
class SeatingChartGA(
        levis.ScalingProportionateGA,
        levis.LoggingProportionateGA,
        levis.ConfigurableCrossoverGA
    ):
    """Genetic solution to simple seating chart assignments."""

    EMPTY_ROLE = "-"
    """The role ID for an empty seat"""

    def __init__(self, config={}):
        """Initialize a genetic algorithm for the Seating Chart Problem."""
        super(self.__class__, self).__init__(config)

        self.people = self.config.setdefault("people", {})
        self.roles = self.config.setdefault("roles", [])
        self.width = self.config.setdefault("width", 7)
        self.height = self.config.setdefault("height", 7)
        self.repulsion = self.config.setdefault("repulsion", {})

        self.prev_best = None
        self.render_best = False

        if "svg_prefix" in self.config:
            self.render_best = True
            self.svg_prefix = self.config["svg_prefix"]

        self.map_type = self.config.setdefault("map_type", "naive")
        if self.map_type == "hilbert":
            self.map = levis.spatial.HilbertMap(self.width, self.height)
        else:
            self.map = levis.spatial.NaiveMap(self.width, self.height)

        for x in range(0, self.width):
            for y in range(0, self.height):
                self.map.add(x, y)

        self.max_distance = 0.0
        worst_len = spatial.euclidian(0, 0, self.width, self.height)
        assignments = {}

        for _, person in self.people.iteritems():
            if person[1] != SeatingChartGA.EMPTY_ROLE:
                if person[1] in assignments:
                    assignments[person[1]] += 1
                else:
                    assignments[person[1]] = 1

        for role, count in assignments.iteritems():
            edges = (count * (count - 1))
            self.max_distance += edges * worst_len

    def add_arguments(self, parser):
        super(self.__class__, self).add_arguments(parser)
        parser.add_argument("--map-type", choices=["naive", "hilbert"],
                            default="naive",
                            help="Map vectorization strategy")
        parser.add_argument("--svg-prefix",
                            help="Prefix for SVG renderings of the fittest "
                            "chromosomes from each generation. Requires that "
                            "the svgwrite package be installed.")

    def seats_by_role(self, chromosome):
        """Return a dict of ``role -> [seat id]``."""
        seats_role = {}
        for locus, allele in enumerate(chromosome):
            person = self.people[allele]
            if person[1] != SeatingChartGA.EMPTY_ROLE:
                if person[1] not in seats_role:
                    seats_role[person[1]] = []
                seats_role[person[1]].append(self.map.point_at(locus))

        return seats_role

    def score(self, chromosome):
        seats_role = self.seats_by_role(chromosome)

        # Tally attractive score
        attraction = 0.0
        for role, coords in seats_role.iteritems():
            attraction += spatial.total_edge_length(coords)

        # Tally repulsive score
        repulsion = 0.0
        for role, repulsors in self.repulsion.iteritems():
            repulsed = seats_role[role]
            for repulsor in repulsors:
                repulsees = seats_role[repulsor]
                repulsion += spatial.length_to_nearest(repulsed, repulsees)

        return self.max_distance - attraction + repulsion

    def create(self):
        people = list(self.people.keys())
        random.shuffle(people)
        return people

    def mutate(self, chromosome):
        return levis.mutation.swap(chromosome)

    def chromosome_str(self, chromosome):
        w = int(math.floor(math.log(len(self.roles)))) + 1

        txt = str(self.score(chromosome)) + "\n"
        for y in range(0, self.height):
            for x in range(0, self.width):
                locus = self.map.index(x, y)
                person = chromosome[locus]
                role = self.people[person][1]
                role_id = self.roles.index(role)
                txt += str(role_id).rjust(w, " ")
            txt += "\n"

        return txt

    def chromosome_repr(self, chromosome):
        return "%s:%f" % (str(chromosome), self.score(chromosome))

    def post_generate(self):
        """Overloaded ``post_generate()`` hook to enable rendering."""
        super(self.__class__, self).post_generate()

        if self.render_best:
            best = self.scored[0][0]
            if self.prev_best != best:
                self.prev_best = best
                filepath = "%s%i.svg" % (self.svg_prefix, self.iteration)
                self.render(best, filepath)

    def render(self, chromosome, filepath):
        """Render a chromosome to an SVG file."""
        import svgwrite

        margin = 100
        unit = 200
        radius = 50
        pad = 10

        width = (self.width + 1) * unit + margin * 2
        height = (self.height + 1) * unit + margin * 2

        doc = svgwrite.Drawing(filename=filepath, size=(width, height))

        # Color theme to match the talk...
        colors = ["#ff9999", "#9999ff", "#99ff99", "#ffffff"]

        # Fill colors at random
        def channel():
            return int(random.triangular(0, 255, 175))

        while len(colors) < len(self.roles):
            colors.append("#%02x%02x%02x" % (channel(), channel(), channel()))

        # Map row, col to pixels
        def origin(row, col):
            x = row * unit + margin
            y = col * unit + margin
            return (x, y)

        def color_of_group(group):
            idx = self.roles.index(group)
            return colors[idx]

        def color_of_person(person_id):
            group = self.people[person_id][1]
            return color_of_group(group)

        # Render seating assignments
        for seat, person in enumerate(chromosome):
            row, col = self.map.point_at(seat)

            x, y = origin(row, col)
            x, y = (x + radius, y + radius)

            doc.add(doc.circle(
                center=(x, y),
                r=radius,
                stroke_width=8,
                stroke="#000",
                fill=color_of_person(person)
            ))

        doc.save()

# pylint: disable=too-many-locals
def create_data(args):
    """Create problem data and write it to a file as JSON."""

    # Imported here to avoid external dependency just to run the GA
    from faker import Factory

    num_roles = args.setdefault("roles", 5)
    num_people = args.setdefault("people", 40)
    map_width = args.setdefault("width", 7)
    map_height = args.setdefault("height", 7)

    fake = Factory.create()

    roles = [fake.job() for _ in range(0, num_roles)]
    repulsed = {}
    people = {}

    for role in roles:
        if random.random() <= 0.3:
            repulsed[role] = []

            others = list(roles)
            others.remove(role)

            for _ in range(0, random.randint(1, num_roles - 1)):
                other = random.choice(others)
                repulsed[role].append(other)
                others.remove(other)

    for i in range(0, num_people):
        people[i] = (fake.name(), random.choice(roles))

    roles.append("-")
    for i in range(num_people, map_width * map_height):
        people[i] = ("-", "-")

    args.update({
        "roles": roles,
        "people": people,
        "repulsion": repulsed
    })

    configuration.write_file(args)


def main():
    """Main entry point."""

    defaults = {
        "population_size": 100,
        "max_iterations": 100,
        "elitism_pct": 0.01,
        "crossover_operator": "partially_matched",
        "population_file": "population.log",
        "stats_file": "stats.csv"
    }

    description = "Genetic solution for simle seating charts"
    parser = configuration.get_parser(description, "seatingchart.json")
    noop = SeatingChartGA()
    noop.add_arguments(parser)

    parser.add_argument("--generate", action="store_true",
                        help="Generate and store problem data")

    group = parser.add_argument_group("data generation options")

    group.add_argument("--roles", type=int, help="Number of roles")
    group.add_argument("--people", type=int, help="Number of people in seats")
    group.add_argument("--width", type=int, help="Width of map")
    group.add_argument("--height", type=int, help="Height of map")

    args = configuration.read_args(parser)

    if args["generate"]:
        del args["generate"]
        create_data(args)

    else:
        config_file = configuration.read_file(args)
        config = configuration.merge(defaults, config_file, args)

        solver = SeatingChartGA(config)
        solver.solve()
        print(solver.chromosome_str(solver.best()))

if __name__ == "__main__":
    main()
