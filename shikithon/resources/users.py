"""Represents `/api/users` and `/api/v2/users` resources."""
from typing import Any, Dict, List, Optional, Union, cast

from ..decorators import exceptions_handler, method_endpoint
from ..enums import (AnimeCensorship, AnimeList, HistoryTargetType, MessageType,
                     RequestType)
from ..exceptions import ShikimoriAPIResponseError
from ..models import (Ban, ClubInfo, Favourites, History, Message,
                      UnreadMessages, User, UserInfo, UserBrief, UserList)
from ..utils import Utils
from .base_resource import BaseResource


class Users(BaseResource):
    """Users resource class.

    Used to represent `/api/users` and `/api/v2/users` resources
    """

    @method_endpoint('/api/users')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None):
        """Returns list of users.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of users
        :rtype: List[UserInfo]
        """
        query_dict = Utils.create_query_dict(page=page, limit=limit)

        response = await self._client.request(self._client.endpoints.users,
                                              query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=UserInfo)

    @method_endpoint('/api/users/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def get(self, user_id: Union[str, int]):
        """Returns info about user.

        :param user_id: User ID/Nickname to get info
        :type user_id: Union[str, int]

        :return: Info about user
        :rtype: Optional[User]
        """
        is_nickname = True if isinstance(user_id, str) else None
        query_dict = Utils.create_query_dict(is_nickname=is_nickname)

        response = await self._client.request(
            self._client.endpoints.user(user_id), query=query_dict)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=User)

    @method_endpoint('/api/users/:id/info')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def info(self, user_id: Union[str, int]):
        """Returns user's brief info.

        :param user_id: User ID/Nickname to get brief info
        :type user_id: Union[int, str]

        :return: User's brief info
        :rtype: Optional[UserBrief]
        """
        is_nickname = True if isinstance(user_id, str) else None
        query_dict = Utils.create_query_dict(is_nickname=is_nickname)

        response = await self._client.request(
            self._client.endpoints.user_info(user_id), query=query_dict)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=UserBrief)

    @method_endpoint('/api/users/whoami')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def current(self):
        """Returns brief info about current user.

        Current user evaluated depending on authorization code.

        :return: Current user brief info
        :rtype: Optional[UserBrief]
        """
        response = await self._client.request(self._client.endpoints.whoami)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=UserBrief)

    @method_endpoint('/api/users/sign_out')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def sign_out(self):
        """Sends sign out request to API.

        :return: True if request was successful, False otherwise
        :rtype: bool
        """
        response = await self._client.request(self._client.endpoints.sign_out)

        return cast(str, response) == 'signed out'

    @method_endpoint('/api/users/:id/friends')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def friends(self, user_id: Union[str, int]):
        """Returns user's friends.

        :param user_id: User ID/Nickname to get friends
        :type user_id: Union[int, str]

        :return: List of user's friends
        :rtype: List[UserInfo]
        """
        is_nickname = True if isinstance(user_id, str) else None
        query_dict = Utils.create_query_dict(is_nickname=is_nickname)

        response = await self._client.request(
            self._client.endpoints.user_friends(user_id), query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=UserInfo)

    @method_endpoint('/api/users/:id/clubs')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def clubs(self, user_id: Union[int, str]):
        """Returns user's clubs.

        :param user_id: User ID/Nickname to get clubs
        :type user_id: Union[int, str]

        :return: List of user's clubs
        :rtype: List[ClubInfo]
        """
        is_nickname = True if isinstance(user_id, str) else None
        query_dict = Utils.create_query_dict(is_nickname=is_nickname)

        response = await self._client.request(
            self._client.endpoints.user_clubs(user_id), query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=ClubInfo)

    @method_endpoint('/api/users/:id/anime_rates')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def anime_rates(self,
                          user_id: Union[int, str],
                          page: Optional[int] = None,
                          limit: Optional[int] = None,
                          status: Optional[AnimeList] = None,
                          censored: Optional[AnimeCensorship] = None):
        """Returns user's anime list.

        :param user_id: User ID/Nickname to get anime list
        :type user_id: Optional[int, str]

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param status: Status of status of anime in list
        :type status: Optional[AnimeList]

        :param censored: Type of anime censorship
        :type censored: Optional[AnimeCensorship]

        :return: User's anime list
        :rtype: List[UserList]
        """
        is_nickname = True if isinstance(user_id, str) else None
        query_dict = Utils.create_query_dict(is_nickname=is_nickname,
                                             page=page,
                                             limit=limit,
                                             status=status,
                                             censored=censored)

        response = await self._client.request(
            self._client.endpoints.user_anime_rates(user_id), query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=UserList)

    @method_endpoint('/api/users/:id/manga_rates')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def manga_rates(self,
                          user_id: Union[int, str],
                          page: Optional[int] = None,
                          limit: Optional[int] = None,
                          censored: Optional[AnimeCensorship] = None):
        """Returns user's manga list.

        :param user_id: User ID/Nickname to get manga list
        :type user_id: Union[int, str]

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param censored: Type of manga censorship
        :type censored: Optional[AnimeCensorship]

        :return: User's manga list
        :rtype: List[UserList]
        """
        is_nickname = True if isinstance(user_id, str) else None
        query_dict = Utils.create_query_dict(is_nickname=is_nickname,
                                             page=page,
                                             limit=limit,
                                             censored=censored)

        response = await self._client.request(
            self._client.endpoints.user_manga_rates(user_id), query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=UserList)

    @method_endpoint('/api/users/:id/favourites')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def favourites(self, user_id: Union[int, str]):
        """Returns user's favourites.

        :param user_id: User ID/Nickname to get favourites
        :type user_id: Union[int, str]

        :return: User's favourites
        :rtype: Optional[Favourites]
        """
        is_nickname = True if isinstance(user_id, str) else None
        query_dict = Utils.create_query_dict(is_nickname=is_nickname)

        response = await self._client.request(
            self._client.endpoints.user_favourites(user_id), query=query_dict)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Favourites)

    @method_endpoint('/api/users/:id/messages')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def messages(self,
                       user_id: Union[int, str],
                       page: Optional[int] = None,
                       limit: Optional[int] = None,
                       message_type: MessageType = MessageType.NEWS):
        """Returns current user's messages by type.

        :param user_id: Current user ID/Nickname to get messages
        :type user_id: Union[int, str]

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of page limits
        :type limit: Optional[int]

        :param message_type: Type of message
        :type message_type: MessageType

        :return: Current user's messages
        :rtype: List[Message]
        """
        is_nickname = True if isinstance(user_id, str) else None
        query_dict = Utils.create_query_dict(is_nickname=is_nickname,
                                             page=page,
                                             limit=limit,
                                             type=message_type)

        response = await self._client.request(
            self._client.endpoints.user_messages(user_id), query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Message)

    @method_endpoint('/api/users/:id/unread_messages')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def unread_messages(
            self, user_id: Union[int, str]) -> Optional[UnreadMessages]:
        """Returns current user's unread messages counter.

        :param user_id: Current user ID/Nickname to get unread messages
        :type user_id: Union[int, str]

        :return: Current user's unread messages counters
        :rtype: Optional[UnreadMessages]
        """
        is_nickname = True if isinstance(user_id, str) else None
        query_dict = Utils.create_query_dict(is_nickname=is_nickname)

        response = await self._client.request(
            self._client.endpoints.user_unread_messages(user_id),
            query=query_dict)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=UnreadMessages)

    @method_endpoint('/api/users/:id/history')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def history(self,
                      user_id: Union[int, str],
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      target_id: Optional[int] = None,
                      target_type: Optional[HistoryTargetType] = None):
        """Returns history of user.

        :param user_id: User ID/Nickname to get history
        :type user_id: Union[int, str]

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param target_id: ID of anime/manga in history
        :type target_id: Optional[int]

        :param target_type: Type of target
        :type target_type: Optional[HistoryTargetType]

        :return: User's history
        :rtype: List[History]
        """
        is_nickname = True if isinstance(user_id, str) else None
        query_dict = Utils.create_query_dict(is_nickname=is_nickname,
                                             page=page,
                                             limit=limit,
                                             target_id=target_id,
                                             target_type=target_type)

        response = await self._client.request(
            self._client.endpoints.user_history(user_id), query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=History)

    @method_endpoint('/api/users/:id/bans')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def bans(self, user_id: Union[int, str]):
        """Returns list of bans of user.

        :param user_id: User ID/Nickname to get list of bans
        :type user_id: Union[int, str]

        :return: User's bans
        :rtype: List[Ban]
        """
        is_nickname = True if isinstance(user_id, str) else None
        query_dict = Utils.create_query_dict(is_nickname=is_nickname)

        response = await self._client.request(
            self._client.endpoints.user_bans(user_id), query=query_dict)
        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Ban)

    @method_endpoint('/api/v2/users/:user_id/ignore')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def ignore(self, user_id: int):
        """Sets user as ignored.

        :param user_id: ID of topic to ignore
        :type user_id: int

        :return: True if user was ignored, False otherwise
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.user_ignore(user_id),
            request_type=RequestType.POST)

        return cast(Dict[str, Any], response).get('is_ignored') is True

    @method_endpoint('/api/v2/users/:user_id/ignore')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def unignore(self, user_id: int):
        """Sets user as unignored.

        :param user_id: ID of user to unignore
        :type user_id: int

        :return: True if user was unignored, False otherwise
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.user_ignore(user_id),
            request_type=RequestType.DELETE)

        return cast(Dict[str, Any], response).get('is_ignored') is False
