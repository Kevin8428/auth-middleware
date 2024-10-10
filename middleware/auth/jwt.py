"""
JWT implementation
"""
import os
import json
import hashlib
import jwt as pjwt
from datetime import datetime, timedelta, timezone

from middleware.storage import storage
from middleware.auth import base
from middleware import exceptions

EXPIRE_SECONDS = 3600
HASH = os.getenv('HASH', 'HS256')
AUTHSECRET = os.getenv('AUTHSECRET')

class Response():
    def __init__(self, token, expires_in):
        self.token = token
        self.expiresin = expires_in

class Jwt():
    def __init__(self, id, client_id, is_admin, exp=None):
        self.id = id
        self.sub = client_id
        self.is_admin = is_admin
        self.exp = exp if exp else datetime.now(timezone.utc) + timedelta(seconds=EXPIRE_SECONDS)

    def to_dict(self):
        """docstring"""
        return self.__dict__

class JWTClient(base.Client):
    """docstring"""
    @staticmethod

    def to_jwt(obj):
        """docstring"""
        if isinstance(obj, storage.Client):
            return Jwt(obj.id, obj.client_id, obj.is_admin)
        raise exceptions.AuthException(f"Unsupported auth type at this time: {obj}")

    def validate_request(self, token):
        """docstring"""
        verified = self.verify(token)
        return verified
    
    def logout(self, token):
        """
        Add token to `blocked` table
        """
        status = storage.block(token)
        return status

    def verify(self, token):
        """
        Attempt to decode token
        """
        try:
            blocked = storage.is_blocked(token)
            self.logger.info('blocked: %s', blocked)
            if blocked:
                return False
            try:
                decoded = pjwt.decode(token, AUTHSECRET, algorithms=[HASH])
                return decoded
            except pjwt.ExpiredSignatureError:
                self.logger.error("Token has expired. Please log in again.")
                return False
            except pjwt.InvalidTokenError:
                self.logger.error("Invalid token. Access denied.")
                return False
        except (Exception) as e:
            self.logger.error('verification failed: %s', e)
            return False

    def authenticate(self, cid, secret):
        """
        Provide JWT
        Verify user exists in storage, generate JWT
        """
        secret_sha = hashlib.sha256(bytes(secret, 'utf-8')).hexdigest() # pw is encrypted at rest. Need to encrypt to match
        response = storage.authenticate(cid, secret_sha)
        try:
            token = pjwt.encode(self.to_jwt(response).to_dict(), AUTHSECRET, algorithm=HASH)
            return json.dumps(token)
        except exceptions.JWTEncodeError:
            self.logger.error("Failed to encode.")
            return False
        

    def save(self, cid, secret, is_admin):
        """
        Save user creds in DB
        """
        secret_sha = hashlib.sha256(bytes(secret, 'utf-8')).hexdigest() # encrypt pw at rest
        response = storage.create(cid, secret_sha, is_admin)
        return {'success': response}


def client(**kwargs):
    """
    get client
    """
    return JWTClient(**kwargs)
