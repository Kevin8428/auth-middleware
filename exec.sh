#!/bin/bash
REPO=middleware
VERSION=$1
VERSION=${VERSION:-0.0.1}
docker exec -it $(docker ps -a -q  --filter ancestor=$REPO:$VERSION) /bin/bash