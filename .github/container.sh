#!/bin/bash

set -ex

TAG="$(git rev-parse --short HEAD)"
# GIT_VERSION="$TAG $(date +%Y/%m/%d)"
# echo $GIT_VERSION > kvirt/version/git

podman build -t quay.io/karmab/glpic:latest .
podman login -u $QUAY_USERNAME -p $QUAY_PASSWORD quay.io
podman push quay.io/karmab/glpic:latest
