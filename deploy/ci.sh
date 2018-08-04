#!/bin/sh

# assume this stuff is already installed
set -e

echo "$(pwd)"

EXCLUDE=".git,.pytest_cache,__pycache__,docs/source/conf.py,old,build,dist,env3,data,training,presentation,deploy,webui"
echo "Format!"
autopep8 --verbose --in-place --recursive --aggressive --exclude "${EXCLUDE}" .
echo "Lint!"
flake8 --exclude "${EXCLUDE}"
echo "Test!"
pytest --doctest-modules --ignore=webui
