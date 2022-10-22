"""Represents /api/publishers resource."""
from typing import Any, Dict, List, Optional

from ..decorators import method_endpoint
from ..models import Publisher
from ..utils import Utils
from .base_resource import BaseResource


class Publishers(BaseResource):
    """Publishers resource class.

    Used to represent /api/publishers resource.
    """

    @method_endpoint('/api/publishers')
    async def get(self) -> Optional[List[Publisher]]:
        """
        Returns list of publishers.

        :return: List of publishers
        :rtype: Optional[List[Publisher]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.publishers)
        return Utils.validate_return_data(response, data_model=Publisher)
