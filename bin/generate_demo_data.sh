#!/bin/bash
#
# Dump the current data into a fixtures, intended for demo data.
#
# You can load this fixture with:
# $ src/manage.py loaddata src/openklant/fixtures/<file>
#
# Run this script from the root of the repository

OTEL_SDK_DISABLED=True src/manage.py dumpdata --indent=4 --natural-foreign --natural-primary klantinteracties > src/openklant/fixtures/klantinteracties.json
OTEL_SDK_DISABLED=True src/manage.py dumpdata --indent=4 --natural-foreign --natural-primary contactgegevens > src/openklant/fixtures/contactgegevens.json
