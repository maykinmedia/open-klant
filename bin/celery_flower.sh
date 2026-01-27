#!/bin/bash

# Set defaults for OTEL
export OTEL_SERVICE_NAME="${OTEL_SERVICE_NAME:-openklant-flower}"

exec celery --workdir src -A openklant.celery flower
