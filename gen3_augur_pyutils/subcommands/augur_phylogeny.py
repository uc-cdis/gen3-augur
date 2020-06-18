augur filter --sequences sequences.fasta --metadata ../data/metadata.csv --output filtered.fasta
augur align --sequences covid19-0609.fasta --reference-sequence sequence.gb --output result/aligned.fasta --fill-gaps --nthreads auto
augur tree --alignment results/aligned.fasta --output results/tree_raw.nwk --nthreads auto
augur refine --tree tree_raw.nwk --alignment aligned.fasta --metadata ../covid19-0609.csv --output-tree tree.nwk --output-node-data branch_lengths.json --timetree --coalescent opt --date-confidence --date-inference marginal --clock-filter-iqd 4
augur traits --tree tree.nwk --metadata ../data/test-genbank.csv --output traits.json --columns country --confidence
augur ancestral --tree tree.nwk --alignment aligned.fasta --output-node-data nt_muts.json --inference joint
augur translate --tree tree.nwk --ancestral-sequences nt_muts.json --reference-sequence ../config/sequence.gb --output aa_muts.json