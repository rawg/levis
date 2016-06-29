"""Configuration utilities.

"""

import argparse
import json
from os import getcwd

DATA_FILE = getcwd() + "/problem.json"
"""Default path to a configuration file."""

def get_parser(description, datafile=DATA_FILE):
    """Get an argument parser with common arguments created."""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("--data-file", "-df", default=datafile,
                        help="Path to the data file")

    return parser


def merge(root_config, *args):
    """Merge two configuration dictionaries together."""

    root = root_config.copy()

    for arg in args:
        clean = {k: v for k, v in arg.iteritems() if v is not None}
        root.update(clean)
    return root

def read_args(parser):
    """Return a ``dict`` of arguments from an ``ArgumentParser``.

    Parses arguments using ``parser.parse_args()`` and returns a ``dict`` of
    all arguments that are not ``None``.
    """
    args = parser.parse_args()
    args_dict = vars(args)
    return {k: v for k, v in args_dict.iteritems() if v is not None}


def write_file(config):
    """Writes configuration to a JSON file.

    The filepath is read from the "data_file" key.
    """
    data = json.dumps(config, indent=4, separators=(',', ': '))
    with open(config["data_file"], "w") as handle:
        handle.write(data)


def read_file(args):
    """Read configuration from a JSON file.

    The filepath is read from the "data_file" key.
    """
    if "data_file" in args:
        data_file = args["data_file"]
    else:
        data_file = DATA_FILE

    with open(data_file, "r") as infile:
        raw = infile.read()
        config = json.loads(raw)
        return config
