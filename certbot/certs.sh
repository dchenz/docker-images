#!/bin/bash

set -e # Exit immediately if a command exits with a non-zero status

imageName=docker.io/dchenz/certbot:3.3.0
containerName=certbot-$(date +%s)

docker run -it \
    --name $containerName \
    $imageName \
    certonly \
    -v \
    --manual \
    --preferred-challenges dns

docker export $containerName | tar -xf - etc/letsencrypt

echo -e "\nCertificates exported from Docker container:\n"
find etc -name *.pem -type f
