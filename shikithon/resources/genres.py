"""Represents `/api/genres` resource."""
from typing import Any, Dict, List, cast

from ..decorators import exceptions_handler, method_endpoint
from ..exceptions import ShikimoriAPIResponseError
from ..models import Genre
from ..utils import Utils
from .base_resource import BaseResource


class Genres(BaseResource):
    """Genres resource class.

    Used to represent `/api/genres` resource
    """

    @method_endpoint('/api/genres')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self):
        """Returns list of genres.

        :return: List of genres
        :rtype: List[Genre]
        """
        response = await self._client.request(self._client.endpoints.genres)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Genre)
