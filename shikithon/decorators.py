"""Custom decorators for API class."""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from shikithon.api import API


def protected_method(scope=None):
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

    def decorator(function):

        def wrapper(api: API, *args, **kwargs):
            """
            Decorator's wrapper function.

            Check for token expire time.
            If needed, triggers token refresh function.

            :return: None if API object is in restricted mode
                or if required scope is missing
            :rtype: None
            """
            if api.restricted_mode:
                return None

            if scope and scope not in api.scopes_list:
                return None

            if api.token_expired():
                api.refresh_tokens()
            return function(api, *args, **kwargs)

        return wrapper

    return decorator
