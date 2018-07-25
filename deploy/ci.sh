#!/bin/sh

# assume this stuff is already installed
set -e

echo "$(pwd)"

echo "Lint!"
flake8 --exclude .git,__pycache__,docs/source/conf.py,old,build,dist,data,env3
echo "Test!"
pytest --doctest-modules
