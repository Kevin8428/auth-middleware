from flask import request, abort

from functools import wraps
import models

def validate_request(f):
    """docs"""
    wraps(f)
    def decorated_function(*args, **kwargs):
        verified = verify(request)
        print('verified: ', verified)
        if not verified:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function



def verify(request):
    """
    Verify JWT - decoode token with AUTHSECRET
    """
    print('request: ', request)
    token = request.headers.get('authorization').replace('Bearer ', '')
    print('token: ', token)
    verified = models.verify(token)
    print('verified: ', verified)
    
    return verified
