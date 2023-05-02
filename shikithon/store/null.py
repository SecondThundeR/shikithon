"""Dummy config store class."""
from typing import Optional

from .base import ReturnConfig, Store


class NullStore(Store):
    """Dummy store with an empty implementation of an abstract store class.

    This store is used when no store is provided to the client
    """

    async def save_config(self,
                          app_name: str,
                          client_id: str,
                          client_secret: str,
                          redirect_uri: str,
                          scopes: str,
                          access_token: str,
                          refresh_token: Optional[str] = None,
                          token_expire_at: Optional[int] = None,
                          auth_code: Optional[str] = None):
        pass

    async def fetch_by_access_token(
            self, app_name: str, access_token: str) -> Optional[ReturnConfig]:
        pass

    async def fetch_by_auth_code(self, app_name: str,
                                 auth_code: str) -> Optional[ReturnConfig]:
        pass

    async def delete_token(self, app_name: str, access_token: str):
        pass

    async def delete_all_tokens(self, app_name: str):
        pass
