#!/bin/bash

# Set defaults for OTEL
export OTEL_SERVICE_NAME="${OTEL_SERVICE_NAME:-openklant-flower}"

exec celery flower --app openklant --workdir src
