"""Represents /api/achievements resource."""

from typing import List

from loguru import logger

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
    async def get(self, user_id: int) -> List[Achievement]:
        """Returns list of user achievements.

        :param user_id: User ID for getting achievements
        :type user_id: int

        :return: List of achievements
        :rtype: List[Achievement]
        """
        if not isinstance(user_id, int):
            logger.error('User ID cannot be other than number')
            return []

        if user_id < 0:
            logger.error('User ID cannot be negative number')
            return []

        response = await self._client.request(
            self._client.endpoints.achievements,
            query=ExperimentalUtils.create_query_dict(user_id=user_id))
        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Achievement)
