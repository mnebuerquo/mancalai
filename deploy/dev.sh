#!/bin/sh

WHICH="dev"
PORT=""
if [ "$1" = "--api" ]; then
	PORT="-p 5000:5000"
    WHICH="api"
	shift
fi
IMAGE="mancalai-${WHICH}"

docker run \
	-it \
	${PORT} \
	-v "$(pwd):/usr/src/app" \
	"${IMAGE}" "$@"
