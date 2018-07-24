#!/bin/sh

DOCKERFILE="Dockerfile.${1:-api}"
echo "Building from $DOCKERFILE"
docker build \
	-t mancalai \
	-f "${DOCKERFILE}" \
	./
