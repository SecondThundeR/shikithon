"""Config store for shikithon library."""

from .base import Store
from .json import JSONStore
from .memory import MemoryStore
from .null import NullStore

__all__ = ['Store', 'NullStore', 'MemoryStore', 'JSONStore']
