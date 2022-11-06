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
    @protected_method('_client', 'friends', fallback=False)
    async def create(self, user_id: int) -> bool:
        """
        Creates (adds) new friend by ID.

        :param user_id: ID of a user to create (add)
        :type user_id: int

        :return: Status of create (addition)
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.friend(user_id),
            headers=self._client.authorization_header,
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, fallback=False)

    @method_endpoint('/api/friends/:id')
    @protected_method('_client', 'friends', fallback=False)
    async def destroy(self, user_id: int) -> bool:
        """
        Destroys (removes) current friend by ID.

        :param user_id: ID of a user to destroy (remove)
        :type user_id: int

        :return: Status of destroy (removal)
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.friend(user_id),
            headers=self._client.authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_response_data(response, fallback=False)
