"""Represents `/api/v2/abuse_requests` resource."""
from typing import Any, Dict, Optional, cast

from ..decorators import exceptions_handler, method_endpoint
from ..enums import RequestType, ResponseCode
from ..exceptions import ShikimoriAPIResponseError
from ..models import AbuseResponse
from ..utils import Utils
from .base_resource import BaseResource


class AbuseRequests(BaseResource):
    """AbuseRequests resource class.

    Used to represent `/api/v2/abuse_requests` resource
    """

    @method_endpoint('/api/v2/abuse_requests/offtopic')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def offtopic(self, comment_id: int):
        """Marks comment as offtopic.

        :param comment_id: ID of comment to mark as offtopic
        :type comment_id: int

        :return: Abuse response info
        :rtype: Optional[AbuseResponse]
        """
        data_dict = Utils.create_data_dict(comment_id=comment_id)

        response = await self._client.request(
            self._client.endpoints.abuse_offtopic,
            data=data_dict,
            request_type=RequestType.POST)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=AbuseResponse)

    @method_endpoint('/api/v2/abuse_requests/review')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def review(self,
                     comment_id: Optional[int] = None,
                     topic_id: Optional[int] = None):
        """Converts comment to review.

        :param comment_id: ID of comment for conversion to review
        :type comment_id: Optional[int]

        :param topic_id: ID of comment's topic
        :type topic_id: Optional[int]

        :return: Abuse response status
        :rtype: bool
        """
        data_dict = Utils.create_data_dict(comment_id=comment_id,
                                           topic_id=topic_id)

        response = await self._client.request(
            self._client.endpoints.abuse_review,
            data=data_dict,
            request_type=RequestType.POST)

        return Utils.validate_response_code(cast(int, response),
                                            check_code=ResponseCode.SUCCESS)

    @method_endpoint('/api/v2/abuse_requests/abuse')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def abuse(self,
                    comment_id: Optional[int] = None,
                    topic_id: Optional[int] = None,
                    reason: Optional[str] = None):
        """Creates abuse about violation of site rules.

        :param comment_id: ID of comment to create abuse request
        :type comment_id: Optional[int]

        :param topic_id: ID of comment's topic
        :type topic_id: Optional[int]

        :param reason: Additional info about violation
        :type reason: Optional[str]

        :return: Abuse response status
        :rtype: bool
        """
        data_dict = Utils.create_data_dict(comment_id=comment_id,
                                           topic_id=topic_id,
                                           reason=reason)

        response = await self._client.request(
            self._client.endpoints.abuse_violation,
            data=data_dict,
            request_type=RequestType.POST)

        return Utils.validate_response_code(cast(int, response),
                                            check_code=ResponseCode.SUCCESS)

    @method_endpoint('/api/v2/abuse_requests/spoiler')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def spoiler(self,
                      comment_id: Optional[int] = None,
                      topic_id: Optional[int] = None,
                      reason: Optional[str] = None):
        """Creates abuse about spoiler in content.

        :param comment_id: ID of comment to create abuse request
        :type comment_id: Optional[int]

        :param topic_id: ID of comment's topic
        :type topic_id: Optional[int]

        :param reason: Additional info about spoiler
        :type reason: Optional[str]

        :return: Abuse response status
        :rtype: bool
        """
        data_dict = Utils.create_data_dict(comment_id=comment_id,
                                           topic_id=topic_id,
                                           reason=reason)

        response = await self._client.request(
            self._client.endpoints.abuse_spoiler,
            data=data_dict,
            request_type=RequestType.POST)

        return Utils.validate_response_code(cast(int, response),
                                            check_code=ResponseCode.SUCCESS)
