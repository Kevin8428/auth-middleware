from flask import Flask, request
import json
import os
import hashlib

import storage

app = Flask(__name__)

@app.route("/client", methods=["POST"])
def client():
    """
    get `authorization` header (token)
    get is_admin
    get client_id
    get client_secret.hexdigest()
    hash secret with sha1
    write to `clients` table - client_id, client_secret, is_admin
    """

    # can use `token` for invalidating token - eg put in a `denied` table
    # token = request.headers.get('authorization').replace('Bearer', '')
    cid = request.form.get('client_id')
    secret = request.form.get('client_secret')
    is_admin = request.form.get('is_admin', False)
    secret_sha = hashlib.sha1(bytes(secret, 'utf-8')).hexdigest()
    response = storage.create(cid, secret_sha, is_admin)
    return {'success': response}