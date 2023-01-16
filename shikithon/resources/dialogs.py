"""Represents /api/dialogs resource."""
from typing import Any, Dict, List, Union

from ..decorators import method_endpoint
from ..enums import RequestType
from ..models import Dialog
from ..models import Message
from ..utils import Utils
from .base_resource import BaseResource


class Dialogs(BaseResource):
    """Dialogs resource class.

    Used to represent /api/dialogs resource.
    """

    @method_endpoint('/api/dialogs')
    async def get_all(self) -> List[Dialog]:
        """Returns list of current user's dialogs.

        :return: List of dialogs
        :rtype: List[Dialog]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.dialogs)
        return Utils.validate_response_data(response,
                                            data_model=Dialog,
                                            fallback=[])

    @method_endpoint('/api/dialogs/:id')
    async def get(self, user_id: Union[int, str]) -> List[Message]:
        """Returns list of current user's messages with certain user.

        :param user_id: ID/Nickname of the user to get dialog
        :type user_id: Union[int, str]

        :return: List of messages
        :rtype: List[Message]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.dialog(user_id))
        return Utils.validate_response_data(response,
                                            data_model=Message,
                                            fallback=[])

    @method_endpoint('/api/dialogs/:id')
    async def delete(self, user_id: Union[int, str]) -> bool:
        """Deletes dialog of current user with certain user.

        :param user_id: ID/Nickname of the user to delete dialog
        :type user_id: Union[int, str]

        :return: Status of message deletion
        :rtype: bool
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.dialog(user_id),
            request_type=RequestType.DELETE)
        return Utils.validate_response_data(response, fallback=False)
