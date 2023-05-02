"""Represents `/api/appears` resource."""
from typing import cast

from ..decorators import exceptions_handler, method_endpoint
from ..enums import RequestType, ResponseCode
from ..exceptions import ShikimoriAPIResponseError
from ..utils import Utils
from .base_resource import BaseResource


class Appears(BaseResource):
    """Appears resource class.

    Used to represent `/api/appears` resource
    """

    @method_endpoint('/api/appears')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def mark(self, *ids: str):
        """Marks comments or topics as read.

        :param ids: Tuple with IDs of comments
        or topics to mark
        :type ids: str

        :return: Status of mark
        :rtype: bool
        """
        data_dict = Utils.create_data_dict(ids=ids)

        response = await self._client.request(self._client.endpoints.appears,
                                              data=data_dict,
                                              request_type=RequestType.POST)

        return Utils.validate_response_code(cast(int, response),
                                            ResponseCode.SUCCESS)
