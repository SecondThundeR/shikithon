"""JSON based config store class."""
from json import dumps
from json import loads
from os.path import exists
from typing import Any, Dict, Optional

from .base import Store
from .memory import MemoryStore


class JSONStore(Store):
    """JSON config store class.

    This class is used for storing configs in JSON file.
    """

    __slots__ = ('_file_path',)

    def __init__(self, file_path: str = '.shikithon') -> None:
        super().__init__()
        self._file_path = file_path

    async def _read_from_file(self) -> Optional[Dict[str, Any]]:
        if not exists(self._file_path):
            return None

        with open(self._file_path, 'r', encoding='utf-8') as file:
            return loads(file.read())

    async def _write_to_file(self, configs: Dict[str, Any]) -> bool:
        try:
            with open(self._file_path, 'w', encoding='utf-8') as file:
                file.write(dumps(configs, indent=4))
            return True
        except IOError:
            return False

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
        async with MemoryStore(await self._read_from_file()) as ms:
            ms: MemoryStore

            await ms.save_config(app_name=app_name,
                                 client_id=client_id,
                                 client_secret=client_secret,
                                 redirect_uri=redirect_uri,
                                 scopes=scopes,
                                 access_token=access_token,
                                 refresh_token=refresh_token,
                                 token_expire_at=token_expire_at,
                                 auth_code=auth_code)

            await self._write_to_file(ms.configs)

    async def fetch_by_access_token(
            self, app_name: str, access_token: str) -> Optional[Dict[str, Any]]:
        async with MemoryStore(await self._read_from_file()) as ms:
            return await ms.fetch_by_access_token(app_name=app_name,
                                                  access_token=access_token)

    async def fetch_by_auth_code(self, app_name: str,
                                 auth_code: str) -> Optional[Dict[str, Any]]:
        async with MemoryStore(await self._read_from_file()) as ms:
            return await ms.fetch_by_auth_code(app_name=app_name,
                                               auth_code=auth_code)

    async def delete_token(self, app_name: str, access_token: str) -> None:
        async with MemoryStore(await self._read_from_file()) as ms:
            ms: MemoryStore

            await ms.delete_token(app_name=app_name, access_token=access_token)

            await self._write_to_file(ms.configs)

    async def delete_all_tokens(self, app_name: str) -> None:
        async with MemoryStore(await self._read_from_file()) as ms:
            ms: MemoryStore

            await ms.delete_all_tokens(app_name)

            await self._write_to_file(ms.configs)
