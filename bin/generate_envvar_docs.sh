#!/bin/bash

# Generates the documentation for environment variables
src/manage.py generate_envvar_docs --file docs/installation/config.rst --exclude-group Celery
