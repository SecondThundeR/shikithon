"""Represents /api/favorites resource."""
from typing import Any, Dict, Optional

from loguru import logger

from ..decorators import exceptions_handler
from ..decorators import method_endpoint
from ..enums import FavoriteLinkedType
from ..enums import PersonKind
from ..enums import RequestType
from ..enums import ResponseCode
from ..exceptions import ShikimoriAPIResponseError
from ..utils import Utils
from .base_resource import BaseResource


class Favorites(BaseResource):
    """Favorites resource class.

    Used to represent /api/favorites resource.
    """

    @method_endpoint('/api/favorites/:linked_type/:linked_id(/:kind)')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def create(self,
                     linked_type: FavoriteLinkedType,
                     linked_id: int,
                     kind: Optional[PersonKind] = None):
        """Creates a favorite.

        :param linked_type: Type of object for making favorite
        :type linked_type: FavoriteLinkedType

        :param linked_id: ID of linked type
        :type linked_id: int

        :param kind: Kind of linked type
            (Required when linked_type is 'Person')
        :type kind: Optional[PersonKind]

        :return: Status of favorite create
        :rtype: bool
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.favorites_create(linked_type, linked_id,
                                                    kind),
            request_type=RequestType.POST)

        logger.info(response)

        return True

    @method_endpoint('/api/favorites/:linked_type/:linked_id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def destroy(self, linked_type: FavoriteLinkedType, linked_id: int):
        """Destroys a favorite.

        :param linked_type: Type of object for destroying from favorite
        :type linked_type: FavoriteLinkedType

        :param linked_id: ID of linked type
        :type linked_id: int

        :return: Status of favorite destroy
        :rtype: bool
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.favorites_destroy(linked_type, linked_id),
            request_type=RequestType.DELETE)

        logger.info(response)

        return True

    @method_endpoint('/api/favorites/:id/reorder')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def reorder(self, favorite_id: int, new_index: Optional[int] = None):
        """Reorders a favorite to the new index.

        This method requires a favorite ID,
        which cannot be retrieved through the current API methods.

        To get the favorite ID, use DevTools on the favorites page
        See https://github.com/shikimori/shikimori/issues/2655

        :param favorite_id: ID of a favorite to reorder
        :type favorite_id: int

        :param new_index: Index of a new position of favorite.
            If skipped, sets favorite to the first position
        :type new_index: Optional[int]

        :return: Status of reorder
        :rtype: bool
        """
        query_dict = Utils.create_query_dict(new_index=new_index)

        response: int = await self._client.request(
            self._client.endpoints.favorites_reorder(favorite_id),
            query=query_dict,
            request_type=RequestType.POST)

        return Utils.validate_response_code(response,
                                            check_code=ResponseCode.SUCCESS)
