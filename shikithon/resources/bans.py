"""Represents `/api/bans` resource."""
from typing import Any, Dict, List, Optional, cast

from ..decorators import exceptions_handler, method_endpoint
from ..exceptions import ShikimoriAPIResponseError
from ..models import Ban
from ..utils import Utils
from .base_resource import BaseResource


class Bans(BaseResource):
    """Bans resource class.

    Used to represent `/api/bans` resource
    """

    @method_endpoint('/api/bans')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None):
        """Returns list of recent bans on Shikimori.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of recent bans
        :rtype: List[Ban]
        """
        query_dict = Utils.create_query_dict(page=page, limit=limit)

        response = await self._client.request(self._client.endpoints.bans_list,
                                              query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Ban)
