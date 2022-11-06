"""Represents /api/user_rates and /api/v2/user_rates resource."""
from typing import Any, Dict, List, Optional, Union

from loguru import logger

from ..decorators import method_endpoint
from ..decorators import protected_method
from ..enums import RequestType
from ..enums import ResponseCode
from ..enums import UserRateStatus
from ..enums import UserRateTarget
from ..enums import UserRateType
from ..models import UserRate
from ..utils import Utils
from .base_resource import BaseResource


class UserRates(BaseResource):
    """UserRates resource class.

    Used to represent /api/user_rates and /api/v2/user_rates resource.
    """

    @method_endpoint('/api/v2/user_rates')
    async def get_all(self,
                      user_id: int,
                      target_id: Optional[int] = None,
                      target_type: Optional[str] = None,
                      status: Optional[str] = None,
                      page: Optional[int] = None,
                      limit: Optional[int] = None) -> List[UserRate]:
        """
        Returns list of user rates.

        **Note:** When passing target_id, target_type is required.

        Also there is a strange API behavior, so when pass nothing,
        endpoint not working.
        However, docs shows that page/limit ignored when user_id is set (bruh)

        :param user_id: ID of user to get rates for
        :type user_id: int

        :param target_id: ID of anime/manga to get rates for
        :type target_id: Optional[int]

        :param target_type: Type of target_id to get rates for
        :type target_type: Optional[str]

        :param status: Status of target_type to get rates for
        :type target_type: Optional[str]

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
            (This field is ignored when user_id is set)
        :type limit: Optional[int]

        :return: List with info about user rates
        :rtype: List[UserRate]
        """
        if target_id is not None and target_type is None:
            logger.warning('target_type is required when passing target_id')
            return []

        if not Utils.validate_enum_params({
                UserRateTarget: target_type,
                UserRateStatus: status
        }):
            return []

        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 1000],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.user_rates,
            query=Utils.create_query_dict(user_id=user_id,
                                          target_id=target_id,
                                          target_type=target_type,
                                          status=status,
                                          page=validated_numbers['page'],
                                          limit=validated_numbers['limit']))
        return Utils.validate_response_data(response,
                                            data_model=UserRate,
                                            fallback=[])

    @method_endpoint('/api/v2/user_rates/:id')
    async def get(self, rate_id: int) -> Optional[UserRate]:
        """
        Returns info about user rate.

        :param rate_id: ID of rate to get
        :type rate_id: int

        :return: Info about user rate
        :rtype: Optional[UserRate]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.user_rate(rate_id))
        return Utils.validate_response_data(response, data_model=UserRate)

    @method_endpoint('/api/v2/user_rates')
    @protected_method('_client', 'user_rates')
    async def create(self,
                     user_id: int,
                     target_id: int,
                     target_type: str,
                     status: Optional[str] = None,
                     score: Optional[int] = None,
                     chapters: Optional[int] = None,
                     episodes: Optional[int] = None,
                     volumes: Optional[int] = None,
                     rewatches: Optional[int] = None,
                     text: Optional[str] = None) -> Optional[UserRate]:
        """
        Creates new user rate and return info about it.

        :param user_id: ID of user to create user rate for
        :type user_id: int

        :param target_id: ID of target to create user rate for
        :type target_id: int

        :param target_type: Type of target_id to create user rate for
            (Anime or Manga)
        :type target_type: str

        :param status: Status of target
        :type status: Optional[str]

        :param score: Score of target
        :type score: Optional[int]

        :param chapters: Watched/read chapters of target
        :type chapters: Optional[int]

        :param episodes: Watched/read episodes of target
        :type episodes: Optional[int]

        :param volumes: Watched/read volumes of target
        :type volumes: Optional[int]

        :param rewatches: Number of target rewatches
        :type rewatches: Optional[int]

        :param text: Text note for user rate
        :type text: Optional[str]

        :return: Info about new user rate
        :rtype: Optional[UserRate]
        """
        if not Utils.validate_enum_params({
                UserRateTarget: target_type,
                UserRateStatus: status
        }):
            return None

        validated_numbers = Utils.query_numbers_validator(score=[score, 10])

        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.user_rates,
            headers=self._client.authorization_header,
            data=Utils.create_data_dict(dict_name='user_rate',
                                        user_id=user_id,
                                        target_id=target_id,
                                        target_type=target_type,
                                        status=status,
                                        score=validated_numbers['score'],
                                        chapters=chapters,
                                        episodes=episodes,
                                        volumes=volumes,
                                        rewatches=rewatches,
                                        text=text),
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, data_model=UserRate)

    @method_endpoint('/api/v2/user_rates/:id')
    @protected_method('_client', 'user_rates')
    async def update(self,
                     rate_id: int,
                     status: Optional[str] = None,
                     score: Optional[int] = None,
                     chapters: Optional[int] = None,
                     episodes: Optional[int] = None,
                     volumes: Optional[int] = None,
                     rewatches: Optional[int] = None,
                     text: Optional[str] = None) -> Optional[UserRate]:
        """
        Updates user rate and return new info about it.

        :param rate_id: ID of user rate to edit
        :type rate_id: int

        :param status: Status of target
        :type status: Optional[str]

        :param score: Score of target
        :type score: Optional[int]

        :param chapters: Watched/read chapters of target
        :type chapters: Optional[int]

        :param episodes: Watched/read episodes of target
        :type episodes: Optional[int]

        :param volumes: Watched/read volumes of target
        :type volumes: Optional[int]

        :param rewatches: Number of target rewatches
        :type rewatches: Optional[int]

        :param text: Text note for user rate
        :type text: Optional[str]

        :return: Info about new user rate
        :rtype: Optional[UserRate]
        """
        if not Utils.validate_enum_params({UserRateStatus: status}):
            return None

        validated_numbers = Utils.query_numbers_validator(score=[score, 10])

        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.user_rate(rate_id),
            headers=self._client.authorization_header,
            data=Utils.create_data_dict(dict_name='user_rate',
                                        status=status,
                                        score=validated_numbers['score'],
                                        chapters=chapters,
                                        episodes=episodes,
                                        volumes=volumes,
                                        rewatches=rewatches,
                                        text=text),
            request_type=RequestType.PATCH)
        return Utils.validate_response_data(response, data_model=UserRate)

    @method_endpoint('/api/v2/user_rates/:id/increment')
    @protected_method('_client', 'user_rates')
    async def increment(self, rate_id: int) -> Optional[UserRate]:
        """
        Increments user rate episode/chapters and return updated info.

        :param rate_id: ID of user rate to increment episode/chapters
        :type rate_id: int

        :return: Info about updated user rate
        :rtype: Optional[UserRate]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.user_rate_increment(rate_id),
            headers=self._client.authorization_header,
            request_type=RequestType.POST)
        return Utils.validate_response_data(response, data_model=UserRate)

    @method_endpoint('/api/v2/user_rates/:id')
    @protected_method('_client', 'user_rates', fallback=False)
    async def delete(self, rate_id: int) -> bool:
        """
        Deletes user rate.

        :param rate_id: ID of user rate to delete
        :type rate_id: int

        :return: Status of user rate deletion
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.user_rate(rate_id),
            headers=self._client.authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_response_data(
            response, response_code=ResponseCode.NO_CONTENT, fallback=False)

    @method_endpoint('/api/users_rates/:type/cleanup')
    @protected_method('_client', 'user_rates', fallback=False)
    async def delete_all(self, user_rate_type: str) -> bool:
        """
        Deletes all user rates.

        :param user_rate_type: Type of user rates to delete
        :type user_rate_type: str

        :return: Status of user rates deletion
        :rtype: bool
        """
        if not Utils.validate_enum_params({UserRateType: user_rate_type}):
            return False

        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.user_rates_cleanup(user_rate_type),
            headers=self._client.authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_response_data(response, fallback=False)

    @method_endpoint('/api/user_rates/:type/reset')
    @protected_method('_client', 'user_rates', fallback=False)
    async def reset_all(self, user_rate_type: str) -> bool:
        """
        Resets all user rates.

        :param user_rate_type: Type of user rates to reset
        :type user_rate_type: UserRateType

        :return: Status of user rates reset
        :rtype: bool
        """
        if not Utils.validate_enum_params({UserRateType: user_rate_type}):
            return False

        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.user_rates_reset(user_rate_type),
            headers=self._client.authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_response_data(response, fallback=False)
