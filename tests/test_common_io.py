
import json
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd
from utils import cleanup_files

from gen3_augur_pyutils.common.io import IO


class TestCommonIO(unittest.TestCase):
    def test_gather_file(self):
        with patch('gen3_augur_pyutils.common.io.walk') as mocked_walk:
            mocked_walk.return_value = [('/foo', [], ['file.txt'])]
            files = list(IO.gather_file('/foo'))
            self.assertEqual(files, ['/foo/file.txt'])

    def test_parse_json(self):
        manifest_obj = [{"object_id": "dg.63D5/67e9eace-5e44-46fa-80ec-71a51437a932",
                         "md5sum": "ac9a2a48c5c9358aea5d332e4aaa6547",
                         "file_name": "MT072688.gb",
                         "file_size": 56513
                         }]
        manifest_frame = pd.DataFrame(manifest_obj)
        (fd, fn) = tempfile.mkstemp()
        try:
            with open(fn, 'wt') as o:
                json.dump(manifest_obj, o)

            res = IO.parse_json(fn)
            self.assertEqual(res, manifest_frame)

        finally:
            cleanup_files(fn)

    def test_write_file(self):
        contents = ['>SARS-CoV-2/human/USA/DC-CDC-1734/2020-MT380728.gb\n',
                    'ATTAAAGGTTTATACCTTCCCAGGTAACAAACCAACCAACTTTCGATCTCTTGTAGATCTGTTCTCTAAACGAACT\n']
        (fd, fn) = tempfile.mkstemp()
        IO.write_file(fn, contents)
        try:
            with open(fn, 'r') as fh:
                results = fh.readlines()
            self.assertEqual(results, contents)
        finally:
            cleanup_files(fn)
