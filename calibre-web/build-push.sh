#!/bin/bash

set -e

CALIBRE_VERSION=0.6.24
COMMIT_HASH=$(git rev-parse --short HEAD)

IMAGE_NAME=dchenz/calibre-web:$CALIBRE_VERSION-$COMMIT_HASH

docker build . \
    -f ./Dockerfile \
    -t $IMAGE_NAME \
    --build-arg CALIBRE_VERSION=$CALIBRE_VERSION

docker push $IMAGE_NAME

docker rmi $IMAGE_NAME
