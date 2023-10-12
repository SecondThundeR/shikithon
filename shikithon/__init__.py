"""Contains package version and some magic for importing API object."""
from .api import ShikimoriAPI
from .store import JSONStore, MemoryStore, NullStore, Store

__version__ = '2.6.0'
__all__ = ['ShikimoriAPI', 'Store', 'NullStore', 'MemoryStore', 'JSONStore']
