"""Represents `/api/studios` resource."""
from typing import Any, Dict, List, cast

from ..decorators import exceptions_handler, method_endpoint
from ..exceptions import ShikimoriAPIResponseError
from ..models import Studio
from ..utils import Utils
from .base_resource import BaseResource


class Studios(BaseResource):
    """Studios resource class.

    Used to represent `/api/studios` resource
    """

    @method_endpoint('/api/studios')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self):
        """Returns list of studios.

        :return: List of studios
        :rtype: List[Studio]
        """
        response = await self._client.request(self._client.endpoints.studios)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Studio)
