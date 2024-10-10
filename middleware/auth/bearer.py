"""
Bearer implementation
"""
from middleware.auth import base

class BearerClient(base.Client):
    """docstring"""
    def authenticate(self, **params):
        """
        Do auth
        """
    def verify(self, **params):
        """
        Do verify
        """
    def save(self, **params):
        """
        Do save
        """
    def logout(self, **params):
        """
        Do logout
        """

def client(**kwargs):
    """
    get client
    """
    return BearerClient(**kwargs)
