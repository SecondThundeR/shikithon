"""Base classes for config store."""
from __future__ import annotations

from typing import Any, Dict, Optional


class Store:
    """Abstract class for config store.

    This class is used to create custom stores by overriding abstract methods.
    """

    __slots__ = ('_is_open',)

    def __init__(self) -> None:
        self._is_open = False

    @property
    def status(self) -> bool:
        """Returns store status.

        :return: Current store status
        :rtype: bool
        """
        return self._is_open

    async def save_config(self,
                          app_name: str,
                          client_id: str,
                          client_secret: str,
                          redirect_uri: str,
                          scopes: str,
                          access_token: str,
                          refresh_token: Optional[str] = None,
                          token_expire_at: Optional[int] = None,
                          auth_code: Optional[str] = None) -> None:
        """Saves config using the method of the selected store class.

        :param app_name: Application name
        :type app_name: str

        :param client_id: Client ID
        :type client_id: str

        :param client_secret: Client secret
        :type client_secret: str

        :param redirect_uri: Redirect URI
        :type redirect_uri: str

        :param scopes: Application scopes
        :type scopes: str

        :param access_token: Access token
        :type access_token: str

        :param refresh_token: Refresh token
        :type refresh_token: Optional[str]

        :param token_expire_at: Token expire time
        :type token_expire_at: Optional[int]

        :param auth_code: Auth code
        :type auth_code: Optional[str]
        """
        raise NotImplementedError

    async def fetch_by_access_token(
            self, app_name: str, access_token: str) -> Optional[Dict[str, Any]]:
        """Fetches config by access token.

        :param app_name: Application name
        :type app_name: str

        :param access_token: Access token
        :type access_token: str

        :return: Config dictionary
        :rtype: Optional[Dict[str, Any]]
        """
        raise NotImplementedError

    async def fetch_by_auth_code(self, app_name: str,
                                 auth_code: str) -> Optional[Dict[str, Any]]:
        """Fetches config by auth code.

        :param app_name: Application name
        :type app_name: str

        :param auth_code: Auth code
        :type auth_code: str

        :return: Config dictionary
        :rtype: Optional[Dict[str, Any]]
        """
        raise NotImplementedError

    async def delete_token(self, app_name: str, access_token: str) -> None:
        """Deletes token from config.

        :param app_name: Application name
        :type app_name: str

        :param access_token: Access token
        :type access_token: str
        """
        raise NotImplementedError

    async def delete_all_tokens(self, app_name: str) -> None:
        """Deletes all tokens from config.

        :param app_name: Application name
        :type app_name: str
        """
        raise NotImplementedError

    async def open(self) -> Store:
        """Open store and return self.

        :return: Store instance
        :rtype: Store
        """
        self._is_open = True
        return self

    async def close(self) -> None:
        """Close store."""
        self._is_open = False

    async def __aenter__(self) -> Store:
        """Async context manager entry point.

        :return: Store instance
        :rtype: Store
        """
        return await self.open()

    async def __aexit__(self, *args) -> None:
        """Async context manager exit point."""
        await self.close()


class NullStore(Store):
    """Dummy store with an empty implementation of an abstract store class.

    This store is used when no store is provided to the client.
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
                          auth_code: Optional[str] = None) -> None:
        pass

    async def fetch_by_access_token(
            self, app_name: str, access_token: str) -> Optional[Dict[str, Any]]:
        pass

    async def fetch_by_auth_code(self, app_name: str,
                                 auth_code: str) -> Optional[Dict[str, Any]]:
        pass

    async def delete_token(self, app_name: str, access_token: str) -> None:
        pass

    async def delete_all_tokens(self, app_name: str) -> None:
        pass
