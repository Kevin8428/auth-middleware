from flask import Flask, request
import json
import os
import hashlib

import storage

app = Flask(__name__)

# change `storage.py` name
# return status code
# reorge file hierarcy

@app.route("/verify", methods=["POST"])
def verify():
    """
    Verify token
    do this by decoding token with AUTHSECRET -  jwt.Decode(token, AUTHSECRET)
    """
    token = request.headers.get('authorization').replace('Bearer ', '')
    verified = storage.verify(token)
    if not verified:
        return {'success': False}
    return verified

@app.route("/auth", methods=["POST"])
def auth():
    """
    POST - authenticate client - give them a token
    get id
    get secret
    get record from db with encrypted secret as id
    # - record found? ok create JWT. No? fail auth
    # - JWT is signed with server-owned secret. This way, can't be altered by anyone.
    # - this is why JWT is secure/trusted.
    # encode response using secret, user_id, user_secret
    encoded_jwt = jwt.encode(
        payload = {
            id = 1,
            clientId = 2,
            isAdmin = True,
            expiration = 2025
        },
        key='my_secret',
        algorithm='HS256'
    )
    # return
    {
        token: "fdasfsdfdafsafdadfsa",
        expiresin: 1000
    }
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
    POST - create client record
    get `authorization` header (token)
    get is_admin
    get client_id
    get client_secret.hexdigest()
    hash secret with sha256
    write to `clients` table - client_id, client_secret, is_admin
    """

    # can use `token` for invalidating token - eg put in a `denied` table
    # token = request.headers.get('authorization').replace('Bearer', '')
    cid = request.form.get('client_id')
    secret = request.form.get('client_secret')
    is_admin = request.form.get('is_admin', False)
    secret_sha = hashlib.sha256(bytes(secret, 'utf-8')).hexdigest() # encrypt pw at rest
    response = storage.create(cid, secret_sha, is_admin)
    return {'success': response}