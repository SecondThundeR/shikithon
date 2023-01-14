"""..."""
from typing import Any, Dict, Optional

from .base import Store


class MemoryStore(Store):
    """..."""

    __slots__ = ('_configs',)

    def __init__(self, configs: Optional[Dict[str, Any]] = None) -> None:
        self._configs = configs or {}

    @property
    def configs(self) -> Dict[str, Any]:
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
                          auth_code: Optional[str] = None) -> None:
        app_data = self._configs.get(app_name)
        if app_data is None:
            app_data = self._configs[app_name] = {}

        app_token = {
            'auth_code': auth_code,
            'scopes': scopes,
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_expire_at': token_expire_at
        }

        app_tokens = app_data.get('tokens', [])
        for token in app_tokens:
            token: Dict[str, Any]
            if token.get('access_token') == access_token:
                token.update(app_token)
                break
        else:
            app_tokens.append(app_token)

        app_data.update(client_id=client_id,
                        client_secret=client_secret,
                        redirect_uri=redirect_uri,
                        tokens=app_tokens)

    async def fetch_by_access_token(
            self, app_name: str, access_token: str) -> Optional[Dict[str, Any]]:
        app_config = self._configs.get(app_name)
        if app_config is not None:
            for token in app_config['tokens']:
                token: Dict[str, Any]
                if token.get('access_token') == access_token:
                    return {
                        'app_name': app_name,
                        'client_id': app_config['client_id'],
                        'client_secret': app_config['client_secret'],
                        'redirect_uri': app_config['redirect_uri'],
                        **token
                    }
        return None

    async def fetch_by_auth_code(self, app_name: str,
                                 auth_code: str) -> Optional[Dict[str, Any]]:
        app_config = self._configs.get(app_name)
        if app_config is not None:
            for token in app_config['tokens']:
                token: Dict[str, Any]
                if token.get('auth_code') == auth_code:
                    return {
                        'app_name': app_name,
                        'client_id': app_config['client_id'],
                        'client_secret': app_config['client_secret'],
                        'redirect_uri': app_config['redirect_uri'],
                        **token
                    }
        return None

    async def delete_token(self, app_name: str, access_token: str) -> None:
        app_config = self._configs.get(app_name)

        if app_config is not None:
            if len(app_config['tokens']) < 2:
                await self.delete_all_tokens(app_name)
            else:
                for idx, token in enumerate(app_config['tokens']):
                    token: Dict[str, Any]
                    if token.get('access_token') == access_token:
                        del app_config['tokens'][idx]
            return

        raise Exception(f'The access token {access_token} \
              of the "{app_name}" app does not exist')

    async def delete_all_tokens(self, app_name: str) -> None:
        try:
            self._configs.pop(app_name)
        except KeyError as exc:
            raise Exception(
                f'The "{app_name}" config app does not exist') from exc

    async def close(self) -> None:
        self._configs.clear()