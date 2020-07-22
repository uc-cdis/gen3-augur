FROM conda/c3i-linux-64

COPY ./gen3-augur /gen3-augur
COPY ./gen3-augur.sh /gen3-augur.sh
COPY credentials.json /gen3-augur/config/
WORKDIR /gen3-augur

RUN conda env create -f environment.yml
RUN conda activate augur
RUN python setup.py develop


CMD ["echo y|", "bash", "gen3-augur.sh"]
