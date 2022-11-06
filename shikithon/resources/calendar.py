"""Represents /api/calendar resource."""
from typing import Any, Dict, List, Optional

from ..decorators import method_endpoint
from ..enums import AnimeCensorship
from ..models import CalendarEvent
from ..utils import Utils
from .base_resource import BaseResource


class Calendar(BaseResource):
    """Calendar resource class.

    Used to represent /api/calendar resource.
    """

    @method_endpoint('/api/calendar')
    async def get(self, censored: Optional[str] = None) -> List[CalendarEvent]:
        """
        Returns current calendar events.

        :param censored: Status of censorship for events (true/false)
        :type censored: Optional[str]

        :return: List of calendar events
        :rtype: List[CalendarEvent]
        """
        if not Utils.validate_enum_params({AnimeCensorship: censored}):
            return []

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.calendar,
            query=Utils.create_query_dict(censored=censored))
        return Utils.validate_response_data(response,
                                            data_model=CalendarEvent,
                                            fallback=[])
