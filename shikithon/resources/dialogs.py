"""Represents `/api/dialogs` resource."""
from typing import Any, Dict, List, Union, cast

from loguru import logger

from ..decorators import exceptions_handler, method_endpoint
from ..enums import RequestType
from ..exceptions import ShikimoriAPIResponseError
from ..models import Dialog, Message
from ..utils import Utils
from .base_resource import BaseResource


class Dialogs(BaseResource):
    """Dialogs resource class.

    Used to represent `/api/dialogs` resource
    """

    @method_endpoint('/api/dialogs')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self):
        """Returns list of current user's dialogs.

        :return: List of dialogs
        :rtype: List[Dialog]
        """
        response = await self._client.request(self._client.endpoints.dialogs)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Dialog)

    @method_endpoint('/api/dialogs/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get(self, user_id: Union[int, str]):
        """Returns list messages with certain user.

        :param user_id: ID/Nickname of the user to get dialog
        :type user_id: Union[int, str]

        :return: List of messages
        :rtype: List[Message]
        """
        response = await self._client.request(
            self._client.endpoints.dialog(user_id))

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Message)

    @method_endpoint('/api/dialogs/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def delete(self, user_id: Union[int, str]):
        """Deletes dialog with certain user.

        Instead of returning just response code,
        API method returns dictionary with "notice"
        field, so it's being logged out with INFO level

        :param user_id: ID/Nickname of the user to delete dialog
        :type user_id: Union[int, str]

        :return: Status of message deletion
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.dialog(user_id),
            request_type=RequestType.DELETE)

        logger.info(response)

        return True
