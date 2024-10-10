"""
Auth implementations
"""
import os
import logging

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

class Base:
    """docs"""
    def __init__(self, client=None, **params):
        self.client = client
        self.logger = logging.getLogger(__name__)
        for key, val in params.items():
            setattr(self, key, val)


class Client(Base):
    """docstring"""
    def authenticate(self, cid, secret):
        """
        Client interface spec
        """
        raise NotImplementedError
    def verify(self, token):
        """
        Client interface spec
        """
        raise NotImplementedError
    def save(self, **params):
        """
        Client interface spec
        """
        raise NotImplementedError
    def logout(self, token):
        """
        Client interface spec
        """
        raise NotImplementedError