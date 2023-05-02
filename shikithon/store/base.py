"""Base classes for config store."""
from typing import Dict, List, Optional, TypedDict


class Token(TypedDict, total=False):
    scopes: str
    access_token: str
    refresh_token: Optional[str]
    token_expire_at: Optional[int]
    auth_code: Optional[str]


class Config(TypedDict, total=False):
    client_id: str
    client_secret: str
    redirect_uri: str
    tokens: List[Token]


class ReturnConfig(Config):
    app_name: str


ConfigsDict = Dict[str, Config]


class Store:
    """Abstract class for config store.

    This class is used to create custom stores by overriding abstract methods
    """

    __slots__ = ('_closed',)

    def __init__(self):
        self._closed = True

    @property
    def closed(self):
        """Returns close status of store.

        :return: True if store is closed, False otherwise
        :rtype: bool
        """
        return self._closed

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
            self, app_name: str, access_token: str) -> Optional[ReturnConfig]:
        """Fetches config by access token.

        :param app_name: Application name
        :type app_name: str

        :param access_token: Access token
        :type access_token: str

        :return: Config dictionary
        :rtype: Optional[ReturnConfig]
        """
        raise NotImplementedError

    async def fetch_by_auth_code(self, app_name: str,
                                 auth_code: str) -> Optional[ReturnConfig]:
        """Fetches config by auth code.

        :param app_name: Application name
        :type app_name: str

        :param auth_code: Auth code
        :type auth_code: str

        :return: Config dictionary
        :rtype: Optional[ReturnConfig]
        """
        raise NotImplementedError

    async def delete_token(self, app_name: str, access_token: str):
        """Deletes token from config.

        :param app_name: Application name
        :type app_name: str

        :param access_token: Access token
        :type access_token: str
        """
        raise NotImplementedError

    async def delete_all_tokens(self, app_name: str):
        """Deletes all tokens from config.

        :param app_name: Application name
        :type app_name: str
        """
        raise NotImplementedError

    async def open(self):
        """Opens store and returns self.

        :return: Store instance
        :rtype: Store
        """
        self._closed = False
        return self

    async def close(self):
        """Closes store."""
        self._closed = True

    async def __aenter__(self):
        """Async context manager entry point.

        :return: Store instance
        :rtype: Store
        """
        return await self.open()

    async def __aexit__(self, *args):
        """Async context manager exit point."""
        await self.close()
