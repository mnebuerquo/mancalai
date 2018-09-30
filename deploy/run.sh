#!/bin/sh

WHICH="${1:-api}"
IMAGE="mancalai-${WHICH}"

docker run \
	-p 5000 \
	${IMAGE} "$@"
