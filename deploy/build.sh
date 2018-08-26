!/bin/sh

WHICH="${1:-api}"
DOCKERFILE="Dockerfile.${WHICH}"
NAME="mancalai-${WHICH}"
echo "Building from $DOCKERFILE"
docker build \
	-t "${NAME}" \
	-f "${DOCKERFILE}" \
	./
