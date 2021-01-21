# gen3-augur

Access complete genomic sequence from gen3 data common https://chicagoland.pandemicresponsecommons.org (sequences originated from https://www.ncbi.nlm.nih.gov/genbank/sars-cov-2-seqs/). Create phylogenic tree using augur https://github.com/uc-cdis/augur (modified from https://github.com/nextstrain/augur).

## Set GEN3_API_KEY

```
download credentials.json from commons
copy credentials.json $HOME/.gen3/credentials.json
export GEN3_API_KEY="$HOME/.gen3/credentials.json"
```

## Install gen3-client

* Download and unzip from: https://github.com/uc-cdis/cdis-data-client
* install `gen3-client` under the `gen3/` folder

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

### Run shell script
```
cd gen3-augur
mkdir data
mkdir logs
mkdir results
mkdir auspice
bash gen3-augur.sh >> logs/run_pipeline.log
```

## docker run

```
(
    IMAGE=quay.io/cdis/gen3-augur:fix_docker2;
    docker pull $IMAGE \
    && docker run --env https_proxy=http://cloud-proxy.internal.io:3128 --env http_proxy=http://cloud-proxy.internal.io:3128 --env no_proxy=localhost,127.0.0.1,169.254.169.254,.internal.io,logs.us-east-1.amazonaws.com,kibana.planx-pla.net -v $(pwd)/logs:/home/gen3/logs -v $(pwd)/results:/home/gen3/results -v $(pwd)/data:/home/gen3/data -v $(pwd)/Gen3Secrets:/gen3 --rm --name=augurbatch $IMAGE
)
```
