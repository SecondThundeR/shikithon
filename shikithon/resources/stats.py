"""Represents `/api/stats` resource."""
from typing import List, cast

from ..decorators import exceptions_handler, method_endpoint
from ..exceptions import ShikimoriAPIResponseError
from .base_resource import BaseResource


class Stats(BaseResource):
    """Stats resource class.

    Used to represent `/api/stats` resource
    """

    @method_endpoint('/api/stats/active_users')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def active_users(self):
        """Returns list of IDs of active users.

        :return: List of IDs of active users
        :rtype: List[int]
        """
        response = await self._client.request(
            self._client.endpoints.active_users)

        return cast(List[int], response)
