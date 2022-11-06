"""Represents /api/publishers resource."""
from typing import Any, Dict, List

from ..decorators import method_endpoint
from ..models import Publisher
from ..utils import Utils
from .base_resource import BaseResource


class Publishers(BaseResource):
    """Publishers resource class.

    Used to represent /api/publishers resource.
    """

    @method_endpoint('/api/publishers')
    async def get(self) -> List[Publisher]:
        """
        Returns list of publishers.

        :return: List of publishers
        :rtype: List[Publisher]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.publishers)
        return Utils.validate_response_data(response,
                                            data_model=Publisher,
                                            fallback=[])
