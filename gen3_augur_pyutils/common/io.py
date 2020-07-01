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
    @classmethod
    def gather_file(cls, dir: str) -> None:
        """
        :param dir: path of the directory
        :return: files path under the directory
        """
        for (dirpath, dirnames, filenames) in walk(dir):
            for item in filenames:
                yield path.join(dirpath, item)

    @classmethod
    def parse_json(cls, file: str) -> DataFrameT:
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

    @classmethod
    def df_merge_columns(cls, file: str, columns: List) -> DataFrameT:
        """
        Parse csv file and merge columns
        :param file:
        :return: DataFrameT
        """
        df = pd.read_csv(file, header=True)
        df['combine'] = df[columns].apply(lambda x: ','.join(x), axis=1)
        return df

    @classmethod
    def write_file(cls, file: str, content: List) -> None:
        """
        Write content into a file
        :param file: output file path
        :param content:
        :return:
        """
        fh = open(file, 'w')
        fh.writelines('%s' % item for item in content)
        fh.close()

    @contextmanager
    def change_dir(self, destination):
        try:
            cwd = getcwd()
            chdir(destination)
            yield
        finally:
            chdir(cwd)
