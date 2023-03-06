"""Decorator for handling method exceptions."""
from functools import wraps
from typing import Any, Awaitable, Callable, Type, TypeVar

from loguru import logger
from typing_extensions import ParamSpec

P = ParamSpec('P')
R = TypeVar('R')


def exceptions_handler(
    *exceptions: Type[Exception], **params: Any
) -> Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]:
    """Decorator for handling method exceptions.

    :param exceptions: Tuple of exceptions
    :type exceptions: Type[Exception]

    :param params: Dictionary with other params
    :type params: Any

    :return: Decorator function
    :rtype: Callable[[Callable[P, Awaitable[R]]], Callable[P, Awaitable[R]]]
    """

    if not exceptions:
        exceptions = (Exception,)

    async def fallback() -> R:
        """Returns fallback value from params dictionary.

        :return: Decorator function
        :rtype: R
        """
        return params.get('fallback', None)

    def exceptions_handler_wrapper(
            function: Callable[P, Awaitable[R]]) -> Callable[P, Awaitable[R]]:
        """Exceptions handler wrapper.

        :param function: Function to wrap
        :type function: Callable[P, Awaitable[R]]

        :return: Wrapped function
        :rtype: Callable[P, Awaitable[R]]
        """

        @wraps(function)
        async def exceptions_handler_wrapped(*args: P.args,
                                             **kwargs: P.kwargs) -> R:
            """Decorator's wrapped function for handling method exceptions.

            :param args: Positional arguments
            :type args: P.args

            :param kwargs: Keyword arguments
            :type kwargs: P.kwargs

            :return: Result of decorated function
            :rtype: R
            """
            logger.debug(f'Handling "{function.__qualname__}" exceptions')

            try:
                return await function(*args, **kwargs)
            except exceptions as e:
                logger.warning(e)
                return await fallback()

        return exceptions_handler_wrapped

    return exceptions_handler_wrapper
