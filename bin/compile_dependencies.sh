#!/bin/sh
#
# Compile the dependencies for production, CI and development.
#
# Usage, in the root of the project:
#
#     ./bin/compile_dependencies.sh
#
# Any extra flags/arguments passed to this wrapper script are passed down to uv pip compile.
# E.g. to update a package:
#
#     ./bin/compile_dependencies.sh --upgrade-package django
set -ex

command -v uv || (echo "uv not found on PATH. Install it https://astral.sh/uv" >&2 && exit 1)

root_dir=$(git rev-parse --show-toplevel)

export UV_CUSTOM_COMPILE_COMMAND="./bin/compile_dependencies.sh"

# Base (& prod) deps
uv pip compile \
    --output-file "$root_dir/requirements/base.txt" \
    "$@" \
    "$root_dir/requirements/base.in"

# Dependencies for testing
uv pip compile \
    --output-file "$root_dir/requirements/ci.txt" \
    "$@" \
    "$root_dir/requirements/test-tools.in" \
    "$root_dir/requirements/docs.in"

# Dev depedencies - exact same set as CI + some extra tooling
uv pip compile \
    --output-file "$root_dir/requirements/dev.txt" \
    "$@" \
    "$root_dir/requirements/dev.in"
