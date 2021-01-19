#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

conda activate gen3-augur

for name in logs data results; do
    if [[ ! -d "./$name" ]]; then
        echo "ERROR: mount /home/gen3/$name"
        exit 1
    fi
done

if [[ ! -f /gen3/credentials.json ]]; then
  echo "ERROR: mount /gen3/credentials.json"
  exit 1
fi
cp /gen3/credentials.json config/ || exit 1

bash ./gen3-augur.sh "$@"
exitCode=$?

chmod -R a+rwX ./logs/* ./results/* ./data/*
exit $exitCode
