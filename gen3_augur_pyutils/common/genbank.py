"""
Module for parsing genbank metadata
@author: Yilin Xu <yilinxu@uchicago.edu>
"""
import json
from os import walk, path
from gen3_augur_pyutils.common.logger import Logger


class GenBankParser(object):
    """
    Parse genbank format sequencing file, extract metadata save in csv format and fasta file into multi fasta file
    """

    def __init__(self):
        self.logger = Logger.get_logger('GenBankParser')

    def gather_file(self, dir: str) -> None:
        """
        List files in a directory
        :param dir: path of the directory
        :return: files under the directory
        """
        for (dirpath, dirnames, filenames) in walk(dir):
            for item in filenames:
                yield path.join(dirpath, item)

    def