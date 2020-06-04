"""
Module for parsing genbank metadata
@author: Yilin Xu <yilinxu@uchicago.edu>
"""
from os import path
from gen3_augur_pyutils.common.logger import Logger
from Bio import SeqIO

class GenBankParser(object):
    """
    Parse genbank format sequencing file, extract metadata save in csv format and fasta file as multi fasta file
    """

    def __init__(self, logfile: str) -> None:

        self.logger = Logger.get_logger(logfile)

    def parse_bg(self, file):
        """
        Extract metadata and save sequence in fasta format with strain as header
        :param file: genbank file path
        :return: metadata dict and fasta list
        """
        gb_record = SeqIO.read(open(file, 'r'), 'genbank')
        try:
            strain = gb_record.features[0].qualifiers['isolate'][0]
        except:
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



