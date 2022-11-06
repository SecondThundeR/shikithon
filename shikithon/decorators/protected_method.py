"""Decorator for protected methods"""
from __future__ import annotations

from typing import Any, Callable, Optional, Tuple, TypeVar

from loguru import logger

from ..resources.base_resource import BaseResource

RT = TypeVar('RT')


def protected_method(
    client_attr: str,
    scope: Optional[str] = None,
    fallback: Optional[Any] = None
) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
    """
    Decorator for protected API methods.

    This method is used for all protected methods
    and checks the expiration of the access token.

    When the access token is no longer valid,
    triggers the token update function.

    Also, this decorator take a scope parameter
    for checking, if current app is allowed to access
    protected method.

    :param client_attr: Name of client attribute
    :type client_attr: str

    :param scope: Scope of app
    :type scope: Optional[str]

    :param fallback: Fallback value
    :type fallback: Optional[Any]

    :return: Decorator function
    :rtype: Callable[[Callable[..., RT]], Callable[..., RT]]
    """

    def protected_method_decorator(
            function: Callable[..., RT]) -> Callable[..., RT]:
        """Protected method decorator.

        :param function: Function to decorate
        :type function: Callable[..., RT]

        :return: Decorated function
        :rtype: Callable[..., RT]
        """

        def protected_method_wrapper(self: BaseResource, *args: Tuple[Any],
                                     **kwargs: Any) -> RT:
            """
            Decorator's wrapper function.

            Check for token expire time.
            If needed, triggers token refresh function.

            :param self: Resource instance
            :type self: BaseResource

            :param args: Positional arguments
            :type args: Tuple[Any]

            :param kwargs: Keyword arguments
            :type kwargs: Any

            :return: Fallback function if API object is in restricted mode
                or if required scope is missing
            :rtype: RT
            """
            client = getattr(self, client_attr)
            logger.debug('Checking the possibility of using a protected method')

            async def fallback_function() -> RT:
                return fallback

            if client.restricted_mode:
                logger.debug('It is not possible to use the protected method '
                             'due to the restricted mode')
                return fallback_function()

            if scope and scope not in client.scopes_list:
                logger.debug(f'Protected method cannot be used due to the '
                             f'absence of "{scope}" scope')
                return fallback_function()

            if client.token_expired():
                logger.debug('Token has expired. Refreshing...')
                client.refresh_tokens()

            logger.debug('All checks for use of the protected '
                         'method have been passed')
            return function(self, *args, **kwargs)

        return protected_method_wrapper

    return protected_method_decorator
