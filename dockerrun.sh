#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

conda activate gen3-augur

for name in logs data results; do
    if [[ ! -d "./$name" ]]; then
        echo "ERROR: mount /home/gen3/$name"
        exit 1
    fi
done

export GEN3_API_KEY="${GEN3_API_KEY:-/gen3/credentials.json}"

if [[ ! -f "$GEN3_API_KEY" ]]; then
  echo "ERROR: mount api key to: $GEN3_API_KEY"
  exit 1
fi
bash ./gen3-augur.sh "$@"
exitCode=$?

chmod -R a+rwX ./logs/* ./results/* ./data/*
exit $exitCode
