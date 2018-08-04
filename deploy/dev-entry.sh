#!/bin/sh

set -e

if [ "--ci" = "$1" ]; then
    shift
    ./deploy/ci.sh
fi

python "$@"
