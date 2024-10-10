"""
Auth implementations
"""
import os
import logging
import json
from functools import wraps

from flask import Flask, render_template, request, abort

from middleware.routers import base

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

class FlaskClient(base.Client):
    """docstring"""

    def __init__(self, **params):
        self.client = Flask(__name__)
        super().__init__(**params)


    def verify_middleware(self, f):
        """docs"""
        wraps(f)
        def decorated_function(*args, **kwargs):
            verified = self.verify()
            if not verified:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function


    def page_not_found(self):
        """
        Render page not found template
        """
        return render_template('404.html'), 404


    def auth_denied(self, error):
        """
        Render auth denied template
        """
        error=['auth denied']
        return render_template('errors.html', error=error), 403
    
    def logout(self):
        """
        Add token to `blocked` table
        """
        token = request.form.get("token")
        status = self.auth_client.logout(token)
        return {'success': status}
    
    def verify(self):
        """
        Verify handler
        """
        token = request.headers.get('authorization').replace('Bearer ', '').strip()
        return self.auth_client.verify(token)

    def authenticate(self):
        """
        Provide JWT
        Verify user exists in storage, generate JWT
        """
        cid = request.form.get('client_id')
        secret = request.form.get('client_secret')
        authenticated = self.auth_client.authenticate(cid, secret)
        if not authenticated:
            return {'success': False}
        return json.dumps(authenticated)

    def save(self):
        """
        Save user creds in DB
        """
        cid = request.form.get('client_id')
        secret = request.form.get('client_secret')
        is_admin = request.form.get('is_admin', False)
        response = self.auth_client.save(cid, secret, is_admin)
        return {'success': response}

    def run(self):
        """docstring"""
        self.client.add_url_rule("/verify", "verify", self.verify, methods=['POST'])
        self.client.add_url_rule("/logout", "logout", self.logout, methods=['POST'])
        self.client.add_url_rule("/authenticate", "authenticate", self.authenticate, methods=['POST'])
        self.client.add_url_rule("/save", "save", self.save, methods=['POST'])
        self.client.register_error_handler(403, self.auth_denied)
        self.client.register_error_handler(404, self.page_not_found)


def client(**kwargs):
    """
    get client
    """
    return FlaskClient(**kwargs)