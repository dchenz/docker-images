#!/bin/bash

set -e

PYTHON_BASE=3.12-alpine
JUPYTER_VERSION=7.4.2
COMMIT_HASH=$(git rev-parse --short HEAD)

IMAGE_NAME=dchenz/jupyter-notebook:$PYTHON_BASE-$JUPYTER_VERSION-$COMMIT_HASH

docker build src \
    -f ./Dockerfile \
    -t $IMAGE_NAME \
    --build-arg PYTHON_BASE=$PYTHON_BASE \
    --build-arg JUPYTER_VERSION=$JUPYTER_VERSION

docker push $IMAGE_NAME

docker rmi $IMAGE_NAME
