import os

from middleware import auth
from middleware import routers

auth_type = os.getenv('AUTH_TYPE', 'jwt')
auth_client = auth.client(auth_type)

router_type = os.getenv('ROUTER_TYPE', 'flask')
router = routers.client(router_type, auth_client=auth_client)

# TODO: export FLASK_APP so this can be removed and run @router.client.route()
app=router.client

@app.route("/users", methods=["POST"])
@router.verify_middleware
def users():
    """
    Get users
    """
    return "route finished - /users\n"