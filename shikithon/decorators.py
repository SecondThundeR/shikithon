"""Custom decorators for API class."""


from __future__ import annotations
from time import time
from typing import Any
from typing import Dict
from typing import Tuple
from typing import TYPE_CHECKING

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
    def wrapper(api: API, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]):
        if int(time()) > api.token_expire:
            tokens_data: Tuple[str, str] = api.get_access_token(
                refresh_token=True
            )
            api.update_tokens(tokens_data)
        return decorated(api, *args, **kwargs)
    return wrapper
