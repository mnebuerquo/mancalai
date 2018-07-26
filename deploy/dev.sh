#!/bin/sh

PORT=""
if [ "$1" = "--api" ]; then
	PORT="-p 5000:5000"
	shift
fi

docker run \
	-it \
	${PORT} \
	-v "$(pwd):/usr/src/app" \
	mancalai "$@"
