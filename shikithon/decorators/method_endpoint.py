"""Decorator for method endpoint logging"""
from functools import wraps
from typing import Callable, TypeVar

from loguru import logger
from typing_extensions import ParamSpec

P = ParamSpec('P')
R = TypeVar('R')


def method_endpoint(
        method_endpoint_name: str
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator for logging method endpoint.

    :param method_endpoint_name: Name of method endpoint
    :type method_endpoint_name: str

    :return: Decorator function
    :rtype: Callable[[Callable[P, R]], Callable[P, R]]
    """

    def endpoint_logger_decorator(function: Callable[P, R]) -> Callable[P, R]:
        """Endpoint logger decorator.

        :param function: Function to decorate
        :type function: Callable[P, R]

        :return: Decorated function
        :rtype: Callable[P, R]
        """

        @wraps(function)
        def endpoint_logger_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            """
            Decorator's wrapper function.
            Logs endpoint of method

            :param args: Positional arguments
            :type args: P.args

            :param kwargs: Keyword arguments
            :type kwargs: P.kwargs

            :return: Result of decorated function
            :rtype: R
            """
            logger.debug(f'Executing "{method_endpoint_name}" method')
            return function(*args, **kwargs)

        return endpoint_logger_wrapper

    return endpoint_logger_decorator
