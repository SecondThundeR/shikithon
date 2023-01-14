"""Contains package version and some magic for importing API object."""
from .api import ShikimoriAPI
from .store import JsonStore
from .store import MemoryStore
from .store import Store

__version__ = '2.1.4'
__all__ = ['ShikimoriAPI', 'Store', 'MemoryStore', 'JsonStore']
