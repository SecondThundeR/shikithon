"""Represents /api/bans resource."""
from typing import Any, Dict, List, Optional

from ..decorators import method_endpoint
from ..models import Ban
from ..utils import Utils
from .base_resource import BaseResource


class Bans(BaseResource):
    """Bans resource class.

    Used to represent /api/bans resource.
    """

    @method_endpoint('/api/bans')
    async def get(self,
                  page: Optional[int] = None,
                  limit: Optional[int] = None) -> List[Ban]:
        """
        Returns list of recent bans on Shikimori.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of recent bans
        :rtype: List[Ban]
        """
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.bans_list,
            query=Utils.create_query_dict(page=validated_numbers['page'],
                                          limit=validated_numbers['limit']))
        return Utils.validate_response_data(response, data_model=Ban)
