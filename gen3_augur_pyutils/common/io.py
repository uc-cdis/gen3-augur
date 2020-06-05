"""IO common utilities
@author: Yilin Xu <yilinxu@uchicago.edu>
"""

import json
from os import walk, path
from typing import List


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
    def write_file(cls, file: str, content: List) -> None:
        """
        Write content into a file
        :param file: output file path
        :param content:
        :return:
        """
        fh = open(file, 'r')
        fh.writelines('%s' % item for item in content)
        fh.close()