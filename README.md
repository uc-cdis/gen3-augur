# gen3-augur
Access complete genomic sequence from gen3 data common https://chicagoland.pandemicresponsecommons.org (sequences originated from https://www.ncbi.nlm.nih.gov/genbank/sars-cov-2-seqs/). Create phylogenic tree using augur (https://github.com/nextstrain/augur).

## Installing dependencies
## Using Conda
An `environment.yml` file is provided and can be used to build a virtual environment containing all dependencies. Create the environment using:
```
conda env create -f enviroment.yml
```
Then activate the environment for use:
```
conda activate gen3-augur
```

## Gen3 Client installation, configuration and object data download
### Install gen3-client
Download the latest MacOS X or Linux version of the gen3-client [here](https://github.com/uc-cdis/cdis-data-client/releases/tag/2020.05)

Update the executable gen3-client `/gen3/gen3-client.exe`

Open a terminal window

Add the directory containing the executable to your Path enviroment variable:
```
echo 'export PATH=$PATH:~/.gen3' >> ~/.bash_profile
```
### Config profile
```
gen3-client configure --profile=<profile-name> --cred=gen3/<your credentials.json> --apiendpoint=<api-endpoint-url>
```

### Check data access auth
```
gen3-client auth --profile=<profile-name>
```

### Download object file using manifest.json
```gen3-client download-multiple --profile=<profile-name> --manifest=data/<your manifest.json> --download-path=<your download folder>
```
