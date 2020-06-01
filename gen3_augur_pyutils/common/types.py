"""Module for defining types for type annotations.
Adapted from Kyle Hernandez's work (https://github.com/COV-IRT/dmwg-data-pyutils/).
@author: Yilin Xu <yilinxu@uchicago.edu>
"""
from typing import NewType
from argparse import ArgumentParser, Namespace
from logging import Logger

# ArgParser types and Namespace types
ArgParserT = NewType("ArgParserT", ArgumentParser)
NamespaceT = NewType("NamespaceT", Namespace)

# Logger types
LoggerT = NewType("LoggerT", Logger)
