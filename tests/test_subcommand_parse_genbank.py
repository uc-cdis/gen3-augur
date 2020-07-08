"""Test gen3_augur_pyutils.subcommands.parse_genbank module"""
import unittest
from pathlib import Path

from gen3_augur_pyutils.common.io import IO
from gen3_augur_pyutils.subcommands import ParseGenBank


class TestSubcommandParseGenbank(unittest.TestCase):
    def test_parse_bg(self):
        dir_path = Path(__file__).resolve().parents[2]
        with IO.change_dir(dir_path):
            self.assertIsNone(ParseGenBank.parse_bg('data/test-genbank-rawbg/EU371562.gb'))
            (MT027062.meta, MT027062.seq) = ParseGenBank.parse_bg('data/test-genbank-rawbg/MT027062.gb')
            self.assertEqual(MT027062.meta['strain'], '2019-nCoV/USA-CA3/2020-MT027062.gb')

if __name__ == '__main__':
    unittest.main()