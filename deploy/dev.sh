#!/bin/sh

docker run \
	-v "$(pwd):/usr/src/app" \
	mancalai "$@"
