#!/bin/bash

# setup initial configuration using environment variables
# Run this script from the root of the repository

set -e

# Set defaults for OTEL
export OTEL_SERVICE_NAME="${OTEL_SERVICE_NAME:-openklant-setup-configuration}"


if [[ "${RUN_SETUP_CONFIG,,}" =~ ^(true|1|yes)$ ]]; then
    # wait for required services
    /wait_for_db.sh

    src/manage.py migrate
    src/manage.py setup_configuration --yaml-file setup_configuration/data.yaml
fi
