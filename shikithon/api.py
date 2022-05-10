""" Shikithon API Module.

This is main module with a class
for interacting with the Shikimori API.
"""
from json import dumps
from time import sleep, time
from typing import Any, Dict, List, Tuple, Union

from ratelimit import limits, sleep_and_retry
from requests import JSONDecodeError, Response, Session

from shikithon.config_cache import ConfigCache
from shikithon.decorators import protected_method
from shikithon.endpoints import Endpoints
from shikithon.enums.anime import (Censorship, Duration, Kind, MyList, Order,
                                   Rating, Status)
from shikithon.enums.history import TargetType
from shikithon.enums.message import MessageType
from shikithon.enums.request import RequestType
from shikithon.enums.response import ResponseCode
from shikithon.exceptions import (AccessTokenException, MissingAppName,
                                  MissingAuthCode, MissingClientID,
                                  MissingClientSecret, MissingConfigData,
                                  MissingScopes)
from shikithon.models.achievement import Achievement
from shikithon.models.anime import Anime
from shikithon.models.ban import Ban
from shikithon.models.calendar_event import CalendarEvent
from shikithon.models.character import Character
from shikithon.models.club import Club
from shikithon.models.creator import Creator
from shikithon.models.favourites import Favourites
from shikithon.models.franchise_tree import FranchiseTree
from shikithon.models.history import History
from shikithon.models.link import Link
from shikithon.models.message import Message
from shikithon.models.relation import Relation
from shikithon.models.screenshot import Screenshot
from shikithon.models.topic import Topic
from shikithon.models.unread_messages import UnreadMessages
from shikithon.models.user import User
from shikithon.models.user_list import UserList
from shikithon.utils import Utils

SHIKIMORI_API_URL = 'https://shikimori.one/api'
SHIKIMORI_API_URL_V2 = 'https://shikimori.one/api/v2'
SHIKIMORI_OAUTH_URL = 'https://shikimori.one/oauth'
DEFAULT_REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'
ONE_MINUTE = 60
MAX_CALLS_PER_MINUTE = 90
RATE_LIMIT_RPS_COOLDOWN = 1
TOKEN_EXPIRE_TIME = 86400


