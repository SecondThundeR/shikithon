"""Decorator for method endpoint logging"""
from __future__ import annotations

from loguru import logger


def method_endpoint(method_endpoint_name: str):
    """
    Decorator for logging method endpoint.
    """

    def endpoint_logger_decorator(function):

        def endpoint_logger_wrapper(*args, **kwargs):
            """
            Decorator's wrapper function.
            Logs endpoint of method
            """
            logger.debug(f'Executing "{method_endpoint_name}" method')
            return function(*args, **kwargs)

        return endpoint_logger_wrapper

    return endpoint_logger_decorator
