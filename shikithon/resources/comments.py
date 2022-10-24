"""Represents /api/comments resource."""
from typing import Any, Dict, List, Optional

from loguru import logger

from ..decorators import method_endpoint
from ..decorators import protected_method
from ..enums import CommentableType
from ..enums import RequestType
from ..models import Comment
from ..utils import Utils
from .base_resource import BaseResource


class Comments(BaseResource):
    """Comments resource class.

    Used to represent /api/comments resource.
    """

    @method_endpoint('/api/comments')
    async def get_all(self,
                      commentable_id: int,
                      commentable_type: str,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      desc: Optional[int] = None) -> List[Comment]:
        """
        Returns list of comments.

        :param commentable_id: ID of entity to get comment
        :type commentable_id: int

        :param commentable_type: Type of entity to get comment
        :type commentable_type: str

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param desc: Status of description in request. Can be 1 or 0
        :type desc: Optional[int]

        :return: List of comments
        :rtype: List[Comment]
        """
        if not Utils.validate_enum_params({CommentableType: commentable_type}):
            return []

        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.comments,
            query=Utils.create_query_dict(page=validated_numbers['page'],
                                          limit=validated_numbers['limit'],
                                          commentable_id=commentable_id,
                                          commentable_type=commentable_type,
                                          desc=desc))
        return Utils.validate_response_data(response,
                                            data_model=Comment,
                                            fallback=[])

    @method_endpoint('/api/comments/:id')
    async def get(self, comment_id: int) -> Optional[Comment]:
        """
        Returns comment info.

        :param comment_id: ID of comment
        :type comment_id: int

        :return: Comment info
        :rtype: Optional[Comment]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.comment(comment_id))
        return Utils.validate_response_data(response, data_model=Comment)

    @method_endpoint('/api/comments')
    @protected_method('_client', 'comments')
    async def create(self,
                     body: str,
                     commentable_id: int,
                     commentable_type: str,
                     is_offtopic: Optional[bool] = None,
                     broadcast: Optional[bool] = None) -> Optional[Comment]:
        """
        Creates comment.

        When commentable_type set to Anime, Manga, Character or Person,
        comment is attached to commentable main topic.

        :param body: Body of comment
        :type body: str

        :param commentable_id: ID of entity to comment on
        :type commentable_id: int

        :param commentable_type: Type of entity to comment on
        :type commentable_type: str

        :param is_offtopic: Status of offtopic
        :type is_offtopic: Optional[bool]

        :param broadcast: Broadcast comment in club’s topic status
        :type broadcast: Optional[bool]

        :return: Created comment info
        :rtype: Optional[Comment]
        """
        if not Utils.validate_enum_params({CommentableType: commentable_type}):
            return None

        data_dict: Dict[str, Any] = Utils.create_data_dict(
            dict_name='comment',
            body=body,
            commentable_id=commentable_id,
            commentable_type=commentable_type,
            is_offtopic=is_offtopic)

        if broadcast:
            logger.debug('Adding a broadcast value to a data_dict')
            data_dict['broadcast'] = broadcast

        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.comments,
            headers=self._client.authorization_header,
            data=data_dict,
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, data_model=Comment)

    @method_endpoint('/api/comments/:id')
    @protected_method('_client', 'comments')
    async def update(self, comment_id: int, body: str) -> Optional[Comment]:
        """
        Updates comment.

        :param comment_id: ID of comment to update
        :type comment_id: int

        :param body: New body of comment
        :type body: str

        :return: Updated comment info
        :rtype: Optional[Comment]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.comment(comment_id),
            headers=self._client.authorization_header,
            data=Utils.create_data_dict(dict_name='comment', body=body),
            request_type=RequestType.PATCH)
        return Utils.validate_response_data(response, data_model=Comment)

    @method_endpoint('/api/comments/:id')
    @protected_method('_client', 'comments', fallback=False)
    async def delete(self, comment_id: int) -> bool:
        """
        Deletes comment.

        :param comment_id: ID of comment to delete
        :type comment_id: int

        :return: Status of comment deletion
        :rtype: bool
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.comment(comment_id),
            headers=self._client.authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_response_data(response, fallback=False)
