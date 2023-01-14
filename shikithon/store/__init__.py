"""Config store for shikithon library."""

from .base import Store
from .json import JsonStore
from .memory import MemoryStore

__all__ = ['Store', 'MemoryStore', 'JsonStore']
