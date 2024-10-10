import importlib as _importlib

def client(name, **kwargs):
    """
    Create client
    """
    module = _importlib.import_module(f'{__name__}.{name}')
    return module.client(**kwargs)