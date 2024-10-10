#!/bin/bash
REPO=middleware
VERSION=$1
VERSION=${VERSION:-0.0.1}
docker build -t $REPO:$VERSION .

# docker run --rm -itd -v /Users/cargometrics/personal/middleware_auth/middleware:/app/middleware middleware:0.0.1 /bin/bash -c "sleep infinity"
# docker run --rm -itd middleware:0.0.1 /bin/bash -c "sleep infinity"

docker run --rm -itd -v ${PWD}:/home $REPO:$VERSION /bin/bash -c "sleep infinity"
docker exec -it $(docker ps -a -q  --filter ancestor=$REPO:$VERSION) /bin/bash




# pg_lsclusters
# pg_ctlcluster 10 main start && sudo -u postgres psql
# pg_ctlcluster 10 main start && sudo -u postgres psql < seed.sql
# psql -d "postgresql://postgres:password@localhost/authdb_dev"


# flask run
# curl -d 'client_id=1&client_secret=something&is_admin=false' http://127.0.0.1:5000/client
# curl -d 'client_id=1&client_secret=something&is_admin=false' http://127.0.0.1:5000/auth
# curl -X POST http://127.0.0.1:5000/verify -H "Authorization: Bearer eyJ0eX..."
# curl -X POST http://127.0.0.1:5000/logout -H "Authorization: Bearer eyJ0eX..."


# psql -d "postgresql://postgres:password@localhost/authdb_dev" -c "select now()"
# curl -d 'client_id=1&client_secret=something&is_admin=false' http://127.0.0.1:5000/users

# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwic3ViIjoiMSIsImlzQWRtaW4iOiIzZmM5YjY4OTQ1OWQ3MzhmOGM4OGEzYTQ4YWE5ZTMzNTQyMDE2YjdhNDA1MmUwMDFhYWE1MzZmY2E3NDgxM2NiIiwiZXhwIjoxNzI4NTgzNjk0fQ.amb8s4odfjTuLZHV-bCIo9O4cpI6BWVapFuQA7j0B5c