"""Decorator for protected methods"""
from __future__ import annotations

from typing import Optional

from loguru import logger

from ..resources.base_resource import BaseResource


def protected_method(client_attr: str, scope: Optional[str] = None):
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

    :return: Decorator function
    :rtype: Callable
    """

    def protected_method_decorator(function):

        def protected_method_wrapper(self, resource: BaseResource, *args,
                                     **kwargs):
            """
            Decorator's wrapper function.

            Check for token expire time.
            If needed, triggers token refresh function.

            :return: None if API object is in restricted mode
                or if required scope is missing
            :rtype: None or Callable
            """
            client = getattr(self, client_attr)
            logger.debug('Checking the possibility of using a protected method')

            if client.restricted_mode:
                logger.debug('It is not possible to use the protected method '
                             'due to the restricted mode')
                return None

            if scope and scope not in client.scopes_list:
                logger.debug(f'Protected method cannot be used due to the '
                             f'absence of "{scope}" scope')
                return None

            if client.token_expired():
                logger.debug('Token has expired. Refreshing...')
                client.refresh_tokens()

            logger.debug('All checks for use of the protected '
                         'method have been passed')
            return function(self, resource, *args, **kwargs)

        return protected_method_wrapper

    return protected_method_decorator
