FROM conda/c3i-linux-64

RUN useradd -m -s /bin/bash gen3
RUN chown -R gen3: /opt/conda

COPY --chown=gen3:gen3 . /home/gen3
#
# Mount credentials.json as an external dependency
#
#COPY credentials.json /gen3-augur/config/
USER gen3
WORKDIR /home/gen3

RUN conda init bash
RUN conda env create -f environment.yml 
RUN conda activate gen3-augur && python setup.py develop

#
# Mount /gen3/credentials.json
# and mount /home/gen3/logs
# and mount /home/gen3/data
# and mount /home/gen3/results
#
CMD ["bash", "dockerrun.sh", ">>", "logs/run_pipeline.log"]

