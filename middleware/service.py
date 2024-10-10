from flask import Flask, render_template

import auth

app = Flask(__name__)

auth.routes(app)

@app.route("/users", methods=["POST"])
@auth.validate_request
def users():
    """
    Dummy endpoint
    """
    return "route finished - /users\n"