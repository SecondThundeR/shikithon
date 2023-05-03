"""Represents `/api/characters` resource."""
from typing import Any, Dict, List, Optional, cast

from ..decorators import exceptions_handler, method_endpoint
from ..exceptions import ShikimoriAPIResponseError
from ..models import CharacterInfo, Character
from ..utils import Utils
from .base_resource import BaseResource


class Characters(BaseResource):
    """Characters resource class.

    Used to represent `/api/characters` resource
    """

    @method_endpoint('/api/characters/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def get(self, character_id: int):
        """Returns character info by ID.

        :param character_id: ID of character to get info
        :type character_id: int

        :return: Character info
        :rtype: Optional[Character]
        """
        response = await self._client.request(
            self._client.endpoints.character(character_id))

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Character)

    @method_endpoint('/api/characters/search')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def search(self, search: Optional[str] = None):
        """Returns list of found characters.

        :param search: Search query for characters
        :type search: Optional[str]

        :return: List of found characters
        :rtype: List[CharacterInfo]
        """
        query_dict = Utils.create_query_dict(search=search)

        response = await self._client.request(
            self._client.endpoints.character_search, query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=CharacterInfo)
