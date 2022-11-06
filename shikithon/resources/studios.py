"""Represents /api/studios resource."""
from typing import Any, Dict, List

from ..decorators import method_endpoint
from ..models import Studio
from ..utils import Utils
from .base_resource import BaseResource


class Studios(BaseResource):
    """Studios resource class.

    Used to represent /api/studios resource.
    """

    @method_endpoint('/api/studios')
    async def get(self) -> List[Studio]:
        """
        Returns list of studios.

        :return: List of studios
        :rtype: List[Studio]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.studios)
        return Utils.validate_response_data(response,
                                            data_model=Studio,
                                            fallback=[])
