"""IO common utilities
@author: Yilin Xu <yilinxu@uchicago.edu>
"""

import json
from contextlib import contextmanager
from os import walk, path, chdir, getcwd
from typing import List

import pandas as pd

from gen3_augur_pyutils.common.types import DataFrameT


class IO(object):
    @staticmethod
    def gather_file(dir: str) -> None:
        """
        :param dir: path of the directory
        :return: files path under the directory
        """
        for (dirpath, dirnames, filenames) in walk(dir):
            for item in filenames:
                yield path.join(dirpath, item)

    @staticmethod
    def parse_json(file: str) -> DataFrameT:
        """
        Extract key value pairs in json file
        :param file: file path
        :return: DataFrame key value pairs from json file
        """
        fh = open(file, 'r')
        items = json.load(fh)
        fh.close()
        items_df = pd.DataFrame(items)
        return items_df

    @staticmethod
    def df_merge_columns(file: str, columns: List) -> DataFrameT:
        """
        Parse csv file and merge columns
        :param file:
        :return: DataFrameT
        """
        df = pd.read_csv(file, header=True)
        df['combine'] = df[columns].apply(lambda x: ','.join(x), axis=1)
        return df

    @staticmethod
    def write_file(file: str, content: List) -> None:
        """
        Write content into a file
        :param file: output file path
        :param content:
        :return:
        """
        fh = open(file, 'w')
        fh.writelines('%s' % item for item in content)
        fh.close()

    @staticmethod
    @contextmanager
    def change_dir(destination):
        """
        Change to destination to do task and change back to the original directory
        :param destination: Target path performing a task
        :return: None
        """
        try:
            cwd = getcwd()
            chdir(destination)
            yield
        finally:
            chdir(cwd)
