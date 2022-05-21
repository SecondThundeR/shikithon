""" Shikithon API Module.

This is main module with a class
for interacting with the Shikimori API.
"""
import sys
from json import dumps
from time import sleep, time
from typing import Any, Dict, List, Optional, Tuple, Union

from loguru import logger
from ratelimit import limits, sleep_and_retry
from requests import JSONDecodeError, Response, Session

from shikithon.config_cache import ConfigCache
from shikithon.decorators import protected_method
from shikithon.endpoints import Endpoints
from shikithon.enums.anime import (AnimeCensorship, AnimeDuration, AnimeKind,
                                   AnimeList, AnimeOrder, AnimeRating,
                                   AnimeStatus)
from shikithon.enums.club import (CommentPolicy, ImageUploadPolicy, JoinPolicy,
                                  PagePolicy, TopicPolicy)
from shikithon.enums.comment import CommentableType
from shikithon.enums.favorite import LinkedType
from shikithon.enums.history import TargetType
from shikithon.enums.manga import (MangaCensorship, MangaKind, MangaList,
                                   MangaOrder, MangaStatus)
from shikithon.enums.message import MessageType
from shikithon.enums.person import PersonKind
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
from shikithon.models.club_image import ClubImage
from shikithon.models.comment import Comment
from shikithon.models.constants import (AnimeConstants, ClubConstants,
                                        MangaConstants, SmileyConstants,
                                        UserRateConstants)
