"""Config store for shikithon library."""

from .base import NullStore
from .base import Store
from .json import JSONStore
from .memory import MemoryStore

__all__ = ['Store', 'NullStore', 'MemoryStore', 'JSONStore']
