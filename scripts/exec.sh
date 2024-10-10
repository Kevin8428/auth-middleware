#!/bin/bash
REPO=middleware
VERSION=$1
DEFAULT_VERSION=$(cat VERSION)
VERSION=${VERSION:-$DEFAULT_VERSION}
docker exec -it $(docker ps -a -q  --filter ancestor=$REPO:$VERSION) /bin/bash