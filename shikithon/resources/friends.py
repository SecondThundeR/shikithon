"""Represents /api/friends resource."""
from typing import Any, Dict, Union

from ..decorators import method_endpoint
from ..decorators import protected_method
from ..enums import RequestType
from ..utils import Utils
from .base_resource import BaseResource


class Friends(BaseResource):
    """Friends resource class.

    Used to represent /api/friends resource.
    """

    @method_endpoint('/api/friends/:id')
    @protected_method('_client', 'friends')
    async def create(self, friend_id: int):
        """
        Creates (adds) new friend by ID.

        :param friend_id: ID of a friend to create (add)
        :type friend_id: int

        :return: Status of create (addition)
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.friend(friend_id),
            headers=self._client.authorization_header,
            request_type=RequestType.POST)
        return Utils.validate_response_data(response)

    @method_endpoint('/api/friends/:id')
    @protected_method('_client', 'friends')
    async def destroy(self, friend_id: int):
        """
        Destroys (removes) current friend by ID.

        :param friend_id: ID of a friend to destroy (remove)
        :type friend_id: int

        :return: Status of destroy (removal)
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.friend(friend_id),
            headers=self._client.authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_response_data(response)
