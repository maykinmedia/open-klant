#!/bin/bash
#
# Dump the current (local database) admin layout to a JSON fixture. This
# overwrites the existing one.
#
# You can load this fixture with:
# $ src/manage.py loaddata src/openklant/fixtures/default_admin_index.json
#
# Run this script from the root of the repository

src/manage.py dumpdata --indent=4 --natural-foreign --natural-primary admin_index.AppGroup admin_index.AppLink > src/openklant/fixtures/default_admin_index.json
