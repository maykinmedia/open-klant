#!/bin/bash

set -e

exec celery flower --app openklant --workdir src
