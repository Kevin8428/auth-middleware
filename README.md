# Outline
Handle authentication as middleware. The routing package is extensible. First implementation is using Flask but you can add more like Django. The authentication package is also extensible. First implementation is for JWT but next step could be to build out the bearer tokens package.

This is a work in progress.

A working example of this can be found in [service.py](https://github.com/Kevin8428/auth-middleware/blob/main/service.py). 

You can run services.py from inside a container. See [Development](#development).

Where you previously would handle routing like:

```python
app = Flask(__name__)

@app.route("/user", methods=["GET"])
def users():
    """
    Fetch user info
    """
    # do something
    return Response("{'User':'...'}", status=200)
```

Auth can now be done as middleware like:

```python
app = Flask(__name__)
auth.routes(app)

@app.route("/user", methods=["GET"])
@auth.validate_request
def users():
    """
    Fetch user info
    """
    # do something
    return Response("{'User':'...'}", status=200)
```

This also exposes some APIs to create/verify/delete tokens:
```
endpoint: "/authenticate, methods: ['POST']
endpoint: "/verify, methods: ['POST']
endpoint: "/save, methods: ['POST']
endpoint: "/logout, methods: ['POST']
```

# Development
## build docker image
You can build the image and tag it via arguments:\
`./scripts/build.sh 0.0.2`\
Or you can do so by setting the `VERSION` file content:\
`./scripts/build.sh`
## build image and run container
You can build the image as shown above, and run it as a single command:\
`./scripts/run.sh`\
This will mount middleware_auth. Doing this, you can then start up the flask server using `flask run`.

Then you can inteface with the API:
- `curl -d 'client_id=1&client_secret=something&is_admin=false' http://127.0.0.1:5000/save`
- `curl -d 'client_id=1&client_secret=something&is_admin=false' http://127.0.0.1:5000/authenticate`
- `curl -X POST http://127.0.0.1:5000/verify -H "Authorization: Bearer eyJ0eX..."`
- `curl -X POST http://127.0.0.1:5000/logout -H "Authorization: Bearer eyJ0eX..."`
## connect to running container
`./scripts/exec.sh`
## kill contianer
`./scripts/kill.sh`
## seed db from inside container
`sudo -u postgres psql < middleware/seed.sql`