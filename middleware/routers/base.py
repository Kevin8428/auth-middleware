"""
Auth implementations
"""
import os
import logging

from middleware import auth

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

class Client:
    """docs"""
    def __init__(self, **params):
        self.logger = logging.getLogger(__name__)
        self.auth_client = params.get('auth_client', auth.client('jwt'))
        self.run()
        for key, val in params.items():
            setattr(self, key, val)
    
    def run(self):
        """docs"""
        raise NotImplementedError