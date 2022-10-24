"""Represents /api/appears resource."""

from typing import Any, Dict, List, Union

from loguru import logger

from ..decorators import method_endpoint
from ..decorators import protected_method
from ..enums import RequestType
from ..enums import ResponseCode
from ..utils import Utils
from .base_resource import BaseResource


class Appears(BaseResource):
    """Appears resource class.

    Used to represent /api/appears resource.
    """

    @method_endpoint('/api/appears')
    @protected_method('_client', fallback=False)
    async def mark(self, ids: List[str]) -> bool:
        """
        Marks comments or topics as read.

        This method uses generate_query_dict for data dict,
        because there is no need for nested dictionary

        :param ids: IDs of comments or topics to mark
        :type ids: List[str]

        :return: Status of mark
        :rtype: bool
        """
        if not isinstance(ids, list):
            logger.error('/api/appears accept only list of ids')
            return False

        if not ids:
            logger.warning('List of ids to mark is empty')
            return False

        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.appears,
            headers=self._client.authorization_header,
            data=Utils.create_query_dict(ids=ids),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response,
                                            response_code=ResponseCode.SUCCESS,
                                            fallback=False)
