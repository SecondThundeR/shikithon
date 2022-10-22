"""Represents /api/genres resource."""
from typing import Any, Dict, List, Optional

from ..decorators import method_endpoint
from ..models import Genre
from ..utils import Utils
from .base_resource import BaseResource


class Genres(BaseResource):
    """Genres resource class.

    Used to represent /api/genres resource.
    """

    @method_endpoint('/api/genres')
    async def get(self) -> Optional[List[Genre]]:
        """
        Returns list of genres.

        :return: List of genres
        :rtype: Optional[List[Genre]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.genres)
        return Utils.validate_return_data(response, data_model=Genre)
