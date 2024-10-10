from flask import request, abort, render_template
import json
import os
import hashlib

from functools import wraps
import models


def validate_request(f):
    """docs"""
    wraps(f)
    def decorated_function(*args, **kwargs):
        verified = _verify(request)
        print('verified: ', verified)
        if not verified:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def logout():
    """
    Add token to `blocked` table
    """
    token = request.form.get("token")
    status = models.block(token)
    return {'success': status}


def _verify(req):
    """
    Verify JWT - decoode token with AUTHSECRET
    """
    token = req.headers.get('authorization').replace('Bearer ', '').strip()
    verified = models.verify(token)
    return verified

def verify():
    """
    Verify handler
    """
    return _verify(request)

def auth():
    """
    Provide JWT
    Verify user exists in storage, generate JWT
    """
    cid = request.form.get('client_id')
    secret = request.form.get('client_secret')
    secret_sha = hashlib.sha256(bytes(secret, 'utf-8')).hexdigest() # pw is encrypted at rest. Need to encrypt to match
    authenticated = models.authenticate(cid, secret_sha)
    # if response.is_auth():
    #     return {'success': False}
    # return json.dumps(response.body())
    if not authenticated:
        return {'success': False}
    return json.dumps(authenticated)


def client():
    """
    Save user creds in DB
    """
    # can use `token` for invalidating token - eg put in a `denied` table
    # token = request.headers.get('authorization').replace('Bearer', '')
    cid = request.form.get('client_id')
    secret = request.form.get('client_secret')
    is_admin = request.form.get('is_admin', False)
    secret_sha = hashlib.sha256(bytes(secret, 'utf-8')).hexdigest() # encrypt pw at rest
    response = models.create(cid, secret_sha, is_admin)
    return {'success': response}


def page_not_found():
    """
    Render page not found template
    """
    return render_template('404.html'), 404

def auth_denied(error):
    """
    Render auth denied template
    """
    error=['auth denied']
    return render_template('errors.html', error=error), 403


def routes(app):
    """
    Routing for client to have auth API exposed
    """
    app.add_url_rule("/auth", "auth", auth, methods=['POST'])
    app.add_url_rule("/verify", "verify", verify, methods=['POST'])
    app.add_url_rule("/client", "client", client, methods=['POST'])
    app.add_url_rule("/logout", "logout", logout, methods=['POST'])
    app.register_error_handler(403, auth_denied)
    app.register_error_handler(404, page_not_found)