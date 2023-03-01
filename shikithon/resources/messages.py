"""Represents /api/messages resource."""
from typing import Any, Dict, List, Optional, Union

from ..decorators import method_endpoint
from ..enums import MessageType
from ..enums import RequestType
from ..enums import ResponseCode
from ..models import Message
from ..utils import ExperimentalUtils
from ..utils import Utils
from .base_resource import BaseResource


class Messages(BaseResource):
    """Messages resource class.

    Used to represent /api/messages resource.
    """

    @method_endpoint('/api/messages/:id')
    async def get(self, message_id: int) -> Optional[Message]:
        """Returns message info.

        :param message_id: ID of message to get info
        :type message_id: int

        :return: Message info
        :rtype: Optional[Message]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.message(message_id))
        return Utils.validate_response_data(response, data_model=Message)

    @method_endpoint('/api/messages')
    async def create(self, body: str, from_id: int,
                     to_id: int) -> Optional[Message]:
        """Creates message.

        :param body: Body of message
        :type body: str

        :param from_id: Sender ID
        :type from_id: int

        :param to_id: Reciver ID
        :type to_id: int

        :return: Created message info
        :rtype: Optional[Message]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.messages,
            data=Utils.create_data_dict(dict_name='message',
                                        body=body,
                                        from_id=from_id,
                                        kind='Private',
                                        to_id=to_id),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, data_model=Message)

    @method_endpoint('/api/messages/:id')
    async def update(self, message_id: int, body: str) -> Optional[Message]:
        """Updates message.

        :param message_id: ID of message to update
        :type message_id: int

        :param body: New body of message
        :type body: str

        :return: Updated message info or None if message cannot be updated
        :rtype: Optional[Message]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.message(message_id),
            data=Utils.create_data_dict(dict_name='message', body=body),
            request_type=RequestType.PATCH)
        return Utils.validate_response_data(response, data_model=Message)

    @method_endpoint('/api/messages/:id')
    async def delete(self, message_id: int) -> bool:
        """Deletes message.

        :param message_id: ID of message to delete
        :type message_id: int

        :return: Status of message deletion
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.message(message_id),
            request_type=RequestType.DELETE)
        return Utils.validate_response_data(
            response, response_code=ResponseCode.NO_CONTENT, fallback=False)

    @method_endpoint('/api/messages/mark_read')
    async def mark_read(self,
                        message_ids: Optional[Union[int, List[int]]] = None,
                        is_read: Optional[bool] = None) -> bool:
        """Marks read/unread selected messages.

        :param message_ids: ID(s) of messages to mark read/unread
        :type message_ids: Optional[Union[int, List[int]]]

        :param is_read: Status of message (read/unread)
        :type is_read: Optional[bool]

        :return: Status of messages read/unread
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.messages_mark_read,
            data=ExperimentalUtils.create_query_dict(ids=message_ids,
                                                     is_read=is_read),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response,
                                            response_code=ResponseCode.SUCCESS,
                                            fallback=False)

    @method_endpoint('/api/messages/read_all')
    async def read_all(self, message_type: MessageType) -> bool:
        """Reads all messages on current user's account.

        **Note:** This methods accepts as type only 'news' and
        'notifications'

        :param message_type: Type of messages to read
        :type message_type: MessageType

        :return: Status of messages read
        :rtype: bool
        """
        if not ExperimentalUtils.is_enum_passed(message_type):
            return False

        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.messages_read_all,
            data=ExperimentalUtils.create_query_dict(type=message_type),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response,
                                            response_code=ResponseCode.SUCCESS,
                                            fallback=False)

    @method_endpoint('/api/messages/delete_all')
    async def delete_all(self, message_type: MessageType) -> bool:
        """Deletes all messages on current user's account.

        **Note:** This methods accepts as type only 'news' and
        'notifications'

        :param message_type: Type of messages to delete
        :type message_type: MessageType

        :return: Status of messages deletion
        :rtype: bool
        """
        if not ExperimentalUtils.is_enum_passed(message_type):
            return False

        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.messages_delete_all,
            data=ExperimentalUtils.create_query_dict(type=message_type),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response,
                                            response_code=ResponseCode.SUCCESS,
                                            fallback=False)
