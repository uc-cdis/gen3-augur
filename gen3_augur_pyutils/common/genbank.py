"""
Module for parsing genbank metadata
@author: Yilin Xu <yilinxu@uchicago.edu>
"""
import json
from os import walk, path
import pandas as pd
from gen3_augur_pyutils.common.logger import Logger
from gen3_augur_pyutils.common.types import DataFrameT


class GenBankParser(object):
    """
    Parse genbank format sequencing file, extract metadata save in csv format and fasta file as multi fasta file
    """

    def __init__(self, logfile: str) -> None:

        self.logger = Logger.get_logger(logfile)