class API:
    """
    Main class for interacting with the API.
    Has most of the methods that simplify the configuration and validation
    of the object and convenient methods for getting data from the API

    **Note:** Due to problems with some methods,
    when the session header contains a User-Agent and authorization,
    __init__ sets only the User-Agent,
    and all protected methods independently
    provide a header with a token
    """

    def __init__(self, config: Dict[str, str]):
        """
        Initialization and updating of variables
        required to interact with the Shikimori API

        This magic method calls config and variables validator,
        as well as updating session object header
        and getting access/refresh tokens

        :param config: Config file for API class
        :type config: Dict[str, str]
        """
        self._endpoints: Endpoints = Endpoints(SHIKIMORI_API_URL,
                                               SHIKIMORI_API_URL_V2,
                                               SHIKIMORI_OAUTH_URL)
        self._session: Session = Session()

        self._app_name: str = ''
        self._client_id: str = ''
        self._client_secret: str = ''
        self._redirect_uri: str = ''
        self._scopes: str = ''
        self._auth_code: str = ''
        self._access_token: str = ''
        self._refresh_token: str = ''
        self._token_expire: int = -1

        self._init_config(config)

    @property
    def config(self) -> Dict[str, str]:
        """
        Returns current API variables as config dictionary.

        :return: Current API variables as config dictionary
        :rtype: Dict[str, str]
        """
        return {
            'app_name': self._app_name,
            'client_id': self._client_id,
            'client_secret': self._client_secret,
            'redirect_uri': self._redirect_uri,
            'scopes': self._scopes,
            'auth_code': self._auth_code,
            'access_token': self._access_token,
            'refresh_token': self._refresh_token,
            'token_expire': str(self._token_expire)
        }

    @config.setter
    def config(self, config: Dict[str, str]):
        """
        Sets new API variables from config dictionary.

        This method calls init_config
        to reconfigure the object

        :param config: Config dictionary
        :type config: Dict[str, str]
        """
        self._init_config(config)

    @property
    def _tokens(self) -> Tuple[str, str]:
        """
        Returns access/refresh tokens as tuple.

        :return: Access and refresh tokens tuple
        :rtype: Tuple[str, str]
        """
        return self._access_token, self._refresh_token

    @_tokens.setter
    def _tokens(self, tokens_data: Tuple[str, str]):
        """
        Sets new access/refresh tokens from tuple.

        :param tokens_data: New access and refresh tokens tuple
        :type tokens_data: Tuple[str, str]
        """
        self._access_token = tokens_data[0]
        self._refresh_token = tokens_data[1]

    @property
    def _user_agent(self) -> Dict[str, str]:
        """
        Returns current session User-Agent.

        :return: Session User-Agent
        :rtype: Dict[str, str]
        """
        return {'User-Agent': self._session.headers['User-Agent']}

    @_user_agent.setter
    def _user_agent(self, app_name: str):
        """
        Update session headers and set user agent.

        :param app_name: OAuth App name
        :type app_name: str
        """
        self._session.headers.update({'User-Agent': app_name})

    @property
    def _authorization_header(self) -> Dict[str, str]:
        """
        Returns user agent and authorization token headers dictionary.

        Needed for accessing Shikimori protected resources

        :return: Dictionary with proper user agent and autorization token
        :rtype: Dict[str, str]
        """
        header = self._user_agent
        header['Authorization'] = f'Bearer {self._access_token}'
        return header

    def _init_config(self, config: Dict[str, str]):
        """
        Special method for initializing an object.

        This method calls several methods:

        - Validation of config and variables
        - Customizing the session header user agent
        - Getting access/refresh tokens if they are missing

        :param config: Config dictionary
        :type config: Dict[str, str]
        """
        self._validate_config(config)
        self._validate_vars()
        self._user_agent = self._app_name

        if not self._access_token:
            tokens_data: Tuple[str, str] = self._get_access_token()
            self._update_tokens(tokens_data)

    def _validate_config(self, config: Dict[str, str]):
        """
        Validates passed config dictionary and sets
        API variables.

        If method detects a cached configuration file,
        replaces passed configuration dictionary
        with the cached one.

        Raises MissingConfigData if some variables
        are missing in config dictionary

        :param config: Config dictionary for validation
        :type config: Dict[str, str]

        :raises MissingConfigData: If any field is missing
            (Not raises if there is a cache config)
        """
        try:
            config_cached = False
            if ConfigCache.config_valid(config['app_name'],
                                        config['auth_code']):
                config = ConfigCache.get_config(config['app_name'])
                config_cached = True

            self._app_name: str = config['app_name']
            self._client_id: str = config['client_id']
            self._client_secret: str = config['client_secret']
            self._redirect_uri: str = config['redirect_uri']
            self._scopes: str = config['scopes']
            self._auth_code: str = config['auth_code']
            if config_cached:
                self._access_token = config['access_token']
                self._refresh_token = config['refresh_token']
                self._token_expire = int(config['token_expire'])
        except KeyError as err:
            raise MissingConfigData(
                'It is impossible to initialize an API object'
                'without missing variables. '
                'Recheck your config and try again.') from err

    def _validate_vars(self):
        """
        Validates variables and throws exception
        if some vars are set to empty string.

        **Note:** Why throwing exception without catching it?

        This decision was made in order to prevent
        future problems with the API due to incorrect variables.
        Raising exception at the beginning of initialization
        immediately indicates errors with the configuration dictionary
        and future unnecessary checks related to this variables

        Also some notes about this method:

        - If redirect URI set to empty string, set to default URI.
        - If authorization code set to empty string,
        returns URL for getting auth code.

        :raises MissingAppName: If app name is set to empty string
        :raises MissingClientID: If client ID is set to empty string
        :raises MissingClientSecret: If client secret is set to empty string
        :raises MissingScopes: If scopes is set to empty string
        :raises MissingAuthCode: If auth code is set to empty string
        """
        exception_msg: str = 'To use the Shikimori API correctly, ' \
                             'you need to pass the application '

        if not self._app_name:
            raise MissingAppName(exception_msg + 'name')

        if not self._client_id:
            raise MissingClientID(exception_msg + 'Client ID')

        if not self._client_secret:
            raise MissingClientSecret(exception_msg + 'Client Secret')

        if not self._redirect_uri:
            self._redirect_uri = DEFAULT_REDIRECT_URI

        if not self._scopes:
            raise MissingScopes(exception_msg + 'scopes')

        if not self._auth_code:
            auth_link: str = self._endpoints.authorization_link(
                self._client_id, self._redirect_uri, self._scopes)
            raise MissingAuthCode(exception_msg +
                                  'authorization code. To get one, go to '
                                  f'{auth_link}')

    def _get_access_token(self, refresh_token: bool = False) -> Tuple[str, str]:
        """
        Returns access/refresh tokens from API request.

        If refresh_token flag is set to True,
        returns refreshed access/refresh tokens.

        :param refresh_token: Flag for token refresh
        :type refresh_token: bool

        :return: New access/refresh tokens tuple
        :rtype: Tuple[str, str]

        :raises AccessTokenException: If token request failed
        """
        data: Dict[str, str] = {
            'client_id': self._client_id,
            'client_secret': self._client_secret
        }

        if refresh_token:
            data['grant_type'] = 'refresh_token'
            data['refresh_token'] = self._refresh_token
        else:
            data['grant_type'] = 'authorization_code'
            data['code'] = self._auth_code
            data['redirect_uri'] = self._redirect_uri

        oauth_json = self._request(self._endpoints.oauth_token,
                                   data=data,
                                   request_type=RequestType.POST)

        try:
            return oauth_json['access_token'], oauth_json['refresh_token']
        except KeyError as err:
            error_info = dumps(oauth_json)
            raise AccessTokenException(
                'An error occurred while receiving tokens, '
                f'here is the information from the response: {error_info}'
            ) from err

    def _update_tokens(self, tokens_data: Tuple[str, str]):
        """
        Set new tokens and update token expire time.

        **Note:** This method also updates cache config file for
        future use

        :param tokens_data: Tuple with access and refresh tokens
        :type tokens_data: Tuple[str, str]
        """
        self._tokens = tokens_data
        self._cache_config()

    def _cache_config(self):
        """Updates token expire time and caches new config."""
        self._token_expire = Utils.get_new_expire_time(TOKEN_EXPIRE_TIME)
        ConfigCache.save_config(self.config)

    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
    def _request(
        self,
        url: str,
        data: Union[None, Dict[str, str]] = None,
        headers: Union[None, Dict[str, str]] = None,
        query: Union[None, Dict[str, str]] = None,
        request_type: RequestType = RequestType.GET
    ) -> Union[List[Dict[str, Any]], Dict[str, Any], int, str]:
        """
        Create request and return response JSON.

        This method uses ratelimit library for rate limiting
        requests (Shikimori API limit: 90rpm)

        For 5rps limit, there is a check for 429 status code.
        When triggered, halt request for 0.5 second and retry

        **Note:** To address duplication of methods
        for different request methods, this method
        uses RequestType enum

        :param url: URL for making request
        :type url: str

        :param data: Request body data
        :type data: Union[None, Dict[str, str]]

        :param headers: Custom headers for request
        :type headers: Union[None, Dict[str, str]]

        :param query: Query data for request
        :type query: Union[None, Dict[str, str]]

        :param request_type: Type of current request
        :type request_type: RequestType

        :return: Response JSON, text or status code
        :rtype: Union[List[Dict[str, Any]], Dict[str, Any], str]
        """
        response: Union[Response, None] = None

        if request_type == RequestType.GET:
            response = self._session.get(url,
                                         headers=headers,
                                         params=query,
                                         data=data)
        if request_type == RequestType.POST:
            response = self._session.post(url,
                                          headers=headers,
                                          params=query,
                                          data=data)
        if request_type == RequestType.PUT:
            response = self._session.put(url,
                                         headers=headers,
                                         params=query,
                                         data=data)
        if request_type == RequestType.PATCH:
            response = self._session.patch(url,
                                           headers=headers,
                                           params=query,
                                           data=data)
        if request_type == RequestType.DELETE:
            response = self._session.delete(url,
                                            headers=headers,
                                            params=query,
                                            data=data)

        if response.status_code == ResponseCode.RETRY_LATER.value:
            sleep(RATE_LIMIT_RPS_COOLDOWN)
            return self._request(url, data, headers, query, request_type)

        try:
            if request_type != RequestType.GET:
                return response.status_code
            return response.json()
        except JSONDecodeError:
            return response.text

    def refresh_tokens(self):
        """
        Manages tokens refreshing and caching.

        This method gets new access/refresh tokens and
        updates them in current instance, as well as
        caching new config.
        """
        tokens_data: Tuple[str,
                           str] = self._get_access_token(refresh_token=True)
        self._update_tokens(tokens_data)

    def token_expired(self):
        """
        Checks if current access token is expired.

        :return: Result of token expiration check
        :rtype: bool
        """
        return int(time()) > self._token_expire

    def achievements(self, user_id: int) -> List[Achievement]:
        """
        Returns achievements of user by ID.

        :param user_id: User ID for getting achievements
        :type user_id: int

        :return: List of achievements
        :rtype: List[Achievement]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.achievements,
            query=Utils.generate_query_dict(user_id=user_id))
        return [Achievement(**achievement) for achievement in response]

    def animes(self,
               page: Union[int, None] = None,
               limit: Union[int, None] = None,
               order: Union[Order, None] = None,
               kind: Union[Kind, None] = None,
               status: Union[Status, None] = None,
               season: Union[str, None] = None,
               score: Union[int, None] = None,
               duration: Union[Duration, None] = None,
               rating: Union[Rating, None] = None,
               genre: Union[None, List[int]] = None,
               studio: Union[None, List[int]] = None,
               franchise: Union[None, List[int]] = None,
               censored: Union[Censorship, None] = None,
               my_list: Union[MyList, None] = None,
               ids: Union[None, List[int]] = None,
               exclude_ids: Union[None, List[int]] = None,
               search: Union[str, None] = None) -> List[Anime]:
        """
        Returns animes list.

        :param page: Number of page
        :type page: Union[int, None]

        :param limit: Number of results limit
        :type limit: Union[int, None]

        :param order: Type of order in list
        :type order: Union[Order, None]

        :param kind: Type of anime topic
        :type kind: Union[Kind, None]

        :param status: Type of anime status
        :type status: Union[Status, None]

        :param season: Name of anime season
        :type season: Union[str, None]

        :param score: Minimal anime score
        :type score: Union[int, None]

        :param duration: Duration size of anime
        :type duration: Union[Duration, None]

        :param rating: Type of anime rating
        :type rating: Union[Rating, None]

        :param genre: Genres ID
        :type genre: Union[List[int], None]

        :param studio: Studios ID
        :type studio: Union[List[int], None]

        :param franchise: Franchises ID
        :type franchise: Union[List[int], None]

        :param censored: Type of anime censorship
        :type censored: Union[Censorship, None]

        :param my_list: Status of anime in current user list
        :type my_list: Union[MyList, None]

        :param ids: Animes ID to include
        :type ids: Union[List[int], None]

        :param exclude_ids: Animes ID to exclude
        :type exclude_ids: Union[List[int], None]

        :param search: Search phrase to filter animes by name
        :type search: Union[str, None]

        :returns: Animes list
        :rtype: List[Anime]
        """
        page = Utils.validate_query_number(page, 100000)
        limit = Utils.validate_query_number(limit, 50)
        score = Utils.validate_query_number(score, 9)

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.animes,
            query=Utils.generate_query_dict(page=page,
                                            limit=limit,
                                            order=order,
                                            kind=kind,
                                            status=status,
                                            season=season,
                                            score=score,
                                            duration=duration,
                                            rating=rating,
                                            genre=genre,
                                            studio=studio,
                                            franchise=franchise,
                                            censored=censored,
                                            my_list=my_list,
                                            ids=ids,
                                            exclude_ids=exclude_ids,
                                            search=search))
        return [Anime(**anime) for anime in response]

    def anime(self, anime_id: int) -> Anime:
        """
        Returns info about certain anime.

        :param anime_id: Anime ID to get info
        :type anime_id: int

        :return: Anime info
        :rtype: Anime
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.anime(anime_id))
        return Anime(**response)

    def anime_creators(self, anime_id: int) -> List[Creator]:
        """
        Returns creators info of certain anime.

        :param anime_id: Anime ID to get creators
        :type anime_id: int

        :return: List of anime creators
        :rtype: List[Creator]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_roles(anime_id))
        return [Creator(**creator) for creator in response]

    def similar_animes(self, anime_id: int) -> List[Anime]:
        """
        Returns list of similar animes for certain anime.

        :param anime_id: Anime ID to get similar animes
        :type anime_id: int

        :return: List of similar animes
        :rtype: List[Anime]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.similar_animes(anime_id))
        return [Anime(**anime) for anime in response]

    def anime_related_content(self, anime_id: int) -> List[Relation]:
        """
        Returns list of related content of certain anime.

        :param anime_id: Anime ID to get related content
        :type anime_id: int

        :return: List of relations
        :rtype: List[Relation]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_related_content(anime_id))
        return [Relation(**relation) for relation in response]

    def anime_screenshots(self, anime_id: int) -> List[Screenshot]:
        """
        Returns list of screenshot links of certain anime.

        :param anime_id: Anime ID to get screenshot links
        :type anime_id: int

        :return: List of screenshot links
        :rtype: List[Screenshot]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_screenshots(anime_id))
        return [Screenshot(**screenshot) for screenshot in response]

    def anime_franchise_tree(self, anime_id: int) -> FranchiseTree:
        """
        Returns franchise tree of certain anime.

        :param anime_id: Anime ID to get franchise tree
        :type anime_id: int

        :return: Franchise tree of certain anime
        :rtype: FranchiseTree
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.anime_franchise_tree(anime_id))
        return FranchiseTree(**response)

    def anime_external_links(self, anime_id: int) -> List[Link]:
        """
        Returns list of external links of certain anime.

        :param anime_id: Anime ID to get external links
        :type anime_id: int

        :return: List of external links
        :rtype: List[Link]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_external_links(anime_id))
        return [Link(**link) for link in response]

    def anime_topics(self,
                     anime_id: int,
                     page: Union[int, None] = None,
                     limit: Union[int, None] = None,
                     kind: Union[Status, None] = None,
                     episode: Union[int, None] = None) -> List[Topic]:
        """
        Returns list of topics of certain anime.

        If some data are not provided, using default values.

        :param anime_id: Anime ID to get topics
        :type anime_id: int

        :param page: Number of page
        :type page: Union[int, None]

        :param limit: Number of results limit
        :type limit: Union[int, None]

        :param kind: Status of anime
        :type kind: Union[Status, None]

        :param episode: Number of anime episode
        :type episode: Union[int, None]

        :return: List of topics
        :rtype: List[Topic]
        """
        page = Utils.validate_query_number(page, 100000)
        limit = Utils.validate_query_number(limit, 30)

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_topics(anime_id),
            query=Utils.generate_query_dict(page=page,
                                            limit=limit,
                                            kind=kind,
                                            episode=episode))
        return [Topic(**topic) for topic in response]

    @protected_method
    def appears(self, comment_ids: List[str]) -> bool:
        """
        Marks comments or topics as read.

        :param comment_ids: IDs of comments or topics to mark
        :type comment_ids: List[str]

        :return: Status of mark
        :rtype: bool
        """
        data: Dict[str, str] = {'ids': ','.join(comment_ids)}
        response_code: int = self._request(self._endpoints.appears,
                                           headers=self._authorization_header,
                                           data=data,
                                           request_type=RequestType.POST)
        return response_code == ResponseCode.SUCCESS.value

    def bans(self,
             page: Union[int, None] = None,
             limit: Union[int, None] = None) -> List[Ban]:
        """
        Returns list of recent bans on Shikimori.

        :param page: Number of page
        :type page: Union[int, None]

        :param limit: Number of results limit
        :type limit: Union[int, None]

        :return: List of recent bans
        :rtype: List[Ban]
        """
        page = Utils.validate_query_number(page, 100000)
        limit = Utils.validate_query_number(limit, 30)

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.bans_list,
            query=Utils.generate_query_dict(page=page, limit=limit))
        return [Ban(**ban) for ban in response]

    def calendar(
            self,
            censored: Union[Censorship, None] = None) -> List[CalendarEvent]:
        """
        Returns current calendar events.

        :param censored: Status of censorship for events
        :type censored: Union[Censorship, None]

        :return: List of calendar events
        :rtype: List[CalendarEvent]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.calendar,
            query=Utils.generate_query_dict(censored=censored))
        return [CalendarEvent(**calendar_event) for calendar_event in response]

    def character(self, character_id: int) -> Character:
        """
        Returns character info by ID.

        :param character_id: ID of character to get info
        :type character_id: int

        :return: Character info
        :rtype: Character
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.character(character_id))
        return Character(**response)

    def character_search(self,
                         search: Union[str, None] = None) -> List[Character]:
        """
        Returns list of found characters.

        :param search: Search query for characters
        :type search: Union[str, None]

        :return: List of found characters
        :rtype: List[Character]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.character_search,
            query=Utils.generate_query_dict(search=search))
        return [Character(**character) for character in response]

    def users(self,
              page: Union[int, None] = None,
              limit: Union[int, None] = None) -> List[User]:
        """
        Returns list of users.

        :param page: Number of page
        :type page: Union[int, None]

        :param limit: Number of results limit
        :type limit: Union[int, None]

        :return: List of users
        :rtype: List[User]
        """
        page = Utils.validate_query_number(page, 100000)
        limit = Utils.validate_query_number(limit, 100)

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.users,
            query=Utils.generate_query_dict(page=page, limit=limit))
        return [User(**user) for user in response]

    def user(self,
             user_id: Union[str, int],
             is_nickname: Union[bool, None] = None) -> User:
        """
        Returns info about user.

        :param user_id: User ID/Nickname to get info
        :type user_id: Union[str, int]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Union[bool, None]

        :return: Info about user
        :rtype: User
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.user(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return User(**response)

    def user_info(self,
                  user_id: Union[str, int],
                  is_nickname: Union[bool, None] = None) -> User:
        """
        Returns user's brief info.

        :param user_id: User ID/Nickname to get brief info
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Union[bool, None]

        :return: User's brief info
        :rtype: User
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.user_info(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return User(**response)

    @protected_method
    def current_user(self) -> User:
        """
        Returns brief info about current user.

        Current user evaluated depending on authorization code.

        :return: Current user brief info
        :rtype: User
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.whoami,
                                            headers=self._authorization_header)
        return User(**response)

    @protected_method
    def sign_out(self):
        """Sends sign out request to API."""
        self._request(self._endpoints.sign_out,
                      headers=self._authorization_header)

    def user_friends(self,
                     user_id: Union[str, int],
                     is_nickname: Union[bool, None] = None) -> List[User]:
        """
        Returns user's friends.

        :param user_id: User ID/Nickname to get friends
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Union[bool, None]

        :return: List of user's friends
        :rtype: List[User]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_friends(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return [User(**friend) for friend in response]

    def user_clubs(self,
                   user_id: Union[int, str],
                   is_nickname: Union[bool, None] = None) -> List[Club]:
        """
        Returns user's clubs.

        :param user_id: User ID/Nickname to get clubs
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Union[bool, None]

        :return: List of user's clubs
        :rtype: List[Club]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_clubs(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return [Club(**club) for club in response]

    def user_anime_rates(
            self,
            user_id: Union[int, str],
            is_nickname: Union[bool, None] = None,
            page: Union[int, None] = None,
            limit: Union[int, None] = None,
            status: Union[MyList, None] = None,
            censored: Union[Censorship, None] = None) -> List[UserList]:
        """
        Returns user's anime list.

        :param user_id: User ID/Nickname to get anime list
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Union[bool, None]

        :param page: Number of page
        :type page: Union[int, None]

        :param limit: Number of results limit
        :type limit: Union[int, None]

        :param status: Status of status of anime in list
        :type status: Union[MyList, None]

        :param censored: Type of anime censorship
        :type censored: Union[Censorship, None]

        :return: User's anime list
        :rtype: List[UserList]
        """
        page = Utils.validate_query_number(page, 100000)
        limit = Utils.validate_query_number(limit, 5000)

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_anime_rates(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=page,
                                            limit=limit,
                                            status=status,
                                            censored=censored))
        return [UserList(**user_list) for user_list in response]

    def user_manga_rates(
            self,
            user_id: Union[int, str],
            is_nickname: Union[bool, None] = None,
            page: Union[int, None] = None,
            limit: Union[int, None] = None,
            censored: Union[Censorship, None] = None) -> List[UserList]:
        """
        Returns user's manga list.

        :param user_id: User ID/Nickname to get manga list
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Union[bool, None]

        :param page: Number of page
        :type page: Union[int, None]

        :param limit: Number of results limit
        :type limit: Union[int, None]

        :param censored: Type of manga censorship
        :type censored: Union[Censorship, None]

        :return: User's manga list
        :rtype: List[UserList]
        """
        page = Utils.validate_query_number(page, 100000)
        limit = Utils.validate_query_number(limit, 5000)

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_manga_rates(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=page,
                                            limit=limit,
                                            censored=censored))
        return [UserList(**user_list) for user_list in response]

    def user_favourites(self,
                        user_id: Union[int, str],
                        is_nickname: Union[bool, None] = None) -> Favourites:
        """
        Returns user's favourites.

        :param user_id: User ID/Nickname to get favourites
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Union[bool, None]

        :return: User's favourites
        :rtype: Favourites
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.user_favourites(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Favourites(**response)

    @protected_method
    def current_user_messages(
            self,
            user_id: Union[int, str],
            is_nickname: Union[bool, None] = None,
            page: Union[int, None] = None,
            limit: Union[int, None] = None,
            message_type: MessageType = MessageType.NEWS) -> List[Message]:
        """
        Returns current user's messages by type.

        :param user_id: Current user ID/Nickname to get messages
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Union[bool, None]

        :param page: Number of page
        :type page: Union[int, None]

        :param limit: Number of page limits
        :type limit: Union[int, None]

        :param message_type: Type of message
        :type message_type: MessageType

        :return: Current user's messages
        :rtype: List[Message]
        """
        page = Utils.validate_query_number(page, 100000)
        limit = Utils.validate_query_number(limit, 100)

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_messages(user_id),
            headers=self._authorization_header,
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=page,
                                            limit=limit,
                                            type=message_type))
        return [Message(**message) for message in response]

    @protected_method
    def current_user_unread_messages(
            self,
            user_id: Union[int, str],
            is_nickname: Union[bool, None] = None) -> UnreadMessages:
        """
        Returns current user's unread messages counter.

        :param user_id: Current user ID/Nickname to get unread messages
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Union[bool, None]

        :return: Current user's unread messages counters
        :rtype: UnreadMessages
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.user_unread_messages(user_id),
            headers=self._authorization_header,
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return UnreadMessages(**response)

    def user_history(
            self,
            user_id: Union[int, str],
            is_nickname: Union[bool, None] = None,
            page: Union[int, None] = None,
            limit: Union[int, None] = None,
            target_id: Union[int, None] = None,
            target_type: Union[TargetType, None] = None) -> List[History]:
        """
        Returns history of user.

        :param user_id: User ID/Nickname to get history
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Union[bool, None]

        :param page: Number of page
        :type page: Union[int, None]

        :param limit: Number of results limit
        :type limit: Union[int, None]

        :param target_id: ID of anime/manga in history
        :type target_id: Union[int, None]

        :param target_type: Type of target (Anime/Manga)
        :type target_type: Union[TargetType, None]

        :return: User's history
        :rtype: List[History]
        """
        page = Utils.validate_query_number(page, 100000)
        limit = Utils.validate_query_number(limit, 100)

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_history(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=page,
                                            limit=limit,
                                            target_id=target_id,
                                            target_type=target_type))
        return [History(**history) for history in response]

    def user_bans(self,
                  user_id: Union[int, str],
                  is_nickname: Union[bool, None] = None) -> List[Ban]:
        """
        Returns list of bans of user.

        :param user_id: User ID/Nickname to get list of bans
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Union[bool, None]

        :return: User's bans
        :rtype: List[Ban]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_bans(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return [Ban(**ban) for ban in response]
