"""..."""
from __future__ import annotations

from typing import Any, Dict


class Store:
    """..."""

    async def save_config(self, app_name: str, client_id: str,
                          client_secret: str, redirect_uri: str, auth_code: str,
                          scopes: str, access_token: str, refresh_token: str,
                          token_expire: int) -> None:
        raise NotImplementedError

    async def fetch_by_access_token(self, app_name: str,
                                    access_token: str) -> Dict[str, Any]:
        raise NotImplementedError

    async def fetch_by_auth_code(self, app_name: str,
                                 auth_code: str) -> Dict[str, Any]:
        raise NotImplementedError

    async def delete_token(self, app_name: str, access_token: str) -> None:
        raise NotImplementedError

    async def delete_all_tokens(self, app_name: str) -> None:
        raise NotImplementedError

    async def open(self) -> Store:
        """Open store and return self."""
        return self

    async def close(self) -> None:
        """Close store."""
        pass

    async def __aenter__(self) -> Store:
        """Async context manager entry point."""
        return await self.open()

    async def __aexit__(self, *args) -> None:
        """Async context manager exit point."""
        await self.close()