from shikithon.models.creator import Creator
from shikithon.models.dialog import Dialog
from shikithon.models.favourites import Favourites
from shikithon.models.forum import Forum
from shikithon.models.franchise_tree import FranchiseTree
from shikithon.models.genre import Genre
from shikithon.models.history import History
from shikithon.models.link import Link
from shikithon.models.manga import Manga
from shikithon.models.message import Message
from shikithon.models.people import People
from shikithon.models.ranobe import Ranobe
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

    def __init__(self, config: Union[str, Dict[str, str]]):
        """
        Initialization and updating of variables
        required to interact with the Shikimori API

        This magic method calls config and variables validator,
        as well as updating session object header
        and getting access/refresh tokens

        :param config: Config file for API class or app name
        :type config: Union[str, Dict[str, str]]
        """
        logger.configure(handlers=[
            {
                'sink': sys.stderr,
                'level': 'INFO',
                'format': '{time} | {level} | {message}'
            },
            {
                'sink': 'shikithon_{time}.log',
                'level': 'DEBUG',
                'format': '{time} | {level} | {file}.{function}: {message}',
                'rotation': '1 MB',
                'compression': 'zip'
            },
        ])

        logger.info('Initializing API object')

        self._endpoints: Endpoints = Endpoints(SHIKIMORI_API_URL,
                                               SHIKIMORI_API_URL_V2,
                                               SHIKIMORI_OAUTH_URL)
        self._session: Session = Session()

        self._restricted_mode = False
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
        logger.info('Successfully initialized API object')

    @property
    def restricted_mode(self) -> bool:
        """
        Returns current restrict mode of API object.

        If true, API object can access only public methods

        :return: Current restrict mode
        :rtype: bool
        """
        return self._restricted_mode

    @restricted_mode.setter
    def restricted_mode(self, restricted_mode: bool):
        """
        Sets new restrict mode of API object.

        :param restricted_mode: New restrict mode
        :type restricted_mode: bool
        """
        self._restricted_mode = restricted_mode

    @property
    def scopes_list(self) -> List[str]:
        """
        Returns list of scopes.

        :return: List of scopes
        :rtype: List[str]
        """
        return self._scopes.split('+')

    @property
    def config(self) -> Dict[str, str]:
        """
        Returns current API variables as config dictionary.

        :return: Current API variables as config dictionary
        :rtype: Dict[str, str]
        """
        logger.debug('Exporting current API config')
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
        logger.info('Setting new API config')
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

    def _init_config(self, config: Union[str, Dict[str, str]]):
        """
        Special method for initializing an object.

        This method calls several methods:

        - Validation of config and variables
        - Customizing the session header user agent
        - Getting access/refresh tokens if they are missing

        Otherwise, if only app name is provided, setting it

        :param config: Config dictionary or app name
        :type config: Union[str, Dict[str, str]]
        """
        logger.debug('Initializing API config')
        self._validate_config(config)
        self._validate_vars()
        logger.debug('Setting User-Agent with current app name')
        self._user_agent = self._app_name

        if isinstance(config, dict) and not self._access_token:
            logger.debug('No tokens found')
            tokens_data: Tuple[str, str] = self._get_access_token()
            self._update_tokens(tokens_data)

    @logger.catch(onerror=lambda _: sys.exit(1))
    def _validate_config(self, config: Union[str, Dict[str, str]]):
        """
        Validates passed config dictionary and sets
        API variables.

        If config is string, sets only app name and change value
        of restrict mode of API object.

        Also, if config is dictionary and method detects
        a cached configuration file, it replaces passed configuration
        dictionary with the cached one.

        Raises MissingConfigData if some variables
        are missing in config dictionary

        :param config: Config dictionary or app name for validation
        :type config: Union[str, Dict[str, str]]

        :raises MissingConfigData: If any field is missing
            (Not raises if there is a cache config)
        """
        logger.debug('Validating API config')
        if isinstance(config, str):
            logger.debug('Detected app_name only. Switching to restricted mode')
            self._app_name = config
            self.restricted_mode = True
            return

        try:
            logger.debug('Checking for cached config')
            cached_config, config_cached = ConfigCache.cache_config_validation(
                config['app_name'], config['auth_code'])

            if config_cached:
                logger.debug('Replacing passed config with cached one')
                config = cached_config

                logger.debug('Extracting access tokens from config')
                self._access_token = cached_config['access_token']
                self._refresh_token = cached_config['refresh_token']
                self._token_expire = int(cached_config['token_expire'])

            logger.debug('Extracting app related variables from config')
            self._app_name = config['app_name']
            self._client_id = config['client_id']
            self._client_secret = config['client_secret']
            self._redirect_uri = config['redirect_uri']
            self._scopes = config['scopes']
            self._auth_code = config['auth_code']
        except KeyError as err:
            raise MissingConfigData(
                'It is impossible to initialize an API object'
                'without missing variables. '
                'Recheck your config and try again.') from err

    @logger.catch(onerror=lambda _: sys.exit(1))
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
        - If restricted mode is True, returns after app name check.

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

        if self.restricted_mode:
            return

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

    @logger.catch(onerror=lambda _: sys.exit(1))
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
            logger.info('Refreshing current tokens')
            data['grant_type'] = 'refresh_token'
            data['refresh_token'] = self._refresh_token
        else:
            logger.info('Getting new tokens')
            data['grant_type'] = 'authorization_code'
            data['code'] = self._auth_code
            data['redirect_uri'] = self._redirect_uri

        oauth_json: Dict[str,
                         Any] = self._request(self._endpoints.oauth_token,
                                              data=data,
                                              request_type=RequestType.POST,
                                              json_logging=False)

        try:
            logger.debug('Returning new access and refresh tokens')
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
        logger.debug('Updating current tokens')
        self._tokens = tokens_data
        self._cache_config()

    def _cache_config(self):
        """Updates token expire time and caches new config."""
        self._token_expire = Utils.get_new_expire_time(TOKEN_EXPIRE_TIME)
        ConfigCache.save_config(self.config)
        logger.debug('New expiration time has been set '
                     'and cached configuration has been updated')

    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
    def _request(
        self,
        url: str,
        data: Optional[Dict[str, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        query: Optional[Dict[str, str]] = None,
        request_type: RequestType = RequestType.GET,
        json_logging: bool = True,
    ) -> Optional[Union[List[Dict[str, Any]], Dict[str, Any], str]]:
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
        :type data: Optional[Dict[str, str]]

        :param headers: Custom headers for request
        :type headers: Optional[Dict[str, str]]

        :param query: Query data for request
        :type query: Optional[Dict[str, str]]

        :param request_type: Type of current request
        :type request_type: RequestType

        :param json_logging: Parameter for logging JSON response
        :type json_logging: bool

        :return: Response JSON, text or status code
        :rtype: Optional[Union[List[Dict[str, Any]], Dict[str, Any], str]]
        """

        logger.info(f'{request_type.value} {url}')
        logger.debug(f'Request info details: {data=}, {headers=}, {query=}')

        if request_type == RequestType.GET:
            response: Response = self._session.get(url,
                                                   headers=headers,
                                                   params=query)
        elif request_type == RequestType.POST:
            response: Response = self._session.post(url,
                                                    headers=headers,
                                                    params=query,
                                                    json=data)
        elif request_type == RequestType.PUT:
            response: Response = self._session.put(url,
                                                   headers=headers,
                                                   params=query,
                                                   json=data)
        elif request_type == RequestType.PATCH:
            response: Response = self._session.patch(url,
                                                     headers=headers,
                                                     params=query,
                                                     json=data)
        elif request_type == RequestType.DELETE:
            response: Response = self._session.delete(url,
                                                      headers=headers,
                                                      params=query,
                                                      json=data)
        else:
            logger.debug('Unknown request_type. Returning None')
            return None

        if response.status_code == ResponseCode.RETRY_LATER.value:
            logger.info('Hit RPS cooldown. Waiting on request repeat')
            sleep(RATE_LIMIT_RPS_COOLDOWN)
            return self._request(url, data, headers, query, request_type)

        try:
            logger.debug('Extracting JSON from response')
            json_response = response.json()
            if json_logging:
                logger.debug(
                    'Successful extraction. '
                    f'Here are the details of the response: {json_response}')
            return json_response
        except JSONDecodeError:
            logger.debug('Can\'t extract JSON. Returning status_code/text')
            return response.status_code if not response.text else response.text

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
        logger.debug('Checking if current time is greater '
                     'than current token expire time')
        return int(time()) > self._token_expire

    def achievements(self, user_id: int) -> Optional[List[Achievement]]:
        """
        Returns achievements of user by ID.

        :param user_id: User ID for getting achievements
        :type user_id: int

        :return: List of achievements or None if list is empty
        :rtype: Optional[List[Achievement]]
        """
        logger.debug('Executing "/api/achievements/ method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.achievements,
            query=Utils.generate_query_dict(user_id=user_id))
        if not response:
            return None
        return [Achievement(**achievement) for achievement in response]

    def animes(self,
               page: Optional[int] = None,
               limit: Optional[int] = None,
               order: Optional[AnimeOrder] = None,
               kind: Optional[Union[AnimeKind, List[AnimeKind]]] = None,
               status: Optional[Union[AnimeStatus, List[AnimeStatus]]] = None,
               season: Optional[Union[str, List[str]]] = None,
               score: Optional[int] = None,
               duration: Optional[Union[AnimeDuration,
                                        List[AnimeDuration]]] = None,
               rating: Optional[Union[AnimeRating, List[AnimeRating]]] = None,
               genre: Optional[Union[int, List[int]]] = None,
               studio: Optional[Union[int, List[int]]] = None,
               franchise: Optional[Union[int, List[int]]] = None,
               censored: Optional[AnimeCensorship] = None,
               my_list: Optional[Union[AnimeList, List[AnimeList]]] = None,
               ids: Optional[Union[int, List[int]]] = None,
               exclude_ids: Optional[Union[int, List[int]]] = None,
               search: Optional[str] = None) -> Optional[List[Anime]]:
        """
        Returns animes list.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param order: Type of order in list
        :type order: Optional[AnimeOrder]

        :param kind: Type(s) of anime topics
        :type kind: Optional[Union[AnimeKind, List[AnimeKind]]]

        :param status: Type(s) of anime status
        :type status: Optional[Union[AnimeStatus, List[AnimeStatus]]]

        :param season: Name(s) of anime seasons
        :type season: Optional[Union[str, List[str]]]

        :param score: Minimal anime score
        :type score: Optional[int]

        :param duration: Duration size(s) of anime
        :type duration: Optional[Union[AnimeDuration, List[AnimeDuration]]]

        :param rating: Type of anime rating(s)
        :type rating: Optional[Union[AnimeRating, List[AnimeRating]]]

        :param genre: Genre(s) ID
        :type genre: Optional[Union[int, List[int]]]

        :param studio: Studio(s) ID
        :type studio: Optional[Union[int, List[int]]]

        :param franchise: Franchise(s) ID
        :type franchise: Optional[Union[int, List[int]]]

        :param censored: Type of anime censorship
        :type censored: Optional[AnimeCensorship]

        :param my_list: Status(-es) of anime in current user list
            **Note:** If app is in restricted mode,
            this parameter won't affect on response.
        :type my_list: Optional[Union[AnimeList, List[AnimeList]]]

        :param ids: Anime(s) ID to include
        :type ids: Optional[Union[int, List[int]]]

        :param exclude_ids: Anime(s) ID to exclude
        :type exclude_ids: Optional[Union[int, List[int]]]

        :param search: Search phrase to filter animes by name
        :type search: Optional[str]

        :return: Animes list or None if page is empty
        :rtype: Optional[List[Anime]]
        """
        logger.debug('Executing "/api/animes" method')
        validated_numbers = Utils.query_numbers_validator(page=[page, 100000],
                                                          limit=[limit, 50],
                                                          score=[score, 9])

        headers: Optional[Dict[str, str]] = None

        if not self.restricted_mode:
            logger.debug('Using "/api/animes" as protected method')
            headers = self._authorization_header

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.animes,
            headers=headers,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            order=order,
                                            kind=kind,
                                            status=status,
                                            season=season,
                                            score=validated_numbers['score'],
                                            duration=duration,
                                            rating=rating,
                                            genre=genre,
                                            studio=studio,
                                            franchise=franchise,
                                            censored=censored,
                                            mylist=my_list,
                                            ids=ids,
                                            exclude_ids=exclude_ids,
                                            search=search))
        if response:
            return [Anime(**anime) for anime in response]
        return None

    def anime(self, anime_id: int) -> Anime:
        """
        Returns info about certain anime.

        :param anime_id: Anime ID to get info
        :type anime_id: int

        :return: Anime info
        :rtype: Anime
        """
        logger.debug('Executing "/api/animes/:id" method')
        response: Dict[str,
                       Any] = self._request(self._endpoints.anime(anime_id))
        return Anime(**response)

    def anime_creators(self, anime_id: int) -> Optional[List[Creator]]:
        """
        Returns creators info of certain anime.

        :param anime_id: Anime ID to get creators
        :type anime_id: int

        :return: List of anime creators or None if list is empty
        :rtype: Optional[List[Creator]]
        """
        logger.debug('Executing "/api/animes/:id/roles" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_roles(anime_id))
        if not response:
            return None
        return [Creator(**creator) for creator in response]

    def similar_animes(self, anime_id: int) -> Optional[List[Anime]]:
        """
        Returns list of similar animes for certain anime.

        :param anime_id: Anime ID to get similar animes
        :type anime_id: int

        :return: List of similar animes or None if list is empty
        :rtype: Optional[List[Anime]]
        """
        logger.debug('Executing "/api/animes/:id/similar" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.similar_animes(anime_id))
        if not response:
            return None
        return [Anime(**anime) for anime in response]

    def anime_related_content(self, anime_id: int) -> Optional[List[Relation]]:
        """
        Returns list of related content of certain anime.

        :param anime_id: Anime ID to get related content
        :type anime_id: int

        :return: List of relations or None if list is empty
        :rtype: Optional[List[Relation]]
        """
        logger.debug('Executing "/api/animes/:id/related" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_related_content(anime_id))
        if not response:
            return None
        return [Relation(**relation) for relation in response]

    def anime_screenshots(self, anime_id: int) -> Optional[List[Screenshot]]:
        """
        Returns list of screenshot links of certain anime.

        :param anime_id: Anime ID to get screenshot links
        :type anime_id: int

        :return: List of screenshot links or None if list is empty
        :rtype: Optional[List[Screenshot]]
        """
        logger.debug('Executing "/api/animes/:id/screenshots" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_screenshots(anime_id))
        if not response:
            return None
        return [Screenshot(**screenshot) for screenshot in response]

    def anime_franchise_tree(self, anime_id: int) -> FranchiseTree:
        """
        Returns franchise tree of certain anime.

        :param anime_id: Anime ID to get franchise tree
        :type anime_id: int

        :return: Franchise tree of certain anime
        :rtype: FranchiseTree
        """
        logger.debug('Executing "/api/animes/:id/franchise" method')
        response: Dict[str, Any] = self._request(
            self._endpoints.anime_franchise_tree(anime_id))
        return FranchiseTree(**response)

    def anime_external_links(self, anime_id: int) -> Optional[List[Link]]:
        """
        Returns list of external links of certain anime.

        :param anime_id: Anime ID to get external links
        :type anime_id: int

        :return: List of external links or None if list is empty
        :rtype: Optional[List[Link]]
        """
        logger.debug('Executing "/api/animes/:id/external_links" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_external_links(anime_id))
        if not response:
            return None
        return [Link(**link) for link in response]

    def anime_topics(self,
                     anime_id: int,
                     page: Optional[int] = None,
                     limit: Optional[int] = None,
                     kind: Optional[AnimeStatus] = None,
                     episode: Optional[int] = None) -> Optional[List[Topic]]:
        """
        Returns list of topics of certain anime.

        If some data are not provided, using default values.

        :param anime_id: Anime ID to get topics
        :type anime_id: int

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param kind: Kind of anime (Uses status enum values)
        :type kind: Optional[AnimeStatus]

        :param episode: Number of anime episode
        :type episode: Optional[int]

        :return: List of topics or None if page is empty
        :rtype: Optional[List[Topic]]
        """
        logger.debug('Executing "/api/animes/:id/topics" method')
        validated_numbers = Utils.query_numbers_validator(page=[page, 100000],
                                                          limit=[limit, 30])

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_topics(anime_id),
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            kind=kind,
                                            episode=episode))
        if response:
            return [Topic(**topic) for topic in response]
        return None

    @protected_method()
    def appears(self, comment_ids: List[str]) -> bool:
        """
        Marks comments or topics as read.

        This method uses generate_query_dict for data dict,
        because there is no need for nested dictionary

        :param comment_ids: IDs of comments or topics to mark
        :type comment_ids: List[str]

        :return: Status of mark
        :rtype: bool
        """
        logger.debug('Executing "/api/appears" method')
        response_code: int = self._request(
            self._endpoints.appears,
            headers=self._authorization_header,
            data=Utils.generate_query_dict(ids=comment_ids),
            request_type=RequestType.POST)
        return response_code == ResponseCode.SUCCESS.value

    def bans(self,
             page: Optional[int] = None,
             limit: Optional[int] = None) -> Optional[List[Ban]]:
        """
        Returns list of recent bans on Shikimori.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of recent bans or None if page is empty
        :rtype: Optional[List[Ban]]
        """
        logger.debug('Executing "/api/bans" method')
        logger.debug('Checking page parameter')
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.bans_list,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit']))
        if response:
            return [Ban(**ban) for ban in response]
        return None

    def calendar(
        self,
        censored: Optional[AnimeCensorship] = None
    ) -> Optional[List[CalendarEvent]]:
        """
        Returns current calendar events.

        :param censored: Status of censorship for events
        :type censored: Optional[AnimeCensorship]

        :return: List of calendar events or None if list is empty
        :rtype: Optional[List[CalendarEvent]]
        """
        logger.debug('Executing "api/calendar" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.calendar,
            query=Utils.generate_query_dict(censored=censored))
        if not response:
            return None
        return [CalendarEvent(**calendar_event) for calendar_event in response]

    def character(self, character_id: int) -> Character:
        """
        Returns character info by ID.

        :param character_id: ID of character to get info
        :type character_id: int

        :return: Character info
        :rtype: Character
        """
        logger.debug('Executing "/api/characters/:id" method')
        response: Dict[str, Any] = self._request(
            self._endpoints.character(character_id))
        return Character(**response)

    def character_search(self,
                         search: Optional[str] = None
                        ) -> Optional[List[Character]]:
        """
        Returns list of found characters.

        :param search: Search query for characters
        :type search: Optional[str]

        :return: List of found characters or None if list is empty
        :rtype: Optional[List[Character]]
        """
        logger.debug('Executing "/api/characters/search" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.character_search,
            query=Utils.generate_query_dict(search=search))
        if not response:
            return None
        return [Character(**character) for character in response]

    def clubs(self,
              page: Optional[int] = None,
              limit: Optional[int] = None,
              search: Optional[str] = None) -> Optional[List[Club]]:
        """
        Returns clubs list.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param search: Search phrase to filter clubs by name
        :type search: Optional[str]

        :return: Clubs list or None if page is empty
        :rtype: Optional[List[Club]]
        """
        logger.debug('Executing "/api/clubs" method')
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.clubs,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            search=search))
        if response:
            return [Club(**club) for club in response]
        return None

    def club(self, club_id: int) -> Club:
        """
        Returns info about club.

        :param club_id: Club ID to get info
        :type club_id: int

        :return: Info about club
        :rtype: Club
        """
        logger.debug('Executing "/api/clubs/:id" method')
        response: Dict[str, Any] = self._request(self._endpoints.club(club_id))
        return Club(**response)

    @protected_method(scope='clubs')
    def club_update(
            self,
            club_id: int,
            name: Optional[str] = None,
            join_policy: Optional[JoinPolicy] = None,
            description: Optional[str] = None,
            display_images: Optional[bool] = None,
            comment_policy: Optional[CommentPolicy] = None,
            topic_policy: Optional[TopicPolicy] = None,
            page_policy: Optional[PagePolicy] = None,
            image_upload_policy: Optional[ImageUploadPolicy] = None,
            is_censored: Optional[bool] = None,
            anime_ids: Optional[List[int]] = None,
            manga_ids: Optional[List[int]] = None,
            ranobe_ids: Optional[List[int]] = None,
            character_ids: Optional[List[int]] = None,
            club_ids: Optional[List[int]] = None,
            admin_ids: Optional[List[int]] = None,
            collection_ids: Optional[List[int]] = None,
            banned_user_ids: Optional[List[int]] = None) -> Optional[Club]:
        """
        Update info/settings about/of club.

        :param club_id: Club ID to modify/update
        :type club_id: int

        :param name: New name of club
        :type name: Optional[str]

        :param description: New description of club
        :type description: Optional[str]

        :param display_images: New display images status of club
        :type display_images: Optional[bool]

        :param is_censored: New censored status of club
        :type is_censored: Optional[bool]

        :param join_policy: New join policy of club
        :type join_policy: Optional[JoinPolicy]

        :param comment_policy: New comment policy of club
        :type comment_policy: Optional[CommentPolicy]

        :param topic_policy: New topic policy of club
        :type topic_policy: Optional[TopicPolicy]

        :param page_policy: New page policy of club
        :type page_policy: Optional[PagePolicy]

        :param image_upload_policy: New image upload policy of club
        :type image_upload_policy: Optional[ImageUploadPolicy]

        :param anime_ids: New anime ids of club
        :type anime_ids: Optional[List[int]]

        :param manga_ids: New manga ids of club
        :type manga_ids: Optional[List[int]]

        :param ranobe_ids: New ranobe ids of club
        :type ranobe_ids: Optional[List[int]]

        :param character_ids: New character ids of club
        :type character_ids: Optional[List[int]]

        :param club_ids: New club ids of club
        :type club_ids: Optional[List[int]]

        :param admin_ids: New admin ids of club
        :type admin_ids: Optional[List[int]]

        :param collection_ids: New collection ids of club
        :type collection_ids: Optional[List[int]]

        :param banned_user_ids: New banned user ids of club
        :type banned_user_ids: Optional[List[int]]

        :return: Updated club info or None if an error occurred
        :rtype: Optional[Club]
        """
        logger.debug('Executing "/api/clubs/:id" method')
        response: Dict[str, Any] = self._request(
            self._endpoints.club(club_id),
            headers=self._authorization_header,
            data=Utils.generate_data_dict(
                dict_name='club',
                name=name,
                join_policy=join_policy,
                description=description,
                display_images=display_images,
                comment_policy=comment_policy,
                topic_policy=topic_policy,
                page_policy=page_policy,
                image_upload_policy=image_upload_policy,
                is_censored=is_censored,
                anime_ids=anime_ids,
                manga_ids=manga_ids,
                ranobe_ids=ranobe_ids,
                character_ids=character_ids,
                club_ids=club_ids,
                admin_ids=admin_ids,
                collection_ids=collection_ids,
                banned_user_ids=banned_user_ids),
            request_type=RequestType.PATCH)
        return Club(**response) if 'errors' not in response else None

    def club_animes(self, club_id: int) -> Optional[List[Anime]]:
        """
        Returns anime list of club.

        :param club_id: Club ID to get anime list
        :type club_id: int

        :return: Club anime list or None if list is empty
        :rtype: Optional[List[Anime]]
        """
        logger.debug('Executing "/api/clubs/:id/animes" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.club_animes(club_id))
        if not response:
            return None
        return [Anime(**anime) for anime in response]

    def club_mangas(self, club_id: int) -> Optional[List[Manga]]:
        """
        Returns manga list of club.

        :param club_id: Club ID to get manga list
        :type club_id: int

        :return: Club manga list or None if list is empty
        :rtype: Optional[List[Manga]]
        """
        logger.debug('Executing "/api/clubs/:id/mangas" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.club_mangas(club_id))
        if not response:
            return None
        return [Manga(**manga) for manga in response]

    def club_ranobe(self, club_id: int) -> Optional[List[Ranobe]]:
        """
        Returns ranobe list of club.

        :param club_id: Club ID to get ranobe list
        :type club_id: int

        :return: Club ranobe list or None if list is empty
        :rtype: Optional[List[Ranobe]]
        """
        logger.debug('Executing "/api/clubs/:id/ranobe" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.club_ranobe(club_id))
        if not response:
            return None
        return [Ranobe(**ranobe) for ranobe in response]

    def club_characters(self, club_id: int) -> Optional[List[Character]]:
        """
        Returns character list of club.

        :param club_id: Club ID to get character list
        :type club_id: int

        :return: Club character list or None if list is empty
        :rtype: Optional[List[Character]]
        """
        logger.debug('Executing "/api/clubs/:id/characters" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.club_characters(club_id))
        if not response:
            return None
        return [Character(**character) for character in response]

    def club_members(self, club_id: int) -> Optional[List[User]]:
        """
        Returns member list of club.

        :param club_id: Club ID to get member list
        :type club_id: int

        :return: Club member list or None if list is empty
        :rtype: Optional[List[User]]
        """
        logger.debug('Executing "/api/clubs/:id/members" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.club_members(club_id))
        if not response:
            return None
        return [User(**user) for user in response]

    def club_images(self, club_id: int) -> Optional[List[ClubImage]]:
        """
        Returns images of club.

        :param club_id: Club ID to get images
        :type club_id: int

        :return: Club's images or None if list is empty
        :rtype: Optional[List[ClubImage]]
        """
        logger.debug('Executing "/api/clubs/:id/images" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.club_images(club_id))
        if not response:
            return None
        return [ClubImage(**club_image) for club_image in response]

    @protected_method(scope='clubs')
    def club_join(self, club_id: int):
        """
        Joins club by ID.

        :param club_id: Club ID to join
        :type club_id: int

        :return: Status of join
        :rtype: bool
        """
        logger.debug('Executing "/api/clubs/:id/join" method')
        response: Union[Dict[str, Any],
                        int] = self._request(self._endpoints.club_join(club_id),
                                             headers=self._authorization_header,
                                             request_type=RequestType.POST)
        return response == ResponseCode.SUCCESS.value

    @protected_method(scope='clubs')
    def club_leave(self, club_id: int) -> bool:
        """
        Leaves club by ID.

        :param club_id: Club ID to leave
        :type club_id: int

        :return: Status of leave
        :rtype: bool
        """
        logger.debug('Executing "/api/clubs/:id/leave" method')
        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.club_leave(club_id),
            headers=self._authorization_header,
            request_type=RequestType.POST)
        return response == ResponseCode.SUCCESS.value

    def comments(self,
                 commentable_id: int,
                 commentable_type: CommentableType,
                 page: Optional[int] = None,
                 limit: Optional[int] = None,
                 desc: Optional[int] = None) -> Optional[List[Comment]]:
        """
        Returns list of comments.

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

        :return: List of comments or None if page is empty
        :rtype: Optional[List[Comment]]
        """
        logger.debug('Executing "/api/comments" method')
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.comments,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            commentable_id=commentable_id,
                                            commentable_type=commentable_type,
                                            desc=desc))
        if response:
            return [Comment(**comment) for comment in response]
        return None

    def comment(self, comment_id: int) -> Comment:
        """
        Returns comment info.

        :param comment_id: ID of comment
        :type comment_id: int

        :return: Comment info
        :rtype: Comment
        """
        logger.debug('Executing "/api/comments/:id" method')
        response: Dict[str,
                       Any] = self._request(self._endpoints.comment(comment_id))
        return Comment(**response)

    @protected_method(scope='comments')
    def create_comment(self,
                       body: str,
                       commentable_id: int,
                       commentable_type: CommentableType,
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
        :type commentable_type: CommentableType

        :param is_offtopic: Status of offtopic
        :type is_offtopic: Optional[bool]

        :param broadcast: Broadcast comment in club’s topic status
        :type broadcast: Optional[bool]

        :return: Created comment info or None if an error occurred
        :rtype: Optional[Comment]
        """
        logger.debug('Executing "/api/comments" method')
        data_dict: Dict[str, Any] = Utils.generate_data_dict(
            dict_name='comment',
            body=body,
            commentable_id=commentable_id,
            commentable_type=commentable_type,
            is_offtopic=is_offtopic)

        if broadcast:
            logger.debug('Adding a broadcast value to a data_dict')
            data_dict['broadcast'] = broadcast

        response: Dict[str,
                       Any] = self._request(self._endpoints.comments,
                                            headers=self._authorization_header,
                                            data=data_dict,
                                            request_type=RequestType.POST)
        return Comment(**response) if 'errors' not in response else None

    @protected_method(scope='comments')
    def update_comment(self, comment_id: int, body: str) -> Optional[Comment]:
        """
        Updates comment.

        :param comment_id: ID of comment to update
        :type comment_id: int

        :param body: New body of comment
        :type body: str

        :return: Updated comment info or None if an error occurred
        :rtype: Optional[Comment]
        """
        logger.debug('Executing "/api/comments/:id" method')
        response: Dict[str, Any] = self._request(
            self._endpoints.comment(comment_id),
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='comment', body=body),
            request_type=RequestType.PATCH)
        return Comment(**response) if 'errors' not in response else None

    @protected_method(scope='comments')
    def delete_comment(self, comment_id: int) -> bool:
        """
        Deletes comment.

        :param comment_id: ID of comment to delete
        :type comment_id: int

        :return: Status of comment deletion
        :rtype: bool
        """
        logger.debug('Executing "/api/comments/:id" method')
        response: Dict[str,
                       Any] = self._request(self._endpoints.comment(comment_id),
                                            headers=self._authorization_header,
                                            request_type=RequestType.DELETE)
        return 'notice' in response

    def anime_constants(self) -> AnimeConstants:
        """
        Returns anime constants values.

        :return: Anime constants values
        :rtype: AnimeConstants
        """
        logger.debug('Executing "/api/constants/anime" method')
        response: Dict[str,
                       Any] = self._request(self._endpoints.anime_constants)
        return AnimeConstants(**response)

    def manga_constants(self) -> MangaConstants:
        """
        Returns manga constants values.

        :return: Manga constants values
        :rtype: MangaConstants
        """
        logger.debug('Executing "/api/constants/manga" method')
        response: Dict[str,
                       Any] = self._request(self._endpoints.manga_constants)
        return MangaConstants(**response)

    def user_rate_constants(self) -> UserRateConstants:
        """
        Returns user rate constants values.

        :return: User rate constants values
        :rtype: UserRateConstants
        """
        logger.debug('Executing "/api/constants/user_rate" method')
        response: Dict[str,
                       Any] = self._request(self._endpoints.user_rate_constants)
        return UserRateConstants(**response)

    def club_constants(self) -> ClubConstants:
        """
        Returns club constants values.

        :return: Club constants values
        :rtype: ClubConstants
        """
        logger.debug('Executing "/api/constants/club" method')
        response: Dict[str, Any] = self._request(self._endpoints.club_constants)
        return ClubConstants(**response)

    def smileys_constants(self) -> Optional[List[SmileyConstants]]:
        """
        Returns list of smileys constants values.

        :return: List of smileys constants values or None if list is empty
        :rtype: Optional[List[SmileyConstants]]
        """
        logger.debug('Executing "/api/constants/smileys" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.smileys_constants)
        if not response:
            return None
        return [SmileyConstants(**smiley) for smiley in response]

    @protected_method(scope='messages')
    def dialogs(self) -> Optional[List[Dialog]]:
        """
        Returns list of current user's dialogs.

        :return: List of dialogs or None if there are no dialogs
        :rtype: Optional[List[Dialog]]
        """
        logger.debug('Executing "/api/dialogs" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.dialogs, headers=self._authorization_header)
        if response:
            return [Dialog(**dialog) for dialog in response]
        return None

    @protected_method(scope='messages')
    def dialog(self, user_id: Union[int, str]) -> Optional[List[Message]]:
        """
        Returns list of current user's messages with certain user.

        :param user_id: ID/Nickname of the user to get dialog
        :type user_id: Union[int, str]

        :return: List of messages or None if there are no messages
        :rtype: Optional[List[Message]]
        """
        logger.debug('Executing "/api/dialogs/:id" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.dialog(user_id), headers=self._authorization_header)
        if response:
            return [Message(**message) for message in response]
        return None

    @protected_method(scope='messages')
    def delete_dialog(self, user_id: Union[int, str]) -> bool:
        """
        Deletes dialog of current user with certain user.

        :param user_id: ID/Nickname of the user to delete dialog
        :type user_id: Union[int, str]

        :return: Status of message deletion
        :rtype: bool
        """
        logger.debug('Executing "/api/dialogs/:id" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.dialog(user_id),
            headers=self._authorization_header,
            request_type=RequestType.DELETE)
        return 'notice' in response

    @protected_method()
    def create_favorite(self,
                        linked_type: LinkedType,
                        linked_id: int,
                        kind: PersonKind = PersonKind.NONE) -> bool:
        """
        Creates a favorite.

        :param linked_type: Type of object for making favorite
        :type linked_type: LinkedType

        :param linked_id: ID of linked type
        :type linked_id: int

        :param kind: Kind of linked type
            (Required when linked_type is LinkedType.Person)
        :type kind: PersonKind

        :return: Status of favorite create
        :rtype: bool
        """
        logger.debug('Executing '
                     '"/api/favorites/:linked_type/:linked_id(/:kind)" '
                     'method')
        response: Dict[str,
                       Any] = self._request(self._endpoints.favorites_create(
                           linked_type, linked_id, kind),
                                            headers=self._authorization_header,
                                            request_type=RequestType.POST)
        return 'success' in response

    @protected_method()
    def destroy_favorite(self, linked_type: LinkedType, linked_id: int) -> bool:
        """
        Destroys a favorite.

        :param linked_type: Type of object for destroying from favorite
        :type linked_type: LinkedType

        :param linked_id: ID of linked type
        :type linked_id: int

        :return: Status of favorite destroy
        :rtype: bool
        """
        logger.debug('Executing '
                     '"/api/favorites/:linked_type/:linked_id" '
                     'method')
        response: Dict[str,
                       Any] = self._request(self._endpoints.favorites_destroy(
                           linked_type, linked_id),
                                            headers=self._authorization_header,
                                            request_type=RequestType.DELETE)
        return 'success' in response

    @protected_method()
    def reorder_favorite(self,
                         favorite_id: int,
                         new_index: Optional[int] = None) -> bool:
        """
        Reorders a favorite to the new index.

        :param favorite_id: ID of a favorite to reorder
        :type favorite_id: int

        :param new_index: Index of a new position of favorite
        :type new_index: Optional[int]

        :return: Status of reorder
        :rtype: bool
        """
        logger.debug('Executing "/api/favorites/:id/reorder" method')
        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.favorites_reorder(favorite_id),
            headers=self._authorization_header,
            query=Utils.generate_query_dict(new_index=new_index),
            request_type=RequestType.POST)
        if isinstance(response, int):
            return response == ResponseCode.SUCCESS.value
        return False

    def forums(self) -> Optional[List[Forum]]:
        """
        Returns list of forums.

        :returns: List of forums or None if list is empty
        :rtype: Optional[List[Forum]]
        """
        logger.debug('Executing "/api/forums" method')
        response: List[Dict[str, Any]] = self._request(self._endpoints.forums)
        if not response:
            return None
        return [Forum(**forum) for forum in response]

    @protected_method(scope='friends')
    def create_friend(self, friend_id: int):
        """
        Creates (adds) new friend by ID.

        Although it is possible to use this method
        with user nicknames, I recommend to pass user ID
        (In this case there is an additional check for string)

        :param friend_id: ID of a friend to create (add)
        :type friend_id: int

        :return: Status of create (addition)
        :rtype: bool
        """
        logger.debug('Executing "/api/friends/:id" method')

        if isinstance(friend_id, str):
            logger.debug(
                'Adding to friends was canceled because a string was passed')
            return False

        response: Union[Dict[str, Any],
                        int] = self._request(self._endpoints.friend(friend_id),
                                             headers=self._authorization_header,
                                             request_type=RequestType.POST)
        return 'notice' in response

    @protected_method(scope='friends')
    def destroy_friend(self, friend_id: int):
        """
        Destroys (removes) current friend by ID.

        Although it is possible to use this method
        with user nicknames, I recommend to pass user ID
        (In this case there is an additional check for string)

        :param friend_id: ID of a friend to destroy (remove)
        :type friend_id: int

        :return: Status of destroy (removal)
        :rtype: bool
        """
        logger.debug('Executing "/api/friends/:id" method')

        if isinstance(friend_id, str):
            logger.debug(
                'Deletion from friends canceled because a string was passed')
            return False

        response: Union[Dict[str, Any],
                        int] = self._request(self._endpoints.friend(friend_id),
                                             headers=self._authorization_header,
                                             request_type=RequestType.DELETE)
        return 'notice' in response

    def genres(self) -> Optional[List[Genre]]:
        """
        Returns list of genres.

        :return: List of genres or None if list is empty
        :rtype: Optional[List[Genre]]
        """
        logger.debug('Executing "/api/genres" method')
        response: List[Dict[str, Any]] = self._request(self._endpoints.genres)
        if not response:
            return None
        return [Genre(**genre) for genre in response]

    def mangas(self,
               page: Optional[int] = None,
               limit: Optional[int] = None,
               order: Optional[MangaOrder] = None,
               kind: Optional[Union[MangaKind, List[MangaKind]]] = None,
               status: Optional[Union[MangaStatus, List[MangaStatus]]] = None,
               season: Optional[Union[str, List[str]]] = None,
               score: Optional[int] = None,
               genre: Optional[Union[int, List[int]]] = None,
               publisher: Optional[Union[int, List[int]]] = None,
               franchise: Optional[Union[int, List[int]]] = None,
               censored: Optional[MangaCensorship] = None,
               my_list: Optional[Union[MangaList, List[MangaList]]] = None,
               ids: Optional[Union[int, List[int]]] = None,
               exclude_ids: Optional[Union[int, List[int]]] = None,
               search: Optional[str] = None) -> Optional[List[Manga]]:
        """
        Returns mangas list.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param order: Type of order in list
        :type order: Optional[MangaOrder]

        :param kind: Type(s) of manga topic
        :type kind: Optional[Union[MangaKind, List[MangaKind]]

        :param status: Type(s) of manga status
        :type status: Optional[Union[MangaStatus, List[MangaStatus]]]

        :param season: Name(s) of manga seasons
        :type season: Optional[Union[str, List[str]]]

        :param score: Minimal manga score
        :type score: Optional[int]

        :param publisher: Publisher(s) ID
        :type publisher: Optional[Union[int, List[int]]

        :param genre: Genre(s) ID
        :type genre: Optional[Union[int, List[int]]

        :param franchise: Franchise(s) ID
        :type franchise: Optional[Union[int, List[int]]

        :param censored: Type of manga censorship
        :type censored: Optional[MangaCensorship]

        :param my_list: Status(-es) of manga in current user list
            **Note:** If app in restricted mode,
            this won't affect on response.
        :type my_list: Optional[Union[MangaList, List[MangaList]]]

        :param ids: Manga(s) ID to include
        :type ids: Optional[Union[int, List[int]]

        :param exclude_ids: Manga(s) ID to exclude
        :type exclude_ids: Optional[Union[int, List[int]]

        :param search: Search phrase to filter mangas by name
        :type search: Optional[str]

        :return: List of Mangas or None if page is empty
        :rtype: Optional[List[Manga]]
        """
        logger.debug('Executing "/api/mangas" method')
        validated_numbers = Utils.query_numbers_validator(page=[page, 100000],
                                                          limit=[limit, 50],
                                                          score=[score, 9])

        headers: Optional[Dict[str, str]] = None

        if not self.restricted_mode:
            logger.debug('Using "/api/mangas" as protected method')
            headers = self._authorization_header

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.mangas,
            headers=headers,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            order=order,
                                            kind=kind,
                                            status=status,
                                            season=season,
                                            score=validated_numbers['score'],
                                            genre=genre,
                                            publisher=publisher,
                                            franchise=franchise,
                                            censored=censored,
                                            mylist=my_list,
                                            ids=ids,
                                            exclude_ids=exclude_ids,
                                            search=search))
        if response:
            return [Manga(**manga) for manga in response]
        return None

    def manga(self, manga_id: int) -> Manga:
        """
        Returns info about certain manga.

        :param manga_id: Manga ID to get info
        :type manga_id: int

        :return: Manga info
        :rtype: Manga
        """
        logger.debug('Executing "/api/mangas/:id" method')
        response: Dict[str,
                       Any] = self._request(self._endpoints.manga(manga_id))
        return Manga(**response)

    def manga_creators(self, manga_id: int) -> Optional[List[Creator]]:
        """
        Returns creators info of certain manga.

        :param manga_id: Manga ID to get creators
        :type manga_id: int

        :return: List of manga creators or None if list is empty
        :rtype: Optional[List[Creator]]
        """
        logger.debug('Executing "/api/mangas/:id/roles" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.manga_roles(manga_id))
        if not response:
            return None
        return [Creator(**creator) for creator in response]

    def similar_mangas(self, manga_id: int) -> Optional[List[Manga]]:
        """
        Returns list of similar mangas for certain manga.

        :param manga_id: Manga ID to get similar mangas
        :type manga_id: int

        :return: List of similar mangas or None if list is empty
        :rtype: Optional[List[Manga]]
        """
        logger.debug('Executing "/api/mangas/:id/similar" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.similar_mangas(manga_id))
        if not response:
            return None
        return [Manga(**manga) for manga in response]

    def manga_related_content(self, manga_id: int) -> Optional[List[Relation]]:
        """
        Returns list of related content of certain manga.

        :param manga_id: Manga ID to get related content
        :type manga_id: int

        :return: List of relations or None if list is empty
        :rtype: Optional[List[Relation]]
        """
        logger.debug('Executing "/api/mangas/:id/related" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.manga_related_content(manga_id))
        if not response:
            return None
        return [Relation(**relation) for relation in response]

    def manga_franchise_tree(self, manga_id: int) -> FranchiseTree:
        """
        Returns franchise tree of certain manga.

        :param manga_id: Manga ID to get franchise tree
        :type manga_id: int

        :return: Franchise tree of certain manga
        :rtype: FranchiseTree
        """
        logger.debug('Executing "/api/mangas/:id/franchise" method')
        response: Dict[str, Any] = self._request(
            self._endpoints.manga_franchise_tree(manga_id))
        return FranchiseTree(**response)

    def manga_external_links(self, manga_id: int) -> Optional[List[Link]]:
        """
        Returns list of external links of certain manga.

        :param manga_id: Manga ID to get external links
        :type manga_id: int

        :return: List of external links or None if list is empty
        :rtype: Optional[List[Link]]
        """
        logger.debug('Executing "/api/mangas/:id/external_links" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.manga_external_links(manga_id))
        if not response:
            return None
        return [Link(**link) for link in response]

    def manga_topics(self,
                     manga_id: int,
                     page: Optional[int] = None,
                     limit: Optional[int] = None) -> Optional[List[Topic]]:
        """
        Returns list of topics of certain manga.

        If some data are not provided, using default values.

        :param manga_id: Manga ID to get topics
        :type manga_id: int

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of topics or None if page is empty
        :rtype: Optional[List[Topic]]
        """
        logger.debug('Executing "/api/mangas/:id/topics" method')
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.manga_topics(manga_id),
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit']))
        if not response:
            return None
        return [Topic(**topic) for topic in response]

    @protected_method(scope='messages')
    def message(self, message_id) -> Message:
        """
        Returns message info.

        :param message_id: ID of message to get info
        :type message_id: int

        :return: Message info
        :rtype: Message
        """
        logger.debug('Executing "/api/messages/:id" method')
        response: Dict[str,
                       Any] = self._request(self._endpoints.message(message_id),
                                            headers=self._authorization_header)
        return Message(**response)

    @protected_method(scope='messages')
    def create_message(self, body: str, from_id: int,
                       to_id: int) -> Optional[Message]:
        """
        Creates message.

        :param body: Body of message
        :type body: str

        :param from_id: Sender ID
        :type from_id: int

        :param to_id: Reciver ID
        :type to_id: int

        :return: Created message info or None if an error occurred
        :rtype: Optional[Message]
        """
        logger.debug('Executing "/api/messages" method')
        response: Dict[str, Any] = self._request(
            self._endpoints.messages,
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='message',
                                          body=body,
                                          from_id=from_id,
                                          kind='Private',
                                          to_id=to_id),
            request_type=RequestType.POST)
        return Message(**response) if 'errors' not in response else None

    @protected_method(scope='messages')
    def update_message(self, message_id: int, body: str) -> Optional[Message]:
        """
        Updates message.

        :param message_id: ID of message to update
        :type message_id: int

        :param body: New body of message
        :type body: str

        :return: Updated message info or None if an error occurred
        :rtype: Optional[Message]
        """
        logger.debug('Executing "/api/messages/:id" method')
        response: Dict[str, Any] = self._request(
            self._endpoints.message(message_id),
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='message', body=body),
            request_type=RequestType.PATCH)
        return Message(**response) if 'errors' not in response else None

    @protected_method(scope='messages')
    def delete_message(self, message_id: int) -> bool:
        """
        Deletes message.

        :param message_id: ID of message to delete
        :type message_id: int

        :return: Status of message deletion
        :rtype: bool
        """
        logger.debug('Executing "/api/messages/:id" method')
        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.message(message_id),
            headers=self._authorization_header,
            request_type=RequestType.DELETE)
        if isinstance(response, int):
            return response == ResponseCode.NO_CONTENT.value
        return False

    @protected_method(scope='messages')
    def message_mark_read(self,
                          message_ids: Optional[Union[int, List[int]]] = None,
                          is_read: Optional[bool] = None) -> bool:
        """
        Marks read/unread selected messages.

        This method uses generate_query_dict for data dict,
        because there is no need for nested dictionary

        :param message_ids: ID(s) of messages to mark read/unread
        :type message_ids: Optional[Union[int, List[int]]]

        :param is_read: Status of message (read/unread)
        :type is_read: Optional[bool]

        :return: Status of messages read/unread
        :rtype: bool
        """
        logger.debug('Executing "/api/messages/mark_read" method')
        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.messages_mark_read,
            headers=self._authorization_header,
            data=Utils.generate_query_dict(ids=message_ids, is_read=is_read),
            request_type=RequestType.POST)
        if isinstance(response, int):
            return response == ResponseCode.SUCCESS.value
        return False

    @protected_method(scope='messages')
    def read_all_messages(self, message_type: MessageType) -> bool:
        """
        Reads all messages on current user's account.

        This method uses generate_query_dict for data dict,
        because there is no need for nested dictionary

        **Note:** This methods accepts as type only MessageType.NEWS and
        MessageType.NOTIFICATIONS

        :param message_type: Type of messages to read
        :type message_type: MessageType

        :return: Status of messages read
        :rtype: bool
        """
        logger.debug('Executing "/api/messages/read_all" method')
        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.messages_read_all,
            headers=self._authorization_header,
            data=Utils.generate_query_dict(type=message_type),
            request_type=RequestType.POST)
        if isinstance(response, int):
            return response == ResponseCode.SUCCESS.value
        return False

    @protected_method(scope='messages')
    def delete_all_messages(self, message_type: MessageType) -> bool:
        """
        Deletes all messages on current user's account.

        This method uses generate_query_dict for data dict,
        because there is no need for nested dictionary

        **Note:** This methods accepts as type only MessageType.NEWS and
        MessageType.NOTIFICATIONS

        :param message_type: Type of messages to delete
        :type message_type: MessageType

        :return: Status of messages deletion
        :rtype: bool
        """
        logger.debug('Executing "/api/messages/delete_all" method')
        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.messages_delete_all,
            headers=self._authorization_header,
            data=Utils.generate_query_dict(type=message_type),
            request_type=RequestType.POST)
        if isinstance(response, int):
            return response == ResponseCode.SUCCESS.value
        return False

    def people(self, people_id: int) -> People:
        """
        Returns info about a person.

        :param people_id: ID of person to get info
        :type people_id: int

        :return: Info about a person
        :rtype: People
        """
        logger.debug('Executing "/api/people/:id" method')
        response: Dict[str,
                       Any] = self._request(self._endpoints.people(people_id))
        return People(**response)

    def people_search(
            self,
            search: Optional[str] = None,
            people_kind: Optional[PersonKind] = None) -> Optional[List[People]]:
        """
        Returns list of found persons.

        **Note:** This API method only allows PersonKind.SEYU,
        PersonKind.MANGAKA or PersonKind.PRODUCER as kind parameter

        :param search:  Search query for persons
        :type search: Optional[str]

        :param people_kind: Kind of person for searching
        :type people_kind: Optional[PersonKind]

        :return: List of found persons or None if list is empty
        :rtype: Optional[List[People]]
        """
        logger.debug('Executing "/api/people/search" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.people_search,
            query=Utils.generate_query_dict(search=search, kind=people_kind))
        if not response:
            return None
        return [People(**people) for people in response]

    def users(self,
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
        logger.debug('Executing "/api/users" method')
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 100],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.users,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit']))
        if not response:
            return None
        return [User(**user) for user in response]

    def user(self,
             user_id: Union[str, int],
             is_nickname: Optional[bool] = None) -> User:
        """
        Returns info about user.

        :param user_id: User ID/Nickname to get info
        :type user_id: Union[str, int]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: Info about user
        :rtype: User
        """
        logger.debug('Executing "/api/users/:id" method')
        response: Dict[str, Any] = self._request(
            self._endpoints.user(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return User(**response)

    def user_info(self,
                  user_id: Union[str, int],
                  is_nickname: Optional[bool] = None) -> User:
        """
        Returns user's brief info.

        :param user_id: User ID/Nickname to get brief info
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: User's brief info
        :rtype: User
        """
        logger.debug('Executing "/api/users"/:id/info method')
        response: Dict[str, Any] = self._request(
            self._endpoints.user_info(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return User(**response)

    @protected_method()
    def current_user(self) -> User:
        """
        Returns brief info about current user.

        Current user evaluated depending on authorization code.

        :return: Current user brief info
        :rtype: User
        """
        logger.debug('Executing "/api/users/whoami" method')
        response: Dict[str,
                       Any] = self._request(self._endpoints.whoami,
                                            headers=self._authorization_header)
        return User(**response)

    @protected_method()
    def user_sign_out(self):
        """Sends sign out request to API."""
        logger.debug('Executing "/api/users/sign_out" method')
        self._request(self._endpoints.sign_out,
                      headers=self._authorization_header)

    def user_friends(
            self,
            user_id: Union[str, int],
            is_nickname: Optional[bool] = None) -> Optional[List[User]]:
        """
        Returns user's friends.

        :param user_id: User ID/Nickname to get friends
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: List of user's friends or None if list is empty
        :rtype: Optional[List[User]]
        """
        logger.debug('Executing "/api/users/:id/friends" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_friends(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        if not response:
            return None
        return [User(**friend) for friend in response]

    def user_clubs(self,
                   user_id: Union[int, str],
                   is_nickname: Optional[bool] = None) -> Optional[List[Club]]:
        """
        Returns user's clubs.

        :param user_id: User ID/Nickname to get clubs
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: List of user's clubs or None if list is empty
        :rtype: Optional[List[Club]]
        """
        logger.debug('Executing "/api/users/:id/clubs" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_clubs(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        if not response:
            return None
        return [Club(**club) for club in response]

    def user_anime_rates(
            self,
            user_id: Union[int, str],
            is_nickname: Optional[bool] = None,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            status: Optional[AnimeList] = None,
            censored: Optional[AnimeCensorship] = None
    ) -> Optional[List[UserList]]:
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
        :type status: Optional[AnimeList]

        :param censored: Type of anime censorship
        :type censored: Optional[AnimeCensorship]

        :return: User's anime list or None if page is empty
        :rtype: Optional[List[UserList]]
        """
        logger.debug('Executing "/api/users/:id/anime_rates" method')
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 5000],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_anime_rates(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            status=status,
                                            censored=censored))
        if response:
            return [UserList(**user_list) for user_list in response]
        return None

    def user_manga_rates(
            self,
            user_id: Union[int, str],
            is_nickname: Optional[bool] = None,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            censored: Optional[AnimeCensorship] = None
    ) -> Optional[List[UserList]]:
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
        :type censored: Optional[AnimeCensorship]

        :return: User's manga list or None if page is empty
        :rtype: Optional[List[UserList]]
        """
        logger.debug('Executing "/api/users/:id/manga_rates" method')
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 5000],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_manga_rates(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            censored=censored))
        if response:
            return [UserList(**user_list) for user_list in response]
        return None

    def user_favourites(self,
                        user_id: Union[int, str],
                        is_nickname: Optional[bool] = None) -> Favourites:
        """
        Returns user's favourites.

        :param user_id: User ID/Nickname to get favourites
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: User's favourites
        :rtype: Favourites
        """
        logger.debug('Executing "/api/users/:id/favourites" method')
        response: Dict[str, Any] = self._request(
            self._endpoints.user_favourites(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Favourites(**response)

    @protected_method(scope='messages')
    def current_user_messages(
        self,
        user_id: Union[int, str],
        is_nickname: Optional[bool] = None,
        page: Optional[int] = None,
        limit: Optional[int] = None,
        message_type: MessageType = MessageType.NEWS
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
        :type message_type: MessageType

        :return: Current user's messages or None if page is empty
        :rtype: Optional[List[Message]]
        """
        logger.debug('Executing "/api/users/:id/messages" method')
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 100],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_messages(user_id),
            headers=self._authorization_header,
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            type=message_type))
        if response:
            return [Message(**message) for message in response]
        return None

    @protected_method(scope='messages')
    def current_user_unread_messages(
            self,
            user_id: Union[int, str],
            is_nickname: Optional[bool] = None) -> UnreadMessages:
        """
        Returns current user's unread messages counter.

        :param user_id: Current user ID/Nickname to get unread messages
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: Current user's unread messages counters
        :rtype: UnreadMessages
        """
        logger.debug('Executing "/api/users/:id/unread_messages" method')
        response: Dict[str, Any] = self._request(
            self._endpoints.user_unread_messages(user_id),
            headers=self._authorization_header,
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return UnreadMessages(**response)

    def user_history(
            self,
            user_id: Union[int, str],
            is_nickname: Optional[bool] = None,
            page: Optional[int] = None,
            limit: Optional[int] = None,
            target_id: Optional[int] = None,
            target_type: Optional[TargetType] = None
    ) -> Optional[List[History]]:
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
        :type target_type: Optional[TargetType]

        :return: User's history or None if page is empty
        :rtype: Optional[List[History]]
        """
        logger.debug('Executing "/api/users/:id/history" method')
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 100],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_history(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            target_id=target_id,
                                            target_type=target_type))
        if not response:
            return None
        return [History(**history) for history in response]

    def user_bans(self,
                  user_id: Union[int, str],
                  is_nickname: Optional[bool] = None) -> Optional[List[Ban]]:
        """
        Returns list of bans of user.

        :param user_id: User ID/Nickname to get list of bans
        :type user_id: Union[int, str]

        :param is_nickname: Specify if passed user_id is nickname
        :type is_nickname: Optional[bool]

        :return: User's bans or None if list is empty
        :rtype: Optional[List[Ban]]
        """
        logger.debug('Executing "/api/users/:id/bans" method')
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_bans(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        if not response:
            return None
        return [Ban(**ban) for ban in response]
