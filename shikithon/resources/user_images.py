"""Represents `/api/user_images` resource."""
from typing import Any, Dict, Optional, cast

from ..decorators import exceptions_handler, method_endpoint
from ..enums import RequestType
from ..exceptions import ShikimoriAPIResponseError
from ..models import CreatedUserImage
from ..utils import Utils
from .base_resource import BaseResource


class UserImages(BaseResource):
    """UserImages resource class.

    Used to represent `/api/user_images` resource
    """

    @method_endpoint('/api/user_images')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def create(self, image_path: str, linked_type: Optional[str] = None):
        """Creates an user image.

        :param image_path: Path or URL to image to create on server
        :type image_path: str

        :param linked_type: Type of linked image
        :type linked_type: Optional[str]

        :return: Created image info
        :rtype: Optional[CreatedUserImage]
        """
        image_data = await Utils.get_image_data(image_path)
        data_dict = Utils.create_data_dict(image=image_data,
                                           linked_type=linked_type)
        form_data = Utils.create_form_data(data_dict)

        response = await self._client.request(
            self._client.endpoints.user_images,
            form_data=form_data,
            request_type=RequestType.POST)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=CreatedUserImage)
