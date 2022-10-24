"""Represents /api/v2/abuse_requests resource."""
from typing import Any, Dict, List, Optional

from ..decorators import method_endpoint
from ..enums import RequestType
from ..models import AbuseResponse
from ..utils import Utils
from .base_resource import BaseResource


class AbuseRequests(BaseResource):
    """AbuseRequests resource class.

    Used to represent /api/v2/abuse_requests resource.
    """

    @method_endpoint('/api/v2/abuse_requests/offtopic')
    async def comment_offtopic(self,
                               comment_id: int) -> Optional[AbuseResponse]:
        """
        Mark comment as offtopic.

        :param comment_id: ID of comment to mark as offtopic
        :type comment_id: int

        :return: Object with info about abuse request
        :rtype: Optional[AbuseResponse]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.abuse_offtopic,
            data=Utils.create_data_dict(comment_id=comment_id),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, data_model=AbuseResponse)

    @method_endpoint('/api/v2/abuse_requests/review')
    async def comment_review(self, comment_id: int) -> Optional[AbuseResponse]:
        """
        Convert comment to review.

        :param comment_id: ID of comment to convert to review
        :type comment_id: int

        :return: Object with info about abuse request
        :rtype: Optional[AbuseResponse]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.abuse_review,
            data=Utils.create_data_dict(comment_id=comment_id),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, data_model=AbuseResponse)

    @method_endpoint('/api/v2/abuse_requests/abuse')
    async def violation_request(self, comment_id: int,
                                reason: str) -> Optional[AbuseResponse]:
        """
        Create abuse about violation of site rules

        :param comment_id: ID of comment to create abuse request
        :type comment_id: int

        :param reason: Additional info about violation
        :type reason: str

        :return: Object with info about abuse request
        :rtype: Optional[AbuseResponse]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.abuse_violation,
            data=Utils.create_data_dict(comment_id=comment_id, reason=reason),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, data_model=AbuseResponse)

    @method_endpoint('/api/v2/abuse_requests/spoiler')
    async def spoiler_abuse_request(self, comment_id: int,
                                    reason: str) -> Optional[AbuseResponse]:
        """
        Create abuse about spoiler in content.

        :param comment_id: ID of comment to create abuse request
        :type comment_id: int

        :param reason: Additional info about spoiler
        :type reason: str

        :return: Object with info about abuse request
        :rtype: Optional[AbuseResponse]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.abuse_spoiler,
            data=Utils.create_data_dict(comment_id=comment_id, reason=reason),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, data_model=AbuseResponse)
