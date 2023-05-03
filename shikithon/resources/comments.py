"""Represents `/api/comments` resource."""
from typing import Any, Dict, List, Optional, cast

from loguru import logger

from ..decorators import exceptions_handler, method_endpoint
from ..enums import CommentableCreateType, CommentableType, RequestType
from ..exceptions import ShikimoriAPIResponseError
from ..models import Comment
from ..utils import Utils
from .base_resource import BaseResource

DICT_NAME = 'comment'


class Comments(BaseResource):
    """Comments resource class.

    Used to represent `/api/comments` resource
    """

    @method_endpoint('/api/comments')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self,
                      commentable_id: int,
                      commentable_type: CommentableType,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      desc: Optional[int] = None):
        """Returns list of comments.

        :param commentable_id: ID of entity to get comment
        :type commentable_id: int

        :param commentable_type: Type of entity to get comment
        :type commentable_type: CommentableType

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param desc: Status of description in request. Can be 1 or 0
        :type desc: Optional[int]

        :return: List of comments
        :rtype: List[Comment]
        """
        query_dict = Utils.create_query_dict(page=page,
                                             limit=limit,
                                             commentable_id=commentable_id,
                                             commentable_type=commentable_type,
                                             desc=desc)

        response = await self._client.request(self._client.endpoints.comments,
                                              query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Comment)

    @method_endpoint('/api/comments/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def get(self, comment_id: int):
        """Returns comment info.

        :param comment_id: ID of comment
        :type comment_id: int

        :return: Comment info
        :rtype: Optional[Comment]
        """
        response = await self._client.request(
            self._client.endpoints.comment(comment_id))

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Comment)

    @method_endpoint('/api/comments')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def create(self,
                     body: str,
                     commentable_id: int,
                     commentable_type: CommentableCreateType,
                     is_offtopic: Optional[bool] = None,
                     broadcast: Optional[bool] = None) -> Optional[Comment]:
        """Creates comment.

        When commentable_type set to other than Topic/User,
        comment is attached to commentable main topic

        :param body: Body of comment
        :type body: str

        :param commentable_id: ID of entity to comment on
        :type commentable_id: int

        :param commentable_type: Type of entity to comment on
        :type commentable_type: CommentableCreateType

        :param is_offtopic: Status of offtopic
        :type is_offtopic: Optional[bool]

        :param broadcast: Broadcast comment in club’s topic status
        :type broadcast: Optional[bool]

        :return: Created comment info
        :rtype: Optional[Comment]
        """
        data_dict = Utils.create_data_dict(dict_name=DICT_NAME,
                                           body=body,
                                           commentable_id=commentable_id,
                                           commentable_type=commentable_type,
                                           is_offtopic=is_offtopic)

        if isinstance(broadcast, bool):
            logger.debug('Adding a broadcast value to a data_dict')
            data_dict['broadcast'] = broadcast

        response = await self._client.request(self._client.endpoints.comments,
                                              data=data_dict,
                                              request_type=RequestType.POST)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Comment)

    @method_endpoint('/api/comments/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def update(self, comment_id: int, body: str):
        """Updates comment.

        To change is_offtopic field,
        use /api/v2/abuse_requests method

        :param comment_id: ID of comment to update
        :type comment_id: int

        :param body: New body of comment
        :type body: str

        :return: Updated comment info
        :rtype: Optional[Comment]
        """
        data_dict = Utils.create_data_dict(dict_name=DICT_NAME, body=body)

        response = await self._client.request(
            self._client.endpoints.comment(comment_id),
            data=data_dict,
            request_type=RequestType.PATCH)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Comment)

    @method_endpoint('/api/comments/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def delete(self, comment_id: int):
        """Deletes comment.

        Instead of returning just response code,
        API method returns dictionary with "notice"
        field, so it's being logged out with INFO level

        :param comment_id: ID of comment to delete
        :type comment_id: int

        :return: Status of comment deletion
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.comment(comment_id),
            request_type=RequestType.DELETE)

        logger.info(response)

        return True
