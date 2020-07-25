FROM conda/c3i-linux-64

COPY ./gen3-augur /gen3-augur
COPY credentials.json /gen3-augur/config/
WORKDIR /gen3-augur

RUN conda env create -f environment.yml
RUN conda activate augur
RUN python setup.py develop


CMD ["bash", "gen3-augur.sh", ">>", "logs/run_pipeline.log"]
