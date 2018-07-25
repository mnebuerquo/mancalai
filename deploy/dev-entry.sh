#!/bin/sh

set -e

./deploy/ci.sh

python "$@"
