"""Represents /api/appears resource."""

from loguru import logger

from ..decorators import exceptions_handler
from ..decorators import method_endpoint
from ..enums import RequestType
from ..enums import ResponseCode
from ..exceptions import ShikimoriAPIResponseError
from ..utils import ExperimentalUtils
from .base_resource import BaseResource


class Appears(BaseResource):
    """Appears resource class.

    Used to represent /api/appears resource.
    """

    @method_endpoint('/api/appears')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def mark(self, *ids: str):
        """Marks comments or topics as read.

        :param ids: IDs of comments or topics to mark
        :type ids: Tuple[str, ...]

        :return: Status of mark
        :rtype: bool
        """
        if not ids:
            logger.error('Cannot pass nothing as IDs to method')
            return False

        data_dict = ExperimentalUtils.create_data_dict(ids=ids)

        response = await self._client.request(self._client.endpoints.appears,
                                              data=data_dict,
                                              request_type=RequestType.POST)

        return ExperimentalUtils.validate_response_code(response,
                                                        ResponseCode.SUCCESS)
