"""Custom decorators for API class."""

from .method_endpoint import method_endpoint
from .protected_method import protected_method

__all__ = ['protected_method', 'method_endpoint']
