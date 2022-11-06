"""Decorator for method endpoint logging"""
from __future__ import annotations

from typing import Any, Callable, Dict, Tuple, TypeVar

from loguru import logger

RT = TypeVar('RT')


def method_endpoint(
    method_endpoint_name: str
) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    """
    Decorator for logging method endpoint.

    :param method_endpoint_name: Name of method endpoint
    :type method_endpoint_name: str

    :return: Decorator function
    :rtype: Callable[[Callable[..., RT]], Callable[..., RT]]
    """

    def endpoint_logger_decorator(
            function: Callable[..., RT]) -> Callable[..., RT]:
        """Endpoint logger decorator.

        :param function: Function to decorate
        :type function: Callable[..., RT]

        :return: Decorated function
        :rtype: Callable[..., RT]
        """

        def endpoint_logger_wrapper(*args: Tuple[Any],
                                    **kwargs: Dict[str, Any]) -> RT:
            """
            Decorator's wrapper function.
            Logs endpoint of method

            :param args: Positional arguments
            :type args: Tuple[Any]

            :param kwargs: Keyword arguments
            :type kwargs: Dict[str, Any]

            :return: Result of decorated function
            :rtype: RT
            """
            logger.debug(f'Executing "{method_endpoint_name}" method')
            return function(*args, **kwargs)

        return endpoint_logger_wrapper

    return endpoint_logger_decorator
