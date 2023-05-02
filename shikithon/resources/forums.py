"""Represents `/api/forums` resource."""
from typing import Any, Dict, List, cast

from ..decorators import exceptions_handler, method_endpoint
from ..exceptions import ShikimoriAPIResponseError
from ..models import Forum
from ..utils import Utils
from .base_resource import BaseResource


class Forums(BaseResource):
    """Forums resource class.

    Used to represent `/api/forums` resource
    """

    @method_endpoint('/api/forums')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self):
        """Returns list of forums.

        :returns: List of forums
        :rtype: List[Forum]
        """
        response = await self._client.request(self._client.endpoints.forums)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Forum)
