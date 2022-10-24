"""Represents /api/favorites resource."""
from typing import Any, Dict, Optional, Union

from ..decorators import method_endpoint
from ..decorators import protected_method
from ..enums import FavoriteLinkedType
from ..enums import PersonKind
from ..enums import RequestType
from ..enums import ResponseCode
from ..utils import Utils
from .base_resource import BaseResource


class Favorites(BaseResource):
    """Favorites resource class.

    Used to represent /api/favorites resource.
    """

    @method_endpoint('/api/favorites/:linked_type/:linked_id(/:kind)')
    @protected_method('_client', fallback=False)
    async def create(self,
                     linked_type: str,
                     linked_id: int,
                     kind: str = PersonKind.NONE.value) -> bool:
        """
        Creates a favorite.

        :param linked_type: Type of object for making favorite
        :type linked_type: str

        :param linked_id: ID of linked type
        :type linked_id: int

        :param kind: Kind of linked type
            (Required when linked_type is 'Person')
        :type kind: str

        :return: Status of favorite create
        :rtype: bool
        """
        if not Utils.validate_enum_params({
                FavoriteLinkedType: linked_type,
                PersonKind: kind
        }):
            return False

        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.favorites_create(linked_type, linked_id,
                                                    kind),
            headers=self._client.authorization_header,
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, fallback=False)

    @method_endpoint('/api/favorites/:linked_type/:linked_id')
    @protected_method('_client', fallback=False)
    async def destroy(self, linked_type: str, linked_id: int) -> bool:
        """
        Destroys a favorite.

        :param linked_type: Type of object for destroying from favorite
        :type linked_type: str

        :param linked_id: ID of linked type
        :type linked_id: int

        :return: Status of favorite destroy
        :rtype: bool
        """
        if not Utils.validate_enum_params({FavoriteLinkedType: linked_type}):
            return False

        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.favorites_destroy(linked_type, linked_id),
            headers=self._client.authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_response_data(response, fallback=False)

    @method_endpoint('/api/favorites/:id/reorder')
    @protected_method('_client', fallback=False)
    async def reorder(self,
                      favorite_id: int,
                      new_index: Optional[int] = None) -> bool:
        """
        Reorders a favorite to the new index.

        :param favorite_id: ID of a favorite to reorder
        :type favorite_id: int

        :param new_index: Index of a new position of favorite.
            If skipped, sets favorite to the first position
        :type new_index: Optional[int]

        :return: Status of reorder
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.favorites_reorder(favorite_id),
            headers=self._client.authorization_header,
            query=Utils.create_query_dict(new_index=new_index),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response,
                                            response_code=ResponseCode.SUCCESS,
                                            fallback=False)
