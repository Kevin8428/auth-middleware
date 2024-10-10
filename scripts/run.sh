#!/bin/bash
REPO=middleware
VERSION=$1
DEFAULT_VERSION=$(cat VERSION)
VERSION=${VERSION:-$DEFAULT_VERSION}
docker build -t $REPO:$VERSION .

docker run --rm -itd -v ${PWD}:/home $REPO:$VERSION /bin/bash -c "sleep infinity"
docker exec -it $(docker ps -a -q  --filter ancestor=$REPO:$VERSION) /bin/bash

# seed DB
# pg_ctlcluster 10 main start && sudo -u postgres psql
# pg_ctlcluster 10 main start && sudo -u postgres psql < middleware/seed.sql
# psql -d "postgresql://postgres:password@localhost/authdb_dev"

# API interfacing
# flask run
# curl -d 'client_id=1&client_secret=something&is_admin=false' http://127.0.0.1:5000/save
# curl -d 'client_id=1&client_secret=something&is_admin=false' http://127.0.0.1:5000/authenticate
# curl -X POST http://127.0.0.1:5000/verify -H "Authorization: Bearer eyJ0eX..."
# curl -X POST http://127.0.0.1:5000/logout -H "Authorization: Bearer eyJ0eX..."