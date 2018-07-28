#!/bin/sh

set -e

if [ "--ci" = "$1" ]; then
    ./deploy/ci.sh
fi

python "$@"
