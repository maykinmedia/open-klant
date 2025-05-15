#!/bin/bash

# Run this script from the root of the repository

>&2 echo "Check current version"

# Figure out abspath of this script
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")

# wait for required services
${SCRIPTPATH}/wait_for_db.sh

# Check the current version
src/manage.py upgrade_check_version