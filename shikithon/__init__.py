"""Contains package version and some magic for importing API object."""
from .api import ShikimoriAPI
from .store import JSONStore
from .store import MemoryStore
from .store import NullStore
from .store import Store

__version__ = '2.3.1'
__all__ = ['ShikimoriAPI', 'Store', 'NullStore', 'MemoryStore', 'JSONStore']
