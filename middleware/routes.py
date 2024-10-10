import hashlib

from middleware import models
def client(request):
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