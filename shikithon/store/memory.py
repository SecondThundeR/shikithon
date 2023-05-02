"""Memory based config store class"""
from typing import Optional

from ..exceptions import StoreException
from .base import ConfigsDict, ReturnConfig, Store, Token


class MemoryStore(Store):
    """Memory config store class.

    This class is used for storing configs in RAM for faster access
    """

    __slots__ = ('_configs',)

    def __init__(self, configs: Optional[ConfigsDict] = None):
        super().__init__()
        self._configs: ConfigsDict = configs or {}

    @property
    def configs(self) -> ConfigsDict:
        return self._configs

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
        app_data = self._configs.get(app_name)
        if app_data is None:
            app_data = self._configs[app_name] = {}

        app_token: Token = {
            'auth_code': auth_code,
            'scopes': scopes,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_expire_at': token_expire_at
        }

        app_tokens = app_data.get('tokens', [])
        for token in app_tokens:
            if token.get('auth_code') == auth_code and token.get(
                    'scopes') == scopes:
                token.update(app_token)
                break
        else:
            app_tokens.append(app_token)

        # Replaced update with keyword arguments
        # as mypy has type check problems with it
        # https://github.com/python/mypy/issues/6019
        app_data.update({
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri,
            'tokens': app_tokens
        })

    async def fetch_by_access_token(self, app_name: str, access_token: str):
        app_config = self._configs.get(app_name)

        if app_config is None:
            return None

        for token in app_config['tokens']:
            if token.get('access_token') == access_token:
                config: ReturnConfig = {
                    'app_name': app_name,
                    'client_id': app_config['client_id'],
                    'client_secret': app_config['client_secret'],
                    'redirect_uri': app_config['redirect_uri'],
                    # See: https://github.com/python/mypy/issues/9408
                    **token  # type: ignore[misc]
                }
                return config

        return None

    async def fetch_by_auth_code(self, app_name: str, auth_code: str):
        app_config = self._configs.get(app_name)
        if app_config is None:
            return None

        for token in app_config['tokens']:
            if token.get('auth_code') == auth_code:
                config: ReturnConfig = {
                    'app_name': app_name,
                    'client_id': app_config['client_id'],
                    'client_secret': app_config['client_secret'],
                    'redirect_uri': app_config['redirect_uri'],
                    # See: https://github.com/python/mypy/issues/9408
                    **token  # type: ignore[misc]
                }
                return config

        return None

    async def delete_token(self, app_name: str, access_token: str):
        app_config = self._configs.get(app_name)

        if app_config is None:
            raise StoreException(f'The access token {access_token} \
                            of the "{app_name}" app does not exist')

        if len(app_config['tokens']) < 2:
            return await self.delete_all_tokens(app_name)

        for idx, token in enumerate(app_config['tokens']):
            if token.get('access_token') == access_token:
                del app_config['tokens'][idx]

    async def delete_all_tokens(self, app_name: str):
        try:
            self._configs.pop(app_name)
        except KeyError as exc:
            raise StoreException(
                f'The "{app_name}" config app does not exist') from exc

    async def close(self):
        self._configs.clear()
        return await super().close()
