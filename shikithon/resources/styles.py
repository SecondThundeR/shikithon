"""Represents `/api/styles` resource."""
from typing import Any, Dict, Optional, cast

from ..decorators import exceptions_handler, method_endpoint
from ..enums import RequestType, StyleOwner
from ..exceptions import ShikimoriAPIResponseError
from ..models import Style
from ..utils import Utils
from .base_resource import BaseResource

DICT_NAME = 'style'


class Styles(BaseResource):
    """Styles resource class.

    Used to represent `/api/styles` resource
    """

    @method_endpoint('/api/styles/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def get(self, style_id: int):
        """Returns info about style.

        :param style_id: Style ID to get info
        :type style_id: int

        :return: Info about style
        :rtype: Optional[Style]
        """
        response = await self._client.request(
            self._client.endpoints.style(style_id))

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Style)

    @method_endpoint('/api/styles/preview')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def preview(self, css: str):
        """Previews style with passed CSS code.

        :param css: CSS code to preview
        :type css: str

        :return: Info about previewed style
        :rtype: Optional[Style]
        """
        data_dict = Utils.create_data_dict(dict_name=DICT_NAME, css=css)

        response = await self._client.request(
            self._client.endpoints.style_preview,
            data=data_dict,
            request_type=RequestType.POST)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Style)

    @method_endpoint('/api/styles')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def create(self, css: str, name: str, owner_id: int,
                     owner_type: StyleOwner):
        """Creates new style.

        :param css: CSS code for style
        :type css: str

        :param name: Style name
        :type name: str

        :param owner_id: User/Club ID for style ownership
        :type owner_id: int

        :param owner_type: Type of owner
        :type owner_type: StyleOwner

        :return: Info about previewed style
        :rtype: Optional[Style]
        """
        data_dict = Utils.create_data_dict(dict_name=DICT_NAME,
                                           css=css,
                                           name=name,
                                           owner_id=owner_id,
                                           owner_type=owner_type)

        response = await self._client.request(self._client.endpoints.styles,
                                              data=data_dict,
                                              request_type=RequestType.POST)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Style)

    @method_endpoint('/api/styles/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def update(self,
                     style_id: int,
                     css: Optional[str] = None,
                     name: Optional[str] = None):
        """Updates existing style.

        :param style_id: ID of existing style for edit
        :type style_id: int

        :param css: New CSS code for style
        :type css: Optional[str]

        :param name: New style name
        :type name: Optional[str]

        :return: Info about updated style
        :rtype: Optional[Style]
        """
        data_dict = Utils.create_data_dict(dict_name=DICT_NAME,
                                           css=css,
                                           name=name)

        response = await self._client.request(
            self._client.endpoints.style(style_id),
            data=data_dict,
            request_type=RequestType.PATCH)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Style)
