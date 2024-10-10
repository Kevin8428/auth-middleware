#!/bin/bash
REPO=middleware
VERSION=$1
DEFAULT_VERSION=$(cat VERSION)
VERSION=${VERSION:-$DEFAULT_VERSION}
docker kill $(docker ps -a -q  --filter ancestor=$REPO:$VERSION)