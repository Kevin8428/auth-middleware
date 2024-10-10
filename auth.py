from flask import Flask, request
import json
import os
import hashlib

import storage

app = Flask(__name__)

# change `storage.py` name
# return status code
# reorge file hierarcy

# routes to add
# /logout - add token to `blocked` table

@app.route("/logout", methods=["POST"])
def logout():
    token = request.form.get("token")
    status = storage.block(token)
    return {'success': status}

@app.route("/verify", methods=["POST"])
def verify():
    """
    Verify JWT - decoode token with AUTHSECRET
    """
    token = request.headers.get('authorization').replace('Bearer ', '')
    verified = storage.verify(token)
    if not verified:
        return {'success': False}
    return verified

@app.route("/auth", methods=["POST"])
def auth():
    """
    Provide JWT
    Verify user exists in storage, generate JWT
    """
    cid = request.form.get('client_id')
    secret = request.form.get('client_secret')
    secret_sha = hashlib.sha256(bytes(secret, 'utf-8')).hexdigest() # pw is encrypted at rest. Need to encrypt to match
    authenticated = storage.authenticate(cid, secret_sha)
    # if response.is_auth():
    #     return {'success': False}
    # return json.dumps(response.body())
    if not authenticated:
        return {'success': False}
    return json.dumps(authenticated)


@app.route("/client", methods=["POST"])
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
    response = storage.create(cid, secret_sha, is_admin)
    return {'success': response}