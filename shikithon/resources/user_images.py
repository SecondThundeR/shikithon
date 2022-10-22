"""Represents /api/user_images resource."""
from typing import Any, Dict, Optional, Union

from ..decorators import method_endpoint, protected_method
from ..enums import RequestType
from ..models import CreatedUserImage
from ..utils import Utils
from .base_resource import BaseResource


class UserImages(BaseResource):
    """UserImages resource class.

    Used to represent /api/user_images resource.
    """

    @method_endpoint('/api/user_images')
    @protected_method('_client', 'comments')
    async def create(
            self,
            image_path: str,
            linked_type: Optional[str] = None) -> Optional[CreatedUserImage]:
        """
        Creates an user image.

        :param image_path: Path or URL to image to create on server
        :type image_path: str

        :param linked_type: Type of linked image
        :type linked_type: Optional[str]

        :return: Created image info
        :rtype: Optional[CreatedUserImage]
        """
        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.user_images,
            headers=self._client.authorization_header,
            files=Utils.get_image_data(image_path),
            data=Utils.generate_data_dict(linked_type=linked_type),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response, data_model=CreatedUserImage)
