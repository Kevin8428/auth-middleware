#!/bin/bash
REPO=middleware
VERSION=$1
VERSION=${VERSION:-0.0.1}
docker build -t $REPO:$VERSION .

docker run --rm -itd $REPO:$VERSION /bin/bash -c "sleep infinity"
docker exec -it $(docker ps -a -q  --filter ancestor=$REPO:$VERSION) /bin/bash

# pg_lsclusters
# pg_ctlcluster 10 main start && sudo -u postgres psql

# pg_ctlcluster 10 main start && sudo -u postgres psql < seed.sql

# flask run
# curl -d 'client_id=1&client_secret=something&is_admin=false' http://127.0.0.1:5000/client
# curl -d 'client_id=1&client_secret=something&is_admin=false' http://127.0.0.1:5000/auth
# curl -X POST http://127.0.0.1:5000/verify -H "Authorization: Bearer eyJ0eX..."

# psql -d "postgresql://postgres:password@localhost/authdb_dev"
# psql -d "postgresql://postgres:password@localhost/authdb_dev" -c "select now()"