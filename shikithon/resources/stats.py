"""Represents /api/stats resource."""
from typing import List

from ..decorators import method_endpoint
from ..utils import Utils
from .base_resource import BaseResource


class Stats(BaseResource):
    """Stats resource class.

    Used to represent /api/stats resource.
    """

    @method_endpoint('/api/stats/active_users')
    async def active_users(self) -> List[int]:
        """
        Returns list of IDs of active users.

        :return: List of IDs of active users
        :rtype: List[int]
        """
        response: List[int] = await self._client.request(
            self._client.endpoints.active_users)
        return Utils.validate_response_data(response, fallback=[])
