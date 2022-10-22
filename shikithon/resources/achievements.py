"""Represents /api/achievements resource."""

from typing import Any, Dict, List, Optional

from loguru import logger

from ..decorators import method_endpoint
from ..models import Achievement
from ..utils import Utils
from .base_resource import BaseResource


class Achievements(BaseResource):
    """Achievements resource class.

    Used to represent /api/achievements resource.
    """

    @method_endpoint('/api/achievements')
    async def get(self, user_id: int) -> Optional[List[Achievement]]:
        """
        Returns achievements of user by ID.

        :param user_id: User ID for getting achievements
        :type user_id: int

        :return: List of achievements
        :rtype: Optional[List[Achievement]]
        """
        if not isinstance(user_id, int):
            logger.error('/api/achievements accept only user_id as int')
            return None

        response: List[Dict[str, Any]] = await self.client.request(
            self.client.endpoints.achievements,
            query=Utils.generate_query_dict(user_id=user_id))
        return Utils.validate_return_data(response, data_model=Achievement)
