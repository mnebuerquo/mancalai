#!/bin/sh

docker run \
	-it \
	-p 5000 \
	-v "$(pwd):/usr/src/app" \
	mancalai "$@"
