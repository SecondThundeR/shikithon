"""Represents /api/topics and /api/v2/topics resource."""
from typing import Any, Dict, List, Optional, Union

from ..decorators import method_endpoint
from ..decorators import protected_method
from ..enums import ForumType
from ..enums import RequestType
from ..enums import ResponseCode
from ..enums import TopicLinkedType
from ..enums import TopicType
from ..models import Topic
from ..utils import Utils
from .base_resource import BaseResource


class Topics(BaseResource):
    """Topics resource class.

    Used to represent /api/topics and /api/v2/topics resource.
    """

    @method_endpoint('/api/topics')
    async def get_all(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      forum: Optional[str] = None,
                      linked_id: Optional[int] = None,
                      linked_type: Optional[str] = None,
                      topic_type: Optional[str] = None) -> List[Topic]:
        """
        Returns list of topics.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param forum: Number of results limit
        :type forum: Optional[str]

        :param linked_id: ID of linked topic (Used together with linked_type)
        :type linked_id: Optional[int]

        :param linked_type: Type of linked topic (Used together with linked_id)
        :type linked_type: Optional[str]

        :param topic_type: Type of topic.
        :type topic_type: Optional[str]

        :return: List of topics
        :rtype: List[Topic]
        """
        if not Utils.validate_enum_params({
                ForumType: forum,
                TopicLinkedType: linked_type,
                TopicType: topic_type
        }):
            return []

        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.topics,
            query=Utils.create_query_dict(page=validated_numbers['page'],
                                          limit=validated_numbers['limit'],
                                          forum=forum,
                                          linked_id=linked_id,
                                          linked_type=linked_type,
                                          type=topic_type))
        return Utils.validate_response_data(response,
                                            data_model=Topic,
                                            fallback=[])

    @method_endpoint('/api/topics/updates')
    async def updates(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None) -> List[Topic]:
        """
        Returns list of NewsTopics about database updates.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of topics
        :rtype: List[Topic]
        """
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.updates_topics,
            query=Utils.create_query_dict(page=validated_numbers['page'],
                                          limit=validated_numbers['limit']))
        return Utils.validate_response_data(response,
                                            data_model=Topic,
                                            fallback=[])

    @method_endpoint('/api/topics/hot')
    async def hot(self, limit: Optional[int] = None) -> List[Topic]:
        """
        Returns list of hot topics.

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of topics
        :rtype: List[Topic]
        """
        validated_numbers = Utils.query_numbers_validator(limit=[limit, 10])

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.hot_topics,
            query=Utils.create_query_dict(limit=validated_numbers['limit']))
        return Utils.validate_response_data(response,
                                            data_model=Topic,
                                            fallback=[])

    @method_endpoint('/api/topics/:id')
    async def get(self, topic_id: int) -> Optional[Topic]:
        """
        Returns info about topic.

        :param topic_id: ID of topic to get
        :type topic_id: int

        :return: Info about topic
        :rtype: Optional[Topic]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.topic(topic_id))
        return Utils.validate_response_data(response, data_model=Topic)

    @method_endpoint('/api/topics')
    @protected_method('_client', 'topics')
    async def create(self,
                     body: str,
                     forum_id: int,
                     title: str,
                     user_id: int,
                     linked_id: Optional[int] = None,
                     linked_type: Optional[str] = None) -> Optional[Topic]:
        """
        Creates topic.

        :param body: Body of topic
        :type body: str

        :param forum_id: ID of forum to post
        :type forum_id: int

        :param title: Title of topic
        :type title: str

        :param user_id: ID of topic creator
        :type user_id: int

        :param linked_id: ID of linked topic (Used together with linked_type)
        :type linked_type: Optional[int]

        :param linked_type: Type of linked topic (Used together with linked_id)
        :type linked_type: Optional[str]

        :return: Created topic info
        :rtype: Optional[Topic]
        """
        if not Utils.validate_enum_params({TopicLinkedType: linked_type}):
            return None

        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.topics,
            headers=self._client.authorization_header,
            data=Utils.create_data_dict(dict_name='topic',
                                        body=body,
                                        forum_id=forum_id,
                                        linked_id=linked_id,
                                        linked_type=linked_type,
                                        title=title,
                                        type=str(TopicType.REGULAR_TOPIC.value),
                                        user_id=user_id),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, data_model=Topic)

    @method_endpoint('/api/topics/:id')
    @protected_method('_client', 'topics')
    async def update(self,
                     topic_id: int,
                     body: Optional[str] = None,
                     title: Optional[str] = None,
                     linked_id: Optional[int] = None,
                     linked_type: Optional[str] = None) -> Optional[Topic]:
        """
        Updates topic.

        :param topic_id: ID of topic to update
        :type topic_id: int

        :param body: Body of topic
        :type body: Optional[str]

        :param title: Title of topic
        :type title: Optional[str]

        :param linked_id: ID of linked topic (Used together with linked_type)
        :type linked_type: Optional[int]

        :param linked_type: Type of linked topic (Used together with linked_id)
        :type linked_type: Optional[str]

        :return: Updated topic info
        :rtype: Optional[Topic]
        """
        if not Utils.validate_enum_params({TopicLinkedType: linked_type}):
            return None

        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.topic(topic_id),
            headers=self._client.authorization_header,
            data=Utils.create_data_dict(dict_name='topic',
                                        body=body,
                                        linked_id=linked_id,
                                        linked_type=linked_type,
                                        title=title),
            request_type=RequestType.PATCH)
        return Utils.validate_response_data(response,
                                            response_code=ResponseCode.SUCCESS,
                                            data_model=Topic)

    @method_endpoint('/api/topics/:id')
    @protected_method('_client', 'topics', fallback=False)
    async def delete(self, topic_id: int) -> bool:
        """
        Deletes topic.

        :param topic_id: ID of topic to delete
        :type topic_id: int

        :return: Status of topic deletion
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.topic(topic_id),
            headers=self._client.authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_response_data(response, fallback=False)

    @method_endpoint('/api/v2/topics/:topic_id/ignore')
    @protected_method('_client', 'topics', fallback=False)
    async def ignore(self, topic_id: int) -> bool:
        """
        Set topic as ignored.

        :param topic_id: ID of topic to ignore
        :type topic_id: int

        :return: True if topic was ignored, False otherwise
        :rtype: bool
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.topic_ignore(topic_id),
            headers=self._client.authorization_header,
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, fallback=False) is True

    @method_endpoint('/api/v2/topics/:topic_id/ignore')
    @protected_method('_client', 'topics', fallback=True)
    async def unignore(self, topic_id: int) -> bool:
        """
        Set topic as unignored.

        :param topic_id: ID of topic to unignore
        :type topic_id: int

        :return: True if topic was unignored, False otherwise
        :rtype: bool
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.topic_ignore(topic_id),
            headers=self._client.authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_response_data(response, fallback=True) is False
