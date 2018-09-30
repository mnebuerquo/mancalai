#!/bin/sh

IMAGE="mancalai-api"

docker run \
	-d \
	-p 5000 \
	--log-opt max-size=10m \
	${IMAGE}
