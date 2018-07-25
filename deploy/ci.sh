#!/bin/sh

# assume this stuff is already installed
set -e

echo "$(pwd)"

echo "Format!"
autopep8 --verbose --in-place --recursive --aggressive \
    --exclude .git,__pycache__,docs/source/conf.py,old,build,dist,env3 \
    ./
echo "Lint!"
flake8 --exclude .git,__pycache__,docs/source/conf.py,old,build,dist,data,env3
echo "Test!"
pytest --doctest-modules
