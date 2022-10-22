"""Represents /api/users and /api/v2/users resource."""
from typing import Any, Dict, List, Optional, Union

from ..decorators import method_endpoint, protected_method
from ..enums import (
    AnimeCensorship,
    AnimeList,
    MessageType,
    RequestType,
    TargetType,
)
from ..models import (
    Ban,
    Club,
    Favourites,
    History,
    Message,
    UnreadMessages,
    User,
    UserList,
)
from ..utils import Utils
from .base_resource import BaseResource


class Users(BaseResource):
    """Users resource class.

    Used to represent /api/users and /api/v2/users resource.
    """

    @method_endpoint('/api/users')
    async def get_all(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None) -> Optional[List[User]]:
        """
        Returns list of users.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of users
        :rtype: Optional[List[User]]
        """
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 100],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.users,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit']))
        return Utils.validate_return_data(response, data_model=User)

    @method_endpoint('/api/users/:id')
    async def get(self,
                  user_id: Union[str, int],
                  is_nickname: Optional[bool] = None) -> Optional[User]:
        """
        Returns info about user.

        :param user_id: User ID/Nickname to get info
        :type user_id: Union[str, int]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: Info about user
        :rtype: Optional[User]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.user(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=User)

    @method_endpoint('/api/users/:id/info')
    async def info(self,
                   user_id: Union[str, int],
                   is_nickname: Optional[bool] = None) -> Optional[User]:
        """
        Returns user's brief info.

        :param user_id: User ID/Nickname to get brief info
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: User's brief info
        :rtype: Optional[User]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.user_info(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=User)

    @method_endpoint('/api/users/whoami')
    @protected_method(
        '_client',)
    async def current(self) -> Optional[User]:
        """
        Returns brief info about current user.

        Current user evaluated depending on authorization code.

        :return: Current user brief info
        :rtype: Optional[User]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.whoami,
            headers=self._client.authorization_header)
        return Utils.validate_return_data(response, data_model=User)

    @method_endpoint('/api/users/sign_out')
    @protected_method(
        '_client',)
    async def sign_out(self):
        """Sends sign out request to API."""
        await self._client.request(self._client.endpoints.sign_out,
                                   headers=self._client.authorization_header)

    @method_endpoint('/api/users/:id/friends')
    async def friends(
            self,
            user_id: Union[str, int],
            is_nickname: Optional[bool] = None) -> Optional[List[User]]:
        """
        Returns user's friends.

        :param user_id: User ID/Nickname to get friends
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: List of user's friends
        :rtype: Optional[List[User]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.user_friends(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=User)

    @method_endpoint('/api/users/:id/clubs')
    async def clubs(self,
                    user_id: Union[int, str],
                    is_nickname: Optional[bool] = None) -> Optional[List[Club]]:
        """
        Returns user's clubs.

        :param user_id: User ID/Nickname to get clubs
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: List of user's clubs
        :rtype: Optional[List[Club]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.user_clubs(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=Club)

    @method_endpoint('/api/users/:id/anime_rates')
    async def anime_rates(
            self,
            user_id: Union[int, str],
            is_nickname: Optional[bool] = None,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            status: Optional[str] = None,
            censored: Optional[str] = None) -> Optional[List[UserList]]:
        """
        Returns user's anime list.

        :param user_id: User ID/Nickname to get anime list
        :type user_id: Optional[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param status: Status of status of anime in list
        :type status: Optional[str]

        :param censored: Type of anime censorship
        :type censored: Optional[str]

        :return: User's anime list
        :rtype: Optional[List[UserList]]
        """
        if not Utils.validate_enum_params({
                AnimeList: status,
                AnimeCensorship: censored
        }):
            return None

        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 5000],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.user_anime_rates(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            status=status,
                                            censored=censored))
        return Utils.validate_return_data(response, data_model=UserList)

    @method_endpoint('/api/users/:id/manga_rates')
    async def manga_rates(
            self,
            user_id: Union[int, str],
            is_nickname: Optional[bool] = None,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            censored: Optional[str] = None) -> Optional[List[UserList]]:
        """
        Returns user's manga list.

        :param user_id: User ID/Nickname to get manga list
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param censored: Type of manga censorship
        :type censored: Optional[str]

        :return: User's manga list
        :rtype: Optional[List[UserList]]
        """
        if not Utils.validate_enum_params({AnimeCensorship: censored}):
            return None

        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 5000],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.user_manga_rates(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            censored=censored))
        return Utils.validate_return_data(response, data_model=UserList)

    @method_endpoint('/api/users/:id/favourites')
    async def favourites(
            self,
            user_id: Union[int, str],
            is_nickname: Optional[bool] = None) -> Optional[Favourites]:
        """
        Returns user's favourites.

        :param user_id: User ID/Nickname to get favourites
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: User's favourites
        :rtype: Optional[Favourites]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.user_favourites(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=Favourites)

    @method_endpoint('/api/users/:id/messages')
    @protected_method('_client', 'messages')
    async def messages(
            self,
            user_id: Union[int, str],
            is_nickname: Optional[bool] = None,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            message_type: str = MessageType.NEWS.value
    ) -> Optional[List[Message]]:
        """
        Returns current user's messages by type.

        :param user_id: Current user ID/Nickname to get messages
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of page limits
        :type limit: Optional[int]

        :param message_type: Type of message
        :type message_type: str

        :return: Current user's messages
        :rtype: Optional[List[Message]]
        """
        if not Utils.validate_enum_params({MessageType: message_type}):
            return None

        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 100],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.user_messages(user_id),
            headers=self._client.authorization_header,
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            type=message_type))
        return Utils.validate_return_data(response, data_model=Message)

    @method_endpoint('/api/users/:id/unread_messages')
    @protected_method('_client', 'messages')
    async def unread_messages(
            self,
            user_id: Union[int, str],
            is_nickname: Optional[bool] = None) -> Optional[UnreadMessages]:
        """
        Returns current user's unread messages counter.

        :param user_id: Current user ID/Nickname to get unread messages
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: Current user's unread messages counters
        :rtype: Optional[UnreadMessages]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.user_unread_messages(user_id),
            headers=self._client.authorization_header,
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=UnreadMessages)

    @method_endpoint('/api/users/:id/history')
    async def history(
            self,
            user_id: Union[int, str],
            is_nickname: Optional[bool] = None,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            target_id: Optional[int] = None,
            target_type: Optional[str] = None) -> Optional[List[History]]:
        """
        Returns history of user.

        :param user_id: User ID/Nickname to get history
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param target_id: ID of anime/manga in history
        :type target_id: Optional[int]

        :param target_type: Type of target (Anime/Manga)
        :type target_type: Optional[str]

        :return: User's history
        :rtype: Optional[List[History]]
        """
        if not Utils.validate_enum_params({TargetType: target_type}):
            return None

        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 100],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.user_history(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            target_id=target_id,
                                            target_type=target_type))
        return Utils.validate_return_data(response, data_model=History)

    @method_endpoint('/api/users/:id/bans')
    async def bans(self,
                   user_id: Union[int, str],
                   is_nickname: Optional[bool] = None) -> Optional[List[Ban]]:
        """
        Returns list of bans of user.

        :param user_id: User ID/Nickname to get list of bans
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: User's bans
        :rtype: Optional[List[Ban]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.user_bans(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=Ban)

    @method_endpoint('/api/v2/users/:user_id/ignore')
    @protected_method('_client', 'ignores')
    async def ignore(self, user_id: int) -> bool:
        """
        Set user as ignored.

        :param user_id: ID of topic to ignore
        :type user_id: int

        :return: True if user was ignored, False otherwise
        :rtype: bool
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.user_ignore(user_id),
            headers=self._client.authorization_header,
            request_type=RequestType.POST)
        return Utils.validate_return_data(response) is True

    @method_endpoint('/api/v2/users/:user_id/ignore')
    @protected_method('_client', 'ignores')
    async def unignore(self, user_id: int) -> bool:
        """
        Set user as unignored.

        :param user_id: ID of user to unignore
        :type user_id: int

        :return: True if user was unignored, False otherwise
        :rtype: bool
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.user_ignore(user_id),
            headers=self._client.authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_return_data(response) is False