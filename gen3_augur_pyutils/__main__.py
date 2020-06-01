"""
Main entrypoint for gen3-augur_pyutils.
"""

import argparse
import datetime
import sys

from gen3_augur_pyutils.common.logger import Logger
from gen3_augur_pyutils.subcommands import ParseGenbank


def main(args=None, extra_subparser=None):
    """
    The main method for gen3-augur-pyutils.
    :param args:
    :param extra_subparser:
    :return:
    """
    # Setup logger
    Logger.setup_root_logger()

    logger = Logger.get_logger('main')

    # Get args
    p = argparse.ArgumentParser('Gen3 Augur Utils')
    subparsers = p.add_subparsers(dest='subcommad')
    subparsers.required = True

    ParseGenbank.add(subparsers=subparsers)
    if extra_subparser:
        extra_subparser.add(subparsers=subparsers)

    options = p.parse_args(args)

    # Run
    options.func(options)

    # Finish


if __name__ == "__main__":
    main()
