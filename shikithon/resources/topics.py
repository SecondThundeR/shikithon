"""Represents `/api/topics` and `/api/v2/topics` resources."""
from typing import Any, Dict, List, Optional, cast

from loguru import logger

from ..decorators import exceptions_handler, method_endpoint
from ..enums import RequestType, TopicForumType, TopicLinkedType, TopicType
from ..exceptions import ShikimoriAPIResponseError
from ..models import Topic, TopicUpdate
from ..utils import Utils
from .base_resource import BaseResource

DICT_NAME = 'topic'


class Topics(BaseResource):
    """Topics resource class.

    Used to represent `/api/topics` and `/api/v2/topics` resources
    """

    @method_endpoint('/api/topics')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      forum: Optional[TopicForumType] = None,
                      linked_id: Optional[int] = None,
                      linked_type: Optional[TopicLinkedType] = None,
                      topic_type: Optional[TopicType] = None):
        """Returns list of topics.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param forum: Type of forum
        :type forum: Optional[TopicForumType]

        :param linked_id: ID of linked topic (Used together with linked_type)
        :type linked_id: Optional[int]

        :param linked_type: Type of linked topic (Used together with linked_id)
        :type linked_type: Optional[TopicLinkedType]

        :param topic_type: Type of topic
        :type topic_type: Optional[TopicType]

        :return: List of topics
        :rtype: List[Topic]
        """
        data_dict = Utils.create_query_dict(page=page,
                                            limit=limit,
                                            forum=forum,
                                            linked_id=linked_id,
                                            linked_type=linked_type,
                                            type=topic_type)

        response = await self._client.request(self._client.endpoints.topics,
                                              query=data_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Topic)

    @method_endpoint('/api/topics/updates')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def updates(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None):
        """Returns list of NewsTopics about database updates.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of topic updates
        :rtype: List[TopicUpdate]
        """
        query_dict = Utils.create_query_dict(page=page, limit=limit)

        response = await self._client.request(
            self._client.endpoints.updates_topics, query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=TopicUpdate)

    @method_endpoint('/api/topics/hot')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def hot(self, limit: Optional[int] = None):
        """Returns list of hot topics.

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of topics
        :rtype: List[Topic]
        """
        query_dict = Utils.create_query_dict(limit=limit)

        response = await self._client.request(self._client.endpoints.hot_topics,
                                              query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Topic)

    @method_endpoint('/api/topics/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def get(self, topic_id: int):
        """Returns info about topic.

        :param topic_id: ID of topic to get
        :type topic_id: int

        :return: Info about topic
        :rtype: Optional[Topic]
        """
        response = await self._client.request(
            self._client.endpoints.topic(topic_id))

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Topic)

    @method_endpoint('/api/topics')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def create(self,
                     body: str,
                     forum_id: int,
                     title: str,
                     user_id: int,
                     linked_id: Optional[int] = None,
                     linked_type: Optional[TopicLinkedType] = None):
        """Creates topic.

        :param body: Body of topic
        :type body: str

        :param forum_id: ID of forum to post
        :type forum_id: int

        :param title: Title of topic
        :type title: str

        :param user_id: ID of topic creator
        :type user_id: int

        :param linked_id: ID of linked topic (Used together with linked_type)
        :type linked_id: Optional[int]

        :param linked_type: Type of linked topic (Used together with linked_id)
        :type linked_type: Optional[TopicLinkedType]

        :return: Created topic info
        :rtype: Optional[Topic]
        """
        data_dict = Utils.create_data_dict(dict_name=DICT_NAME,
                                           body=body,
                                           forum_id=forum_id,
                                           linked_id=linked_id,
                                           linked_type=linked_type,
                                           title=title,
                                           type=TopicType.REGULAR_TOPIC,
                                           user_id=user_id)

        response = await self._client.request(self._client.endpoints.topics,
                                              data=data_dict,
                                              request_type=RequestType.POST)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Topic)

    @method_endpoint('/api/topics/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def update(self,
                     topic_id: int,
                     body: Optional[str] = None,
                     title: Optional[str] = None,
                     linked_id: Optional[int] = None,
                     linked_type: Optional[TopicLinkedType] = None):
        """Updates topic.

        :param topic_id: ID of topic to update
        :type topic_id: int

        :param body: Body of topic
        :type body: Optional[str]

        :param title: Title of topic
        :type title: Optional[str]

        :param linked_id: ID of linked topic (Used together with linked_type)
        :type linked_id: Optional[int]

        :param linked_type: Type of linked topic (Used together with linked_id)
        :type linked_type: Optional[TopicLinkedType]

        :return: Updated topic info
        :rtype: Optional[Topic]
        """
        data_dict = Utils.create_data_dict(dict_name=DICT_NAME,
                                           body=body,
                                           linked_id=linked_id,
                                           linked_type=linked_type,
                                           title=title)

        response = await self._client.request(
            self._client.endpoints.topic(topic_id),
            data=data_dict,
            request_type=RequestType.PATCH)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Topic)

    @method_endpoint('/api/topics/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def delete(self, topic_id: int):
        """Deletes topic.

        :param topic_id: ID of topic to delete
        :type topic_id: int

        :return: Status of topic deletion
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.topic(topic_id),
            request_type=RequestType.DELETE)

        logger.info(response)

        return True

    @method_endpoint('/api/v2/topics/:topic_id/ignore')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def ignore(self, topic_id: int):
        """Sets topic as ignored.

        :param topic_id: ID of topic to ignore
        :type topic_id: int

        :return: True if topic was ignored, False otherwise
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.topic_ignore(topic_id),
            request_type=RequestType.POST)

        return cast(Dict[str, Any], response).get('is_ignored', None) is True

    @method_endpoint('/api/v2/topics/:topic_id/ignore')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def unignore(self, topic_id: int):
        """Sets topic as unignored.

        :param topic_id: ID of topic to unignore
        :type topic_id: int

        :return: True if topic was unignored, False otherwise
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.topic_ignore(topic_id),
            request_type=RequestType.DELETE)

        return cast(Dict[str, Any], response).get('is_ignored', None) is False
