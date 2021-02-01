#!/bin/sh
set -ex

today=$(date +'%m%d%y')

# Query manifest
echo "Query Manifest"
expect_files=$(gen3-augur Gen3Query --url https://chicagoland.pandemicresponsecommons.org/ --type genomic_file --fields file_name,file_size,md5sum,object_id --filter project_id --value "Walder-SIU-SARS-CoV2" --format json --logfile genomic_manifest_${today})

# Setup up gen3-client
echo "Setup gen3-client"
./gen3/gen3-client configure --profile=covid19 --cred=config/credentials.json --apiendpoint=https://chicagoland.pandemicresponsecommons.org/ &&

# Download object files
echo "Download object files"
mkdir -p data/covid19_${today}_rawbg
exist_files=$(ls data/covid19_${today}_rawbg|wc -l)

while [ ${exist_files} -lt ${expect_files} ];
do
    echo ${expect_files}
    echo ${exist_files}
    echo y|bash download.sh
    exist_files=$(ls data/covid19_${today}_rawbg|wc -l)
done;

# Merge multiple fasta into one fasta file
echo "Merge fasta file"
cat data/covid19_${today}_rawbg/*.fasta >> data/covid19_${today}.fasta

# Query metadata, generate metadata.csv
echo "Query Metadata"
expect_files=$(gen3-augur Gen3Query --url https://chicagoland.pandemicresponsecommons.org/ --type genomic_file --fields location,continent,country_region,province_state,county,host,organism,sample_type,isolation_source,isolate,collection_date,originating_lab,submitting_lab,submitting_lab_PI --filter project_id --value "Walder-SIU-SARS-CoV2" --format csv --logfile sample_manifest_${today})

# Run Augur pipeline
# Filter
echo "Filter fasta files"
augur filter --sequences data/covid19_${today}.fasta --metadata data/sample_${today}_manifest.csv --output results/covid19_${today}_filter.fasta &&

# Alignment(default mafft tool)
echo "Run alignment"
augur align --sequences results/covid19_${today}_filter.fasta --reference-sequence config/sequence.gb --output results/covid19_${today}_aligned.fasta --fill-gaps --nthreads auto &&

# Create raw tree
echo "Create raw tree"
augur tree --alignment results/covid19_${today}_aligned.fasta --output results/covid19_${today}_tree_raw.nwk --nthreads auto &&

# Refine tree
echo "Refine tree"
augur refine --tree results/covid19_${today}_tree_raw.nwk --alignment results/covid19_${today}_aligned.fasta --metadata data/sample_${today}_manifest.csv --output-tree results/covid19_${today}_tree.nwk --output-node-data results/covid19_${today}_branch_lengths.json --timetree --coalescent opt --date-confidence --date-inference marginal --clock-filter-iqd 4 &&

# Refine traits
echo "Refine traits"
augur traits --tree results/covid19_${today}_tree.nwk --metadata data/sample_${today}_manifest.csv --output results/covid19_${today}_traits.json --columns location --confidence &&

# Ancestry Inference
echo "Infer ancestry"
augur ancestral --tree results/covid19_${today}_tree.nwk --alignment results/covid19_${today}_aligned.fasta --output-node-data results/covid19_${today}_nt_muts.json --inference joint &&

# Mutation Translate
echo "Mutation translation"
augur translate --tree results/covid19_${today}_tree.nwk --ancestral-sequences results/covid19_${today}_nt_muts.json --reference-sequence config/sequence.gb --output results/covid19_${today}_aa_muts.json &&

# Labeling clades as specified in config/clades.tsv
augur clades --tree results/covid19_${today}_tree.nwk --mutations results/covid19_${today}_nt_muts.json results/covid19_${today}_aa_muts.json --clades config/clades.tsv --output results/covid19_${today}_clade.json


# Export json
echo "Export json"
augur export v2 --tree results/covid19_${today}_tree.nwk --metadata data/sample_${today}_manifest.csv--node-data results/covid19_${today}_branch_lengths.json results/covid19_${today}_traits.json results/covid19_${today}_nt_muts.json results/covid19_${today}_aa_muts.json results/covid19_${today}_clade.json --colors config/color_schemes.tsv --lat-longs config/latitude_longitude.tsv --auspice-config config/auspice_config.json --output auspice/covid19_${today}.json
