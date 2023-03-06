"""Represents /api/achievements resource."""

from typing import Any, Dict, List

from ..decorators import exceptions_handler
from ..decorators import method_endpoint
from ..exceptions import ShikimoriAPIResponseError
from ..models import Achievement
from ..utils import ExperimentalUtils
from .base_resource import BaseResource


class Achievements(BaseResource):
    """Achievements resource class.

    Used to represent /api/achievements resource.
    """

    @method_endpoint('/api/achievements')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get(self, user_id: int):
        """Returns list of user achievements.

        :param user_id: User ID for getting achievements
        :type user_id: int

        :return: List of achievements
        :rtype: List[Achievement]
        """
        query_dict = ExperimentalUtils.create_query_dict(user_id=user_id)

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.achievements, query=query_dict)

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Achievement)
