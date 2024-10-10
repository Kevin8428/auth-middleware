from flask import Flask, render_template

import routes

app = Flask(__name__)

@app.errorhandler(403)
def auth_denied(error):
    error=['auth denied']
    return render_template('errors.html', error=error), 403

@app.route("/users", methods=["POST"])
@routes.validate_request
def users():
    """
    Dummy endpoint
    """
    return "route finished - /users\n"