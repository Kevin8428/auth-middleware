#!/bin/bash
REPO=middleware
VERSION=$1
VERSION=${VERSION:-0.0.1}
docker kill $(docker ps -a -q  --filter ancestor=$REPO:$VERSION)