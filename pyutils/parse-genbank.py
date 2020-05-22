from Bio import SeqIO
from os import walk, path
import argparse
import pandas as pd
import json


def parse_args():
    """
    Parse arguments
    :return: parsed arguments
    """
    global args
    parser = argparse.ArgumentParser(
        description='Crate metadata.tsv and sequence.fasta from raw files in genbank format')
    parser.add_argument('--rawfolder', required=True, help='path of the folder having raw genbank sequence files')
    parser.add_argument('--manifest', required=True, help='path of manifest file having attributes describing files')
    parser.add_argument('--fasta', required=True, help='path of output fasta file')
    parser.add_argument('--metadata', required=True, help='path of output metadata file')
    args = parser.parse_args()
    return args


def gather_files(folder):
    """
    List files in a folder
    :param folder:
    :return: files in the folder
    """
    for (dirpath, dirnames, filenames) in walk(folder):
        for item in filenames:
            yield path.join(dirpath, item)


def parse_manifest(file):
    """
    Extract GUID, file name, file size and md5sum
    :param file:
    :return:
    """
    with open(file, 'r') as fh:
        manifest = json.load(fh)
        manifest_df = pd.DataFrame(manifest)
        return manifest_df


def parse_bg(file):
    """
    Extract metadata and save sequence in fasta format with strain as header
    :param file: genbank file path
    :return: metadata dict
    """
    gb_record = SeqIO.read(open(file, 'r'), 'genbank')
    output_handle = open(args.fasta, "a")
    strain = gb_record.features[0].qualifiers['isolate'][0]
    output_handle.write(">%s\n%s\n" % (
        strain,
        gb_record.seq
    ))
    metadata = {key: value[0] for key, value in gb_record.features[0].qualifiers.items() if key != "resource"}
    metadata['strain'] = strain
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
    merge_manifest = metadata_df.merge(manifest, how='left', left_on='file', right_on='file_name')
    merge_manifest.to_csv(args.metadata, index=False)


if __name__ == "__main__":
    main()
