"""Represents `/api/messages` resource."""
from typing import Any, Dict, List, Optional, Union, cast

from ..decorators import exceptions_handler, method_endpoint
from ..enums import MessageType, RequestType, ResponseCode
from ..exceptions import ShikimoriAPIResponseError
from ..models import Message
from ..utils import Utils
from .base_resource import BaseResource

DICT_NAME = 'message'
PRIVATE_DM = 'Private'


class Messages(BaseResource):
    """Messages resource class.

    Used to represent `/api/messages` resource
    """

    @method_endpoint('/api/messages/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def get(self, message_id: int):
        """Returns message info.

        :param message_id: ID of message to get info
        :type message_id: int

        :return: Message info
        :rtype: Optional[Message]
        """
        response = await self._client.request(
            self._client.endpoints.message(message_id))

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Message)

    @method_endpoint('/api/messages')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def create(self, body: str, from_id: int,
                     to_id: int) -> Optional[Message]:
        """Creates message.

        :param body: Body of message (Need to have length >= 2)
        :type body: str

        :param from_id: Sender ID
        :type from_id: int

        :param to_id: Reciver ID
        :type to_id: int

        :return: Created message info
        :rtype: Optional[Message]
        """
        data_dict = Utils.create_data_dict(dict_name=DICT_NAME,
                                           body=body,
                                           from_id=from_id,
                                           kind=PRIVATE_DM,
                                           to_id=to_id)

        response = await self._client.request(self._client.endpoints.messages,
                                              data=data_dict,
                                              request_type=RequestType.POST)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Message)

    @method_endpoint('/api/messages/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def update(self, message_id: int, body: str):
        """Updates message.

        :param message_id: ID of message to update
        :type message_id: int

        :param body: New body of message
        :type body: str

        :return: Updated message info
        or None if message cannot be updated
        :rtype: Optional[Message]
        """
        data_dict = Utils.create_data_dict(dict_name=DICT_NAME, body=body)

        response = await self._client.request(
            self._client.endpoints.message(message_id),
            data=data_dict,
            request_type=RequestType.PATCH)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Message)

    @method_endpoint('/api/messages/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def delete(self, message_id: int):
        """Deletes message.

        :param message_id: ID of message to delete
        :type message_id: int

        :return: Status of message deletion
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.message(message_id),
            request_type=RequestType.DELETE)

        return Utils.validate_response_code(cast(int, response),
                                            check_code=ResponseCode.NO_CONTENT)

    @method_endpoint('/api/messages/mark_read')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def mark_read(self,
                        message_ids: Optional[Union[int, List[int]]] = None,
                        is_read: Optional[bool] = None):
        """Marks read/unread selected messages.

        :param message_ids: ID(s) of messages to mark read/unread
        :type message_ids: Optional[Union[int, List[int]]]

        :param is_read: Status of message (read/unread)
        :type is_read: Optional[bool]

        :return: Status of messages read/unread
        :rtype: bool
        """
        data_dict = Utils.create_query_dict(ids=message_ids, is_read=is_read)

        response = await self._client.request(
            self._client.endpoints.messages_mark_read,
            data=data_dict,
            request_type=RequestType.POST)

        return Utils.validate_response_code(cast(int, response),
                                            check_code=ResponseCode.SUCCESS)

    @method_endpoint('/api/messages/read_all')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def read_all(self, message_type: MessageType):
        """Reads all messages on current user's account.

        This method accepts as message type
        only 'news' and 'notifications'

        :param message_type: Type of messages to read
        :type message_type: MessageType

        :return: Status of messages read
        :rtype: bool
        """
        data_dict = Utils.create_query_dict(type=message_type)

        response = await self._client.request(
            self._client.endpoints.messages_read_all,
            data=data_dict,
            request_type=RequestType.POST)

        return Utils.validate_response_code(cast(int, response),
                                            check_code=ResponseCode.SUCCESS)

    @method_endpoint('/api/messages/delete_all')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def delete_all(self, message_type: MessageType):
        """Deletes all messages on current user's account.

        This method accepts as message type
        only 'news' and 'notifications'

        :param message_type: Type of messages to delete
        :type message_type: MessageType

        :return: Status of messages deletion
        :rtype: bool
        """
        data_dict = Utils.create_query_dict(type=message_type)

        response = await self._client.request(
            self._client.endpoints.messages_delete_all,
            data=data_dict,
            request_type=RequestType.POST)

        return Utils.validate_response_code(cast(int, response),
                                            check_code=ResponseCode.SUCCESS)
