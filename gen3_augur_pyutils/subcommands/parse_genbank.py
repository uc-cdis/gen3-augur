"""
Extract patient metadata, viral metadata and viral sequence from GenBank .gb file

@author: Yilin Xu <yilinxu@uchicago.edu>
"""
from Bio import SeqIO
from os import walk, path
import pandas as pd
from typing import Tuple, List
import json

from gen3_augur_pyutils.common.logger import Logger
from gen3_augur_pyutils.common.io import IO
from gen3_augur_pyutils.common.types import ArgParserT, NamespaceT, DataFrameT, LoggerT
from gen3_augur_pyutils.subcommands import Subcommand


class ParseGenBank(Subcommand):
    @classmethod
    def __add_arguments__(cls, parser: ArgParserT):
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
        paths = IO.gather_file(options.rawfoler)

        # Parse GenBank files

    @classmethod
    def parse_bg(cls, gbfile: str, logger: LoggerT) -> Tuple[DataFrameT, List]:
        """
        Extract metadata and save sequence in fasta format with strain as header
        :param file: genbank file path
        :return: metadata dict
        """
        gb_record = SeqIO.read(open(gbfile, 'r'), 'genbank')
        output_handle = open(fasta, "a")
        try:
            strain = gb_record.features[0].qualifiers['isolate'][0]
        except KeyError:
            logger.error("%s doesn't have isolate information, use source to code strain", gbfile)
        else:
            strain = gb_record.annotations['source']
        output_handle.write(">%s\n%s\n" % (
            strain,
            gb_record.seq
        ))
        metadata = {key: value[0] for key, value in gb_record.features[0].qualifiers.items() if key != "resource"}
        metadata['strain'] = strain
        try:
            metadata['country'] = metadata['country'].split(':')[0]
        except:
            pass
        metadata['file'] = path.basename(file)
        metadata['accession'] = gb_record.name
        return (metadata)


def main():
    """
    Parse input parameters to prepare metadata for running Augur
    :param args:
    :return:
    """
    parse_args()
    files = gather_files(args.rawfolder)
    metadata = list(map(parse_bg, files))
    metadata_df = pd.DataFrame(metadata)
    manifest = parse_manifest(args.manifest)
    merge_manifest = metadata_df.merge(manifest, how='inner', left_on='file', right_on='file_name')
    merge_manifest.to_csv(args.metadata, index=False)


if __name__ == "__main__":
    main()
