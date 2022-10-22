"""Represents /api/forums resource."""
from typing import Any, Dict, List, Optional

from ..decorators import method_endpoint
from ..models import Forum
from ..utils import Utils
from .base_resource import BaseResource


class Forums(BaseResource):
    """Forums resource class.

    Used to represent /api/forums resource.
    """

    @method_endpoint('/api/forums')
    async def get(self) -> Optional[List[Forum]]:
        """
        Returns list of forums.

        :returns: List of forums
        :rtype: Optional[List[Forum]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.forums)
        return Utils.validate_return_data(response, data_model=Forum)