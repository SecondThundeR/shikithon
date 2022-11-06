"""Represents /api/styles resource."""
from typing import Any, Dict, Optional

from loguru import logger

from ..decorators import method_endpoint
from ..enums import OwnerType
from ..enums import RequestType
from ..models import Style
from ..utils import Utils
from .base_resource import BaseResource


class Styles(BaseResource):
    """Styles resource class.

    Used to represent /api/styles resource.
    """

    @method_endpoint('/api/styles/:id')
    async def get(self, style_id: int) -> Optional[Style]:
        """
        Returns info about style.

        :param style_id: Style ID to get info
        :type style_id: int

        :return: Info about style
        :rtype: Optional[Style]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.style(style_id))
        return Utils.validate_response_data(response, data_model=Style)

    @method_endpoint('/api/styles/preview')
    async def preview(self, css: str) -> Optional[Style]:
        """
        Previews style with passed CSS code.

        :param css: CSS code to preview
        :type css: str

        :return: Info about previewed style
        :rtype: Optional[Style]
        """
        if not css:
            logger.warning('No CSS code passed to preview')
            return None

        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.style_preview,
            headers=self._client.authorization_header,
            data=Utils.create_data_dict(dict_name='style', css=css),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, data_model=Style)

    @method_endpoint('/api/styles')
    async def create(self, css: str, name: str, owner_id: int,
                     owner_type: str) -> Optional[Style]:
        """
        Creates new style.

        :param css: CSS code for style
        :type css: str

        :param name: Style name
        :type name: str

        :param owner_id: User/Club ID for style ownership
        :type owner_id: int

        :param owner_type: Type of owner (User/Club)
        :type owner_type: str

        :return: Info about previewed style
        :rtype: Optional[Style]
        """
        if not Utils.validate_enum_params({OwnerType: owner_type}):
            return None

        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.styles,
            headers=self._client.authorization_header,
            data=Utils.create_data_dict(dict_name='style',
                                        css=css,
                                        name=name,
                                        owner_id=owner_id,
                                        owner_type=owner_type),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, data_model=Style)

    @method_endpoint('/api/styles/:id')
    async def update(self,
                     style_id: int,
                     css: Optional[str] = None,
                     name: Optional[str] = None) -> Optional[Style]:
        """
        Updates existing style.

        :param style_id: ID of existing style for edit
        :type style_id: int

        :param css: New CSS code for style
        :type css: Optional[str]

        :param name: New style name
        :type name: Optional[str]

        :return: Info about updated style
        :rtype: Optional[Style]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.style(style_id),
            headers=self._client.authorization_header,
            data=Utils.create_data_dict(dict_name='style', css=css, name=name),
            request_type=RequestType.PATCH)
        return Utils.validate_response_data(response, data_model=Style)
