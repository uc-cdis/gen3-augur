#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"

conda activate gen3-augur

for name in logs data results auspice; do
    if [[ ! -d "./$name" ]]; then
        echo "ERROR: mount /home/gen3/$name"
        exit 1
    fi
done

export GEN3_API_KEY="${GEN3_API_KEY:-/gen3/credentials.json}"

if [[ ! -z "$GEN3_API_ENV" ]]; then
    echo "$GEN3_API_ENV" | base64 -d > $GEN3_API_KEY
fi

if [[ ! -f "$GEN3_API_KEY" ]]; then
  echo "ERROR: mount api key to: $GEN3_API_KEY"
  exit 1
fi
bash ./gen3-augur.sh "$@"
exitCode=$?

for name in logs data results auspice; do
    find "./$name" -type f -exec chmod a+rwX '{}' ';'
done

# Upload resulting auspice file to s3
if [[ ! -z "$S3_BUCKET"  ]]; then
    for file in auspice/*.json; do
        aws s3 cp $file s3://$S3_BUCKET/
    done
fi

exit $exitCode