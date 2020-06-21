"""
Extract patient metadata, viral metadata and viral sequence from GenBank .gb file

@author: Yilin Xu <yilinxu@uchicago.edu>
"""
import re
from datetime import datetime
from itertools import repeat
from os import path
from typing import Tuple, Dict

import pandas as pd
from Bio import SeqIO

from gen3_augur_pyutils.common.io import IO
from gen3_augur_pyutils.common.logger import Logger
from gen3_augur_pyutils.common.types import ArgParserT, NamespaceT, LoggerT
from gen3_augur_pyutils.subcommands import Subcommand


class ParseGenBank(Subcommand):
    @classmethod
    def __add_arguments__(cls, parser: ArgParserT) -> None:
        """
        Add the arguments to the parser
        :param parser: parsed arguments
        :return: None
        """
        parser.add_argument('--rawfolder', required=True, help='path of the folder having raw genbank sequence files')
        parser.add_argument('--manifest', required=True,
                            help='path of manifest file having object data describing files')
        parser.add_argument('--fasta', required=True, help='path of output fasta file')
        parser.add_argument('--metadata', required=True, help='path of output metadata file')
        parser.add_argument('--logfile', required=True, help='path of the log file')

    @classmethod
    def parse_bg(cls, gbfile: str, logger: LoggerT) -> Tuple[Dict[str, str], str]:
        """
        Extract metadata and save sequence in fasta format with strain as header
        :param file: genbank file path
        :return: metadata dict and seq string
        """
        gb_record = SeqIO.read(open(gbfile, 'r'), 'genbank')
        bf = path.basename(gbfile)
        metadata = {key: value[0] for key, value in gb_record.features[0].qualifiers.items() if key != "resource"}
        if metadata['organism'] != 'Severe acute respiratory syndrome coronavirus 2':
            logger.info('%s is not Covid19 sample, remove the file', bf)
            return None
        try:
            metadata['country'] = metadata['country'].split(':')[0]
        except KeyError:
            logger.error("No location information, remove %s", bf)
            return None
        try:
            strain = gb_record.features[0].qualifiers['strain'][0]
        except KeyError:
            try:
                strain = gb_record.features[0].qualifiers['isolate'][0]
            except KeyError:
                strain = gb_record.annotations['source']
        strain = re.sub(' ', '/', strain)
        strain = strain + "-" + bf
        seq = '>' + strain + "\n" + gb_record.seq + "\n"
        metadata['strain'] = strain
        metadata['file'] = bf
        metadata['accession'] = gb_record.name
        date = metadata['collection_date']
        try:
            date = datetime.strptime(date, '%d-%M-%Y')
        except Exception as e:
            logger.error(f'{bf} date error:{e}')
            date = datetime.strptime(date, '%Y-%m')
        finally:
            metadata['collection_date'] = date.date()
        return (metadata, seq)

    @classmethod
    def main(cls, options: NamespaceT) -> None:
        """
        Entrypoint for ParseGeneBank
        :param options:
        :return:
        """
        logger = Logger.get_logger(cls.__tool_name__(), options.logfile)
        logger.info(cls.__get_description__())

        # Parse Manifest file
        manifest = IO.parse_json(options.manifest)
        logger.info("Parse Manifest file %s", options.manifest)

        # Get GenBank file paths
        paths = IO.gather_file(options.rawfolder)

        # Parse GenBank files
        res_list = list(map(cls.parse_bg, paths, repeat(logger)))
        paths = IO.gather_file(options.rawfolder)

        # Parse GenBank files
        res_list = list(map(cls.parse_bg, paths, repeat(logger)))
        metadata = [x[0] for x in res_list if x is not None]
        seq = [x[1] for x in res_list if x is not None]
        metadata_df = pd.DataFrame(metadata)
        metadata_df.rename(columns={'collection_date': 'date'}, inplace=True)

        # Write sequence into a multifastq file
        IO.write_file(options.fasta, seq)

        # Merge Manifest and Metadata
        merge_manifest = metadata_df.merge(manifest, how='inner', left_on='file', right_on='file_name')
        merge_manifest.rename(columns={'object_id': 'guid'}, inplace=True)

        # Write merge dataframe
        merge_manifest.to_csv(options.metadata, index=False)
