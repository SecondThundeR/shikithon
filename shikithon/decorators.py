"""Custom decorators for API class."""
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from loguru import logger

if TYPE_CHECKING:
    from shikithon.api import API


def protected_method(scope: Optional[str] = None):
    """
    Decorator for protected API methods.

    This method is used for all protected methods
    and checks the expiration of the access token.

    When the access token is no longer valid,
    triggers the token update function.

    Also, this decorator take a scope parameter
    for checking, if current app is allowed to access
    protected method.
    """

    def protected_method_decorator(function):

        def protected_method_wrapper(api: API, *args, **kwargs):
            """
            Decorator's wrapper function.

            Check for token expire time.
            If needed, triggers token refresh function.

            :return: None if API object is in restricted mode
                or if required scope is missing
            :rtype: None
            """
            logger.debug('Checking the possibility of using a protected method')
            if api.restricted_mode:
                logger.debug('It is not possible to use the protected method '
                             'due to the restricted mode')
                return None

            if scope and scope not in api.scopes_list:
                logger.debug(f'Protected method cannot be used due to the '
                             f'absence of "{scope}" scope')
                return None

            if api.token_expired():
                logger.debug('Token has expired. Refreshing...')
                api.refresh_tokens()
            logger.debug('All checks for use of the protected '
                         'method have been passed')
            return function(api, *args, **kwargs)

        return protected_method_wrapper

    return protected_method_decorator


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
