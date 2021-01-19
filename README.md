# gen3-augur
Access complete genomic sequence from gen3 data common https://chicagoland.pandemicresponsecommons.org (sequences originated from https://www.ncbi.nlm.nih.gov/genbank/sars-cov-2-seqs/). Create phylogenic tree using augur https://github.com/uc-cdis/augur (modified from https://github.com/nextstrain/augur).

## Download credentials.json from data common and copy the credentials.json into config folder
```
copy credentials.json gen3-augur/config/credentials.json
```

## Installing dependencies
## Using Conda
An `environment.yml` file is provided and can be used to build a virtual environment containing all dependencies. Create the environment using:
```
conda env create -f environment.yml
```
Then activate the environment for use:
```
conda activate gen3-augur
```

Install the gen3-augur package for use:
```
python setup.py develop
```

## Run shell script
```
cd gen3-augur
mkdir data
mkdir logs
mkdir results
mkdir auspice
bash gen3-augur.sh >> logs/run_pipeline.log
```
