"""Represents `/api/friends` resource."""
from loguru import logger

from ..decorators import exceptions_handler, method_endpoint
from ..enums import RequestType
from ..exceptions import ShikimoriAPIResponseError
from .base_resource import BaseResource


class Friends(BaseResource):
    """Friends resource class.

    Used to represent `/api/friends` resource
    """

    @method_endpoint('/api/friends/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def create(self, user_id: int):
        """Creates (adds) new friend by ID.

        :param user_id: ID of a user to create (add)
        :type user_id: int

        :return: Status of create (addition)
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.friend(user_id),
            request_type=RequestType.POST)

        logger.info(response)

        return True

    @method_endpoint('/api/friends/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def destroy(self, user_id: int):
        """Destroys (removes) current friend by ID.

        :param user_id: ID of a user to destroy (remove)
        :type user_id: int

        :return: Status of destroy (removal)
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.friend(user_id),
            request_type=RequestType.DELETE)

        logger.info(response)

        return True
