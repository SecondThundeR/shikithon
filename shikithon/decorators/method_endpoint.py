"""Decorator for logging method endpoint."""
from functools import wraps
from typing import Awaitable, Callable, TypeVar

from loguru import logger
from typing_extensions import ParamSpec

P = ParamSpec('P')
R = TypeVar('R')


def method_endpoint(
    method_endpoint_name: str
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """Decorator for logging method endpoint.

    :param method_endpoint_name: Name of method endpoint
    :type method_endpoint_name: str

    :return: Decorator function
    :rtype: Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]
    """

    def endpoint_logger_wrapper(
            function: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """Endpoint logger wrapper.

        :param function: Function to decorate
        :type function: Callable[P, Awaitable[R]]

        :return: Decorated function
        :rtype: Callable[P, Awaitable[R]]
        """

        @wraps(function)
        async def endpoint_logger_wrapped(*args: P.args,
                                          **kwargs: P.kwargs) -> R:
            """Decorator's wrapped function for logging endpoint of method.

            :param args: Positional arguments
            :type args: P.args

            :param kwargs: Keyword arguments
            :type kwargs: P.kwargs

            :return: Result of decorated function
            :rtype: R
            """
            logger.debug(f'Executing "{method_endpoint_name}" method')
            return await function(*args, **kwargs)

        return endpoint_logger_wrapped

    return endpoint_logger_wrapper
