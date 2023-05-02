"""Represents `/api/user_rates` and `/api/v2/user_rates` resources."""
from typing import Any, Dict, List, Optional, cast

from loguru import logger

from ..decorators import exceptions_handler, method_endpoint
from ..enums import (RequestType, ResponseCode, UserRateStatus, UserRateTarget,
                     UserRateType)
from ..exceptions import ShikimoriAPIResponseError
from ..models import UserRate
from ..utils import Utils
from .base_resource import BaseResource

DICT_NAME = 'user_rate'


class UserRates(BaseResource):
    """UserRates resource class.

    Used to represent `/api/user_rates` and `/api/v2/user_rates` resources
    """

    @method_endpoint('/api/v2/user_rates')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self,
                      user_id: int,
                      target_id: Optional[int] = None,
                      target_type: Optional[UserRateTarget] = None,
                      status: Optional[UserRateStatus] = None,
                      page: Optional[int] = None,
                      limit: Optional[int] = None):
        """Returns list of user rates.

        When passing target_id, target_type is required

        Also there is a strange API behavior, so when pass nothing,
        endpoint not working.
        However, docs shows that page/limit ignored when user_id is set (bruh)

        :param user_id: ID of user to get rates for
        :type user_id: int

        :param target_id: ID of anime/manga to get rates for
        :type target_id: Optional[int]

        :param target_type: Type of target_id to get rates for
        :type target_type: Optional[UserRateTarget]

        :param status: Status of target_type to get rates for
        :type status: Optional[UserRateStatus]

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
            (This field is ignored when user_id is set)
        :type limit: Optional[int]

        :return: List with info about user rates
        :rtype: List[UserRate]
        """
        query_dict = Utils.create_query_dict(user_id=user_id,
                                             target_id=target_id,
                                             target_type=target_type,
                                             status=status,
                                             page=page,
                                             limit=limit)

        response = await self._client.request(self._client.endpoints.user_rates,
                                              query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=UserRate)

    @method_endpoint('/api/v2/user_rates/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def get(self, rate_id: int):
        """Returns info about user rate.

        :param rate_id: ID of rate to get
        :type rate_id: int

        :return: Info about user rate
        :rtype: Optional[UserRate]
        """
        response = await self._client.request(
            self._client.endpoints.user_rate(rate_id))

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=UserRate)

    @method_endpoint('/api/v2/user_rates')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def create(self,
                     user_id: int,
                     target_id: int,
                     target_type: UserRateTarget,
                     status: Optional[UserRateStatus] = None,
                     score: Optional[int] = None,
                     chapters: Optional[int] = None,
                     episodes: Optional[int] = None,
                     volumes: Optional[int] = None,
                     rewatches: Optional[int] = None,
                     text: Optional[str] = None):
        """Creates new user rate and return info about it.

        :param user_id: ID of user to create user rate for
        :type user_id: int

        :param target_id: ID of target to create user rate for
        :type target_id: int

        :param target_type: Type of target_id to create user rate for
            (Anime or Manga)
        :type target_type: UserRateTarget

        :param status: Status of target
        :type status: Optional[UserRateStatus]

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
        data_dict = Utils.create_data_dict(dict_name=DICT_NAME,
                                           user_id=user_id,
                                           target_id=target_id,
                                           target_type=target_type,
                                           status=status,
                                           score=score,
                                           chapters=chapters,
                                           episodes=episodes,
                                           volumes=volumes,
                                           rewatches=rewatches,
                                           text=text)

        response = await self._client.request(self._client.endpoints.user_rates,
                                              data=data_dict,
                                              request_type=RequestType.POST)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=UserRate)

    @method_endpoint('/api/v2/user_rates/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def update(self,
                     rate_id: int,
                     status: Optional[UserRateStatus] = None,
                     score: Optional[int] = None,
                     chapters: Optional[int] = None,
                     episodes: Optional[int] = None,
                     volumes: Optional[int] = None,
                     rewatches: Optional[int] = None,
                     text: Optional[str] = None):
        """Updates user rate and return new info about it.

        :param rate_id: ID of user rate to edit
        :type rate_id: int

        :param status: Status of target
        :type status: Optional[UserRateStatus]

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
        data_dict = Utils.create_data_dict(dict_name=DICT_NAME,
                                           status=status,
                                           score=score,
                                           chapters=chapters,
                                           episodes=episodes,
                                           volumes=volumes,
                                           rewatches=rewatches,
                                           text=text)

        response = await self._client.request(
            self._client.endpoints.user_rate(rate_id),
            data=data_dict,
            request_type=RequestType.PATCH)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=UserRate)

    @method_endpoint('/api/v2/user_rates/:id/increment')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def increment(self, rate_id: int):
        """Increments user rate episode/chapters and return updated info.

        :param rate_id: ID of user rate to increment episode/chapters
        :type rate_id: int

        :return: Info about updated user rate
        :rtype: Optional[UserRate]
        """
        response = await self._client.request(
            self._client.endpoints.user_rate_increment(rate_id),
            request_type=RequestType.POST)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=UserRate)

    @method_endpoint('/api/v2/user_rates/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def delete(self, rate_id: int):
        """Deletes user rate.

        :param rate_id: ID of user rate to delete
        :type rate_id: int

        :return: Status of user rate deletion
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.user_rate(rate_id),
            request_type=RequestType.DELETE)

        return Utils.validate_response_code(cast(int, response),
                                            check_code=ResponseCode.NO_CONTENT)

    @method_endpoint('/api/user_rates/:type/cleanup')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def delete_all(self, user_rate_type: UserRateType):
        """Deletes all user rates.

        :param user_rate_type: Type of user rates to delete
        :type user_rate_type: UserRateType

        :return: Status of user rates deletion
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.user_rates_cleanup(str(user_rate_type)),
            request_type=RequestType.DELETE)

        logger.info(response)

        return True

    @method_endpoint('/api/user_rates/:type/reset')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def reset_all(self, user_rate_type: UserRateType):
        """Resets all user rates.

        :param user_rate_type: Type of user rates to reset
        :type user_rate_type: UserRateType

        :return: Status of user rates reset
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.user_rates_reset(str(user_rate_type)),
            request_type=RequestType.DELETE)

        logger.info(response)

        return True
