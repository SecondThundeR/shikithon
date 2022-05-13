"""Custom decorators for API class."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List

if TYPE_CHECKING:
    from shikithon.api import API


def protected_method(decorated):
    """
    Decorator for protected API methods.

    This method is used for all protected methods
    and checks the expiration of the access token.

    When the access token is no longer valid,
    triggers the token update function.
    """

    def wrapper(api: API, *args: List[Any], **kwargs: Dict[str, Any]):
        """
        Decorator's wrapper function.

        Check for token expire time.
        If needed, triggers token refresh function.

        :return: None if API object is in restricted mode
        :rtype: None
        """
        if api.restricted_mode:
            return None

        if api.token_expired():
            api.refresh_tokens()
        return decorated(api, *args, **kwargs)

    return wrapper
