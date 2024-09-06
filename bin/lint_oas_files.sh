#!/bin/bash

# Run this script from the root of the repository

set -e

COMPONENTS=(
    contactgegevens
    klantinteracties
)

for component in "${COMPONENTS[@]}";
do
    echo "Linting src/openklant/components/$component/openapi.yaml ..."
    spectral lint "src/openklant/components/$component/openapi.yaml"
done
