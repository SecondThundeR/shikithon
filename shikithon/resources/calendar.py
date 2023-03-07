"""Represents /api/calendar resource."""
from typing import Any, Dict, List, Optional

from ..decorators import exceptions_handler
from ..decorators import method_endpoint
from ..enums import AnimeCensorship
from ..exceptions import ShikimoriAPIResponseError
from ..models import CalendarEvent
from ..utils import ExperimentalUtils
from .base_resource import BaseResource


class Calendar(BaseResource):
    """Calendar resource class.

    Used to represent /api/calendar resource.
    """

    @method_endpoint('/api/calendar')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self, censored: Optional[AnimeCensorship] = None):
        """Returns current calendar events.

        :param censored: Status of censorship for events
        :type censored: Optional[AnimeCensorship]

        :return: List of calendar events
        :rtype: List[CalendarEvent]
        """
        query_dict = ExperimentalUtils.create_query_dict(censored=censored)

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.calendar, query=query_dict)

        return ExperimentalUtils.validate_response_data(
            response, data_model=CalendarEvent)
