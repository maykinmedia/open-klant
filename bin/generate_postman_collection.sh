#!/bin/bash

# Run this script from the root of the repository

set -e

COMPONENTS=(
    contactgegevens
    klantinteracties
)

OUTPUT_PATH="./tests/postman/collection.json"

for component in "${COMPONENTS[@]}";
do
    echo "Converting src/openklant/components/$component/openapi.yaml into $OUTPUT_PATH ..."

    openapi2postmanv2 \
        --spec "./src/openklant/components/$component/openapi.yaml" \
        --output $OUTPUT_PATH \
        --pretty
done
