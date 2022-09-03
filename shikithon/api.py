"""Shikithon API Module.

This is main module with a class
for interacting with the Shikimori API.
"""
import sys
from json import dumps
from time import sleep, time
from typing import Any, Dict, List, Optional, Tuple, Union

from loguru import logger
from ratelimit import limits, sleep_and_retry
from requests import JSONDecodeError, Session

from shikithon.config_cache import ConfigCache
from shikithon.decorators import method_endpoint, protected_method
from shikithon.endpoints import Endpoints
from shikithon.enums.anime import (AnimeCensorship, AnimeDuration, AnimeKind,
                                   AnimeList, AnimeOrder, AnimeRating,
                                   AnimeStatus)
from shikithon.enums.club import (CommentPolicy, ImageUploadPolicy, JoinPolicy,
                                  PagePolicy, TopicPolicy)
from shikithon.enums.comment import CommentableType
from shikithon.enums.favorite import FavoriteLinkedType
from shikithon.enums.history import TargetType
from shikithon.enums.manga import (MangaCensorship, MangaKind, MangaList,
                                   MangaOrder, MangaStatus)
from shikithon.enums.message import MessageType
from shikithon.enums.person import PersonKind
from shikithon.enums.ranobe import (RanobeCensorship, RanobeList, RanobeOrder,
                                    RanobeStatus)
from shikithon.enums.request import RequestType
from shikithon.enums.response import ResponseCode
from shikithon.enums.style import OwnerType
from shikithon.enums.topic import ForumType, TopicLinkedType, TopicType
from shikithon.enums.user_rate import (UserRateStatus, UserRateTarget,
                                       UserRateType)
from shikithon.enums.video import VideoKind
from shikithon.exceptions import (AccessTokenException, MissingAppVariable,
                                  MissingAuthCode, MissingConfigData)
from shikithon.models.abuse_response import AbuseResponse
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
from shikithon.models.created_user_image import CreatedUserImage
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
from shikithon.models.publisher import Publisher
from shikithon.models.ranobe import Ranobe
from shikithon.models.relation import Relation
from shikithon.models.screenshot import Screenshot
from shikithon.models.studio import Studio
from shikithon.models.style import Style
from shikithon.models.topic import Topic
from shikithon.models.unread_messages import UnreadMessages
from shikithon.models.user import User
from shikithon.models.user_list import UserList
from shikithon.models.user_rate import UserRate
from shikithon.models.video import Video
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

        self._endpoints = Endpoints(SHIKIMORI_API_URL, SHIKIMORI_API_URL_V2,
                                    SHIKIMORI_OAUTH_URL)
        self._session = Session()

        self._restricted_mode = False
        self._app_name = ''
        self._client_id = ''
        self._client_secret = ''
        self._redirect_uri = ''
        self._scopes = ''
        self._auth_code = ''
        self._access_token = ''
        self._refresh_token = ''
        self._token_expire = -1

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

    @logger.catch(onerror=lambda _: sys.exit(1))
    def _init_config(self, config: Union[str, Dict[str, str]]):
        """
        Special method for initializing an object.

        This method calls several methods:

        - Validation of config and variables
        - Customizing the session header user agent
        - Getting access/refresh tokens if they are missing
        - Refresh current tokens if they are not valid

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
            tokens_data = self._get_access_token()
            self._update_tokens(tokens_data)

        if self.token_expired():
            logger.debug('Token has expired. Refreshing...')
            self.refresh_tokens()

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
            raise MissingConfigData() from err

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
        - If restricted mode is True, stops validation after app name check.

        :raises MissingAppVariable: If app variable in config is missing
        :raises MissingAuthCode: If auth code is set to empty string
        """
        if not self._app_name:
            raise MissingAppVariable('name')

        if self.restricted_mode:
            return

        if not self._client_id:
            raise MissingAppVariable('Client ID')

        if not self._client_secret:
            raise MissingAppVariable('Client Secret')

        if not self._redirect_uri:
            self._redirect_uri = DEFAULT_REDIRECT_URI

        if not self._scopes:
            raise MissingAppVariable('scopes')

        if self._auth_code:
            return

        auth_link = self._endpoints.authorization_link(self._client_id,
                                                       self._redirect_uri,
                                                       self._scopes)
        raise MissingAuthCode(auth_link)

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
        data_body = {
            'client_id': self._client_id,
            'client_secret': self._client_secret
        }

        if refresh_token:
            logger.info('Refreshing current tokens')
            data_body['grant_type'] = 'refresh_token'
            data_body['refresh_token'] = self._refresh_token
        else:
            logger.info('Getting new tokens')
            data_body['grant_type'] = 'authorization_code'
            data_body['code'] = self._auth_code
            data_body['redirect_uri'] = self._redirect_uri

        oauth_json: Dict[str,
                         Any] = self._request(self._endpoints.oauth_token,
                                              data=data_body,
                                              request_type=RequestType.POST,
                                              output_logging=False)

        try:
            logger.debug('Returning new access and refresh tokens')
            return oauth_json['access_token'], oauth_json['refresh_token']
        except KeyError as err:
            error_info = dumps(oauth_json)
            raise AccessTokenException(error_info) from err

    @logger.catch(onerror=lambda _: sys.exit(1))
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

    @logger.catch(onerror=lambda _: sys.exit(1))
    def refresh_tokens(self):
        """
        Manages tokens refreshing and caching.

        This method gets new access/refresh tokens and
        updates them in current instance, as well as
        caching new config.
        """
        tokens_data = self._get_access_token(refresh_token=True)
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

    @logger.catch(onerror=lambda _: sys.exit(1))
    def _cache_config(self):
        """Updates token expire time and caches new config."""
        self._token_expire = Utils.get_new_expire_time(TOKEN_EXPIRE_TIME)
        ConfigCache.save_config(self.config)
        logger.debug('New expiration time has been set '
                     'and cached configuration has been updated')

    @logger.catch
    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
    def _request(
        self,
        url: str,
        data: Optional[Dict[str, str]] = None,
        files: Optional[Dict[str, Tuple[str, bytes, str]]] = None,
        headers: Optional[Dict[str, str]] = None,
        query: Optional[Dict[str, str]] = None,
        request_type: RequestType = RequestType.GET,
        output_logging: bool = True,
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

        :param files: Binary data for request
        :type files: Optional[Dict[str, Tuple[str, bytes, str]]]

        :param headers: Custom headers for request
        :type headers: Optional[Dict[str, str]]

        :param query: Query data for request
        :type query: Optional[Dict[str, str]]

        :param request_type: Type of current request
        :type request_type: RequestType

        :param output_logging: Parameter for logging JSON response
        :type output_logging: bool

        :return: Response JSON, text or status code
        :rtype: Optional[Union[List[Dict[str, Any]], Dict[str, Any], str]]
        """

        logger.info(f'{request_type.value} {url}')
        if output_logging:
            logger.debug(
                f'Request info details: {data=}, {files=}, {headers=}, {query=}'
            )

        if request_type == RequestType.GET:
            response = self._session.get(url, headers=headers, params=query)
        elif request_type == RequestType.POST:
            response = self._session.post(url,
                                          files=files,
                                          headers=headers,
                                          params=query,
                                          json=data)
        elif request_type == RequestType.PUT:
            response = self._session.put(url,
                                         files=files,
                                         headers=headers,
                                         params=query,
                                         json=data)
        elif request_type == RequestType.PATCH:
            response = self._session.patch(url,
                                           files=files,
                                           headers=headers,
                                           params=query,
                                           json=data)
        elif request_type == RequestType.DELETE:
            response = self._session.delete(url,
                                            headers=headers,
                                            params=query,
                                            json=data)
        else:
            logger.debug('Unknown request_type. Returning None')
            return None

        if response.status_code == ResponseCode.RETRY_LATER.value:
            logger.debug('Hit RPS cooldown. Waiting on request repeat')
            sleep(RATE_LIMIT_RPS_COOLDOWN)
            return self._request(url, data, files, headers, query, request_type,
                                 output_logging)

        try:
            logger.debug('Extracting JSON from response')
            json_response = response.json()
            if output_logging:
                logger.debug(
                    'Successful extraction. '
                    f'Here are the details of the response: {json_response}')
            return json_response
        except JSONDecodeError:
            logger.debug('Can\'t extract JSON. Returning status_code/text')
            return response.status_code if not response.text else response.text

    @logger.catch
    def _semi_protected_method(self, api_name: str) -> Optional[Dict[str, str]]:
        """
        This method utilizes protected method decoration logic
        for such methods, which uses access tokens in some situations.

        :param api_name: Name of API endpoint for calling as protected
        :type api_name: str

        :return: Authorization header with correct tokens or None
        :rtype: Optional[Dict[str, str]]
        """
        logger.debug(f'Checking the possibility of using "{api_name}" '
                     f'as protected method')

        if self.restricted_mode:
            logger.debug(f'It is not possible to use "{api_name}" '
                         'as the protected method '
                         'due to the restricted mode')
            return None

        if self.token_expired():
            logger.debug('Token has expired. Refreshing...')
            self.refresh_tokens()

        logger.debug('All checks for use of the protected '
                     'method have been passed')
        return self._authorization_header

    @method_endpoint('/api/achievements')
    def achievements(self, user_id: int) -> Optional[List[Achievement]]:
        """
        Returns achievements of user by ID.

        :param user_id: User ID for getting achievements
        :type user_id: int

        :return: List of achievements
        :rtype: Optional[List[Achievement]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.achievements,
            query=Utils.generate_query_dict(user_id=user_id))
        return Utils.validate_return_data(response, data_model=Achievement)

    @method_endpoint('/api/animes')
    def animes(self,
               page: Optional[int] = None,
               limit: Optional[int] = None,
               order: Optional[str] = None,
               kind: Optional[Union[str, List[str]]] = None,
               status: Optional[Union[str, List[str]]] = None,
               season: Optional[Union[str, List[str]]] = None,
               score: Optional[int] = None,
               duration: Optional[Union[str, List[str]]] = None,
               rating: Optional[Union[str, List[str]]] = None,
               genre: Optional[Union[int, List[int]]] = None,
               studio: Optional[Union[int, List[int]]] = None,
               franchise: Optional[Union[int, List[int]]] = None,
               censored: Optional[str] = None,
               my_list: Optional[Union[str, List[str]]] = None,
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
        :type order: Optional[str]

        :param kind: Type(s) of anime topics
        :type kind: Optional[Union[str, List[str]]]

        :param status: Type(s) of anime status
        :type status: Optional[Union[str, List[str]]]

        :param season: Name(s) of anime seasons
        :type season: Optional[Union[str, List[str]]]

        :param score: Minimal anime score
        :type score: Optional[int]

        :param duration: Duration size(s) of anime
        :type duration: Optional[Union[str, List[str]]]

        :param rating: Type of anime rating(s)
        :type rating: Optional[Union[str, List[str]]]

        :param genre: Genre(s) ID
        :type genre: Optional[Union[int, List[int]]]

        :param studio: Studio(s) ID
        :type studio: Optional[Union[int, List[int]]]

        :param franchise: Franchise(s) ID
        :type franchise: Optional[Union[int, List[int]]]

        :param censored: Type of anime censorship
        :type censored: Optional[str]

        :param my_list: Status(-es) of anime in current user list
            **Note:** If app is in restricted mode,
            this parameter won't affect on response.
        :type my_list: Optional[Union[str, List[str]]]

        :param ids: Anime(s) ID to include
        :type ids: Optional[Union[int, List[int]]]

        :param exclude_ids: Anime(s) ID to exclude
        :type exclude_ids: Optional[Union[int, List[int]]]

        :param search: Search phrase to filter animes by name
        :type search: Optional[str]

        :return: Animes list
        :rtype: Optional[List[Anime]]
        """
        if not Utils.validate_enum_params({
                AnimeOrder: order,
                AnimeKind: kind,
                AnimeStatus: status,
                AnimeDuration: duration,
                AnimeRating: rating,
                AnimeCensorship: censored,
                AnimeList: my_list,
        }):
            return None

        validated_numbers = Utils.query_numbers_validator(page=[page, 100000],
                                                          limit=[limit, 50],
                                                          score=[score, 9])

        headers = self._user_agent

        if my_list:
            headers = self._semi_protected_method('/api/animes')

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
        return Utils.validate_return_data(response, data_model=Anime)

    @method_endpoint('/api/animes/:id')
    def anime(self, anime_id: int) -> Optional[Anime]:
        """
        Returns info about certain anime.

        :param anime_id: Anime ID to get info
        :type anime_id: int

        :return: Anime info
        :rtype: Optional[Anime]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.anime(anime_id))
        return Utils.validate_return_data(response, data_model=Anime)

    @method_endpoint('/api/animes/:id/roles')
    def anime_creators(self, anime_id: int) -> Optional[List[Creator]]:
        """
        Returns creators info of certain anime.

        :param anime_id: Anime ID to get creators
        :type anime_id: int

        :return: List of anime creators
        :rtype: Optional[List[Creator]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_roles(anime_id))
        return Utils.validate_return_data(response, data_model=Creator)

    @method_endpoint('/api/animes/:id/similar')
    def similar_animes(self, anime_id: int) -> Optional[List[Anime]]:
        """
        Returns list of similar animes for certain anime.

        :param anime_id: Anime ID to get similar animes
        :type anime_id: int

        :return: List of similar animes
        :rtype: Optional[List[Anime]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.similar_animes(anime_id))
        return Utils.validate_return_data(response, data_model=Anime)

    @method_endpoint('/api/animes/:id/related')
    def anime_related_content(self, anime_id: int) -> Optional[List[Relation]]:
        """
        Returns list of related content of certain anime.

        :param anime_id: Anime ID to get related content
        :type anime_id: int

        :return: List of relations
        :rtype: Optional[List[Relation]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_related_content(anime_id))
        return Utils.validate_return_data(response, data_model=Relation)

    @method_endpoint('/api/animes/:id/screenshots')
    def anime_screenshots(self, anime_id: int) -> Optional[List[Screenshot]]:
        """
        Returns list of screenshot links of certain anime.

        :param anime_id: Anime ID to get screenshot links
        :type anime_id: int

        :return: List of screenshot links
        :rtype: Optional[List[Screenshot]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_screenshots(anime_id))
        return Utils.validate_return_data(response, data_model=Screenshot)

    @method_endpoint('/api/animes/:id/franchise')
    def anime_franchise_tree(self, anime_id: int) -> Optional[FranchiseTree]:
        """
        Returns franchise tree of certain anime.

        :param anime_id: Anime ID to get franchise tree
        :type anime_id: int

        :return: Franchise tree of certain anime
        :rtype: Optional[FranchiseTree]
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.anime_franchise_tree(anime_id))
        return Utils.validate_return_data(response, data_model=FranchiseTree)

    @method_endpoint('/api/animes/:id/external_links')
    def anime_external_links(self, anime_id: int) -> Optional[List[Link]]:
        """
        Returns list of external links of certain anime.

        :param anime_id: Anime ID to get external links
        :type anime_id: int

        :return: List of external links
        :rtype: Optional[List[Link]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_external_links(anime_id))
        return Utils.validate_return_data(response, data_model=Link)

    @method_endpoint('/api/animes/:id/topics')
    def anime_topics(self,
                     anime_id: int,
                     page: Optional[int] = None,
                     limit: Optional[int] = None,
                     kind: Optional[str] = None,
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

        :param kind: Kind of anime
        :type kind: Optional[str]

        :param episode: Number of anime episode
        :type episode: Optional[int]

        :return: List of topics
        :rtype: Optional[List[Topic]]
        """
        if not Utils.validate_enum_params({AnimeKind: kind}):
            return None

        validated_numbers = Utils.query_numbers_validator(page=[page, 100000],
                                                          limit=[limit, 30])

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_topics(anime_id),
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            kind=kind,
                                            episode=episode))
        return Utils.validate_return_data(response, data_model=Topic)

    @method_endpoint('/api/animes/:anime_id/videos')
    def anime_videos(self, anime_id: int) -> Optional[List[Video]]:
        """
        Returns anime videso.

        :param anime_id: Anime ID to get videos
        :type anime_id: int

        :return: Anime videos list
        :rtype: Optional[List[Video]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_videos(anime_id))
        return Utils.validate_return_data(response, data_model=Video)

    @method_endpoint('/api/animes/:anime_id/videos')
    @protected_method('content')
    def create_anime_video(self, anime_id: int, kind: str, name: str,
                           url: str) -> Optional[Video]:
        """
        Creates anime video.

        :param anime_id: Anime ID to create video
        :type anime_id: int

        :param kind: Kind of video
        :type kind: str

        :param name: Name of video
        :type name: str

        :param url: URL of video
        :type url: str

        :return: Created video info
        :rtype: Optional[Video]
        """
        if not Utils.validate_enum_params({VideoKind: kind}):
            return None

        data_dict: Dict[str, Any] = Utils.generate_data_dict(dict_name='video',
                                                             kind=kind,
                                                             name=name,
                                                             url=url)
        response: Dict[str, Any] = self._request(
            self._endpoints.anime_videos(anime_id),
            headers=self._authorization_header,
            data=data_dict,
            request_type=RequestType.POST)
        return Utils.validate_return_data(response, data_model=Video)

    @method_endpoint('/api/animes/:anime_id/videos/:id')
    @protected_method('content')
    def delete_anime_video(self, anime_id: int, video_id: int) -> bool:
        """
        Deletes anime video.

        :param anime_id: Anime ID to delete video
        :type anime_id: int

        :param video_id: Video ID to delete
        :type video_id: str

        :return: Status of video deletion
        :rtype: bool
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.anime_video(
                           anime_id, video_id),
                                            headers=self._authorization_header,
                                            request_type=RequestType.DELETE)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/appears')
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
        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.appears,
            headers=self._authorization_header,
            data=Utils.generate_query_dict(ids=comment_ids),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response,
                                          response_code=ResponseCode.SUCCESS)

    @method_endpoint('/api/bans')
    def bans(self,
             page: Optional[int] = None,
             limit: Optional[int] = None) -> Optional[List[Ban]]:
        """
        Returns list of recent bans on Shikimori.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of recent bans
        :rtype: Optional[List[Ban]]
        """
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.bans_list,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit']))
        return Utils.validate_return_data(response, data_model=Ban)

    @method_endpoint('/api/calendar')
    def calendar(
            self,
            censored: Optional[str] = None) -> Optional[List[CalendarEvent]]:
        """
        Returns current calendar events.

        :param censored: Status of censorship for events
        :type censored: Optional[str]

        :return: List of calendar events
        :rtype: Optional[List[CalendarEvent]]
        """
        if not Utils.validate_enum_params({AnimeCensorship: censored}):
            return None

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.calendar,
            query=Utils.generate_query_dict(censored=censored))
        return Utils.validate_return_data(response, data_model=CalendarEvent)

    @method_endpoint('/api/characters/:id')
    def character(self, character_id: int) -> Optional[Character]:
        """
        Returns character info by ID.

        :param character_id: ID of character to get info
        :type character_id: int

        :return: Character info
        :rtype: Optional[Character]
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.character(character_id))
        return Utils.validate_return_data(response, data_model=Character)

    @method_endpoint('/api/characters/search')
    def character_search(self,
                         search: Optional[str] = None
                        ) -> Optional[List[Character]]:
        """
        Returns list of found characters.

        :param search: Search query for characters
        :type search: Optional[str]

        :return: List of found characters
        :rtype: Optional[List[Character]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.character_search,
            query=Utils.generate_query_dict(search=search))
        return Utils.validate_return_data(response, data_model=Character)

    @method_endpoint('/api/clubs')
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

        :return: Clubs list
        :rtype: Optional[List[Club]]
        """
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.clubs,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            search=search))
        return Utils.validate_return_data(response, data_model=Club)

    @method_endpoint('/api/clubs/:id')
    def club(self, club_id: int) -> Optional[Club]:
        """
        Returns info about club.

        :param club_id: Club ID to get info
        :type club_id: int

        :return: Info about club
        :rtype: Optional[Club]
        """
        response: Dict[str, Any] = self._request(self._endpoints.club(club_id))
        return Utils.validate_return_data(response, data_model=Club)

    @method_endpoint('/api/clubs/:id')
    @protected_method('clubs')
    def club_update(
            self,
            club_id: int,
            name: Optional[str] = None,
            join_policy: Optional[str] = None,
            description: Optional[str] = None,
            display_images: Optional[bool] = None,
            comment_policy: Optional[str] = None,
            topic_policy: Optional[str] = None,
            page_policy: Optional[str] = None,
            image_upload_policy: Optional[str] = None,
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
        :type join_policy: Optional[str]

        :param comment_policy: New comment policy of club
        :type comment_policy: Optional[str]

        :param topic_policy: New topic policy of club
        :type topic_policy: Optional[str]

        :param page_policy: New page policy of club
        :type page_policy: Optional[str]

        :param image_upload_policy: New image upload policy of club
        :type image_upload_policy: Optional[str]

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

        :return: Updated club info
        :rtype: Optional[Club]
        """
        if not Utils.validate_enum_params({
                JoinPolicy: join_policy,
                CommentPolicy: comment_policy,
                TopicPolicy: topic_policy,
                PagePolicy: page_policy,
                ImageUploadPolicy: image_upload_policy
        }):
            return None

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
        return Utils.validate_return_data(response, data_model=Club)

    @method_endpoint('/api/clubs/:id/animes')
    def club_animes(self, club_id: int) -> Optional[List[Anime]]:
        """
        Returns anime list of club.

        :param club_id: Club ID to get anime list
        :type club_id: int

        :return: Club anime list
        :rtype: Optional[List[Anime]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.club_animes(club_id))
        return Utils.validate_return_data(response, data_model=Anime)

    @method_endpoint('/api/clubs/:id/mangas')
    def club_mangas(self, club_id: int) -> Optional[List[Manga]]:
        """
        Returns manga list of club.

        :param club_id: Club ID to get manga list
        :type club_id: int

        :return: Club manga list
        :rtype: Optional[List[Manga]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.club_mangas(club_id))
        return Utils.validate_return_data(response, data_model=Manga)

    @method_endpoint('/api/clubs/:id/ranobe')
    def club_ranobe(self, club_id: int) -> Optional[List[Ranobe]]:
        """
        Returns ranobe list of club.

        :param club_id: Club ID to get ranobe list
        :type club_id: int

        :return: Club ranobe list
        :rtype: Optional[List[Ranobe]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.club_ranobe(club_id))
        return Utils.validate_return_data(response, data_model=Ranobe)

    @method_endpoint('/api/clubs/:id/characters')
    def club_characters(self, club_id: int) -> Optional[List[Character]]:
        """
        Returns character list of club.

        :param club_id: Club ID to get character list
        :type club_id: int

        :return: Club character list
        :rtype: Optional[List[Character]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.club_characters(club_id))
        return Utils.validate_return_data(response, data_model=Character)

    @method_endpoint('/api/clubs/:id/members')
    def club_members(self, club_id: int) -> Optional[List[User]]:
        """
        Returns member list of club.

        :param club_id: Club ID to get member list
        :type club_id: int

        :return: Club member list
        :rtype: Optional[List[User]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.club_members(club_id))
        return Utils.validate_return_data(response, data_model=User)

    @method_endpoint('/api/clubs/:id/images')
    def club_images(self, club_id: int) -> Optional[List[ClubImage]]:
        """
        Returns images of club.

        :param club_id: Club ID to get images
        :type club_id: int

        :return: Club's images
        :rtype: Optional[List[ClubImage]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.club_images(club_id))
        return Utils.validate_return_data(response, data_model=ClubImage)

    @method_endpoint('/api/clubs/:id/join')
    @protected_method('clubs')
    def club_join(self, club_id: int):
        """
        Joins club by ID.

        :param club_id: Club ID to join
        :type club_id: int

        :return: Status of join
        :rtype: bool
        """
        response: Union[Dict[str, Any],
                        int] = self._request(self._endpoints.club_join(club_id),
                                             headers=self._authorization_header,
                                             request_type=RequestType.POST)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/clubs/:id/leave')
    @protected_method('clubs')
    def club_leave(self, club_id: int) -> bool:
        """
        Leaves club by ID.

        :param club_id: Club ID to leave
        :type club_id: int

        :return: Status of leave
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.club_leave(club_id),
            headers=self._authorization_header,
            request_type=RequestType.POST)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/comments')
    def comments(self,
                 commentable_id: int,
                 commentable_type: str,
                 page: Optional[int] = None,
                 limit: Optional[int] = None,
                 desc: Optional[int] = None) -> Optional[List[Comment]]:
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
        :rtype: Optional[List[Comment]]
        """
        if not Utils.validate_enum_params({CommentableType: commentable_type}):
            return None

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
        return Utils.validate_return_data(response, data_model=Comment)

    @method_endpoint('/api/comments/:id')
    def comment(self, comment_id: int) -> Optional[Comment]:
        """
        Returns comment info.

        :param comment_id: ID of comment
        :type comment_id: int

        :return: Comment info
        :rtype: Optional[Comment]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.comment(comment_id))
        return Utils.validate_return_data(response, data_model=Comment)

    @method_endpoint('/api/comments')
    @protected_method('comments')
    def create_comment(self,
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
        return Utils.validate_return_data(response, data_model=Comment)

    @method_endpoint('/api/comments/:id')
    @protected_method('comments')
    def update_comment(self, comment_id: int, body: str) -> Optional[Comment]:
        """
        Updates comment.

        :param comment_id: ID of comment to update
        :type comment_id: int

        :param body: New body of comment
        :type body: str

        :return: Updated comment info
        :rtype: Optional[Comment]
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.comment(comment_id),
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='comment', body=body),
            request_type=RequestType.PATCH)
        return Utils.validate_return_data(response, data_model=Comment)

    @method_endpoint('/api/comments/:id')
    @protected_method('comments')
    def delete_comment(self, comment_id: int) -> bool:
        """
        Deletes comment.

        :param comment_id: ID of comment to delete
        :type comment_id: int

        :return: Status of comment deletion
        :rtype: bool
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.comment(comment_id),
                                            headers=self._authorization_header,
                                            request_type=RequestType.DELETE)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/constants/anime')
    def anime_constants(self) -> Optional[AnimeConstants]:
        """
        Returns anime constants values.

        :return: Anime constants values
        :rtype: Optional[AnimeConstants]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.anime_constants)
        return Utils.validate_return_data(response, data_model=AnimeConstants)

    @method_endpoint('/api/constants/manga')
    def manga_constants(self) -> Optional[MangaConstants]:
        """
        Returns manga constants values.

        :return: Manga constants values
        :rtype: Optional[MangaConstants]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.manga_constants)
        return Utils.validate_return_data(response, data_model=MangaConstants)

    @method_endpoint('/api/constants/user_rate')
    def user_rate_constants(self) -> Optional[UserRateConstants]:
        """
        Returns user rate constants values.

        :return: User rate constants values
        :rtype: Optional[UserRateConstants]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.user_rate_constants)
        return Utils.validate_return_data(response,
                                          data_model=UserRateConstants)

    @method_endpoint('/api/constants/club')
    def club_constants(self) -> Optional[ClubConstants]:
        """
        Returns club constants values.

        :return: Club constants values
        :rtype: Optional[ClubConstants]
        """
        response: Dict[str, Any] = self._request(self._endpoints.club_constants)
        return Utils.validate_return_data(response, data_model=ClubConstants)

    @method_endpoint('/api/constants/smileys')
    def smileys_constants(self) -> Optional[List[SmileyConstants]]:
        """
        Returns list of smileys constants values.

        :return: List of smileys constants values
        :rtype: Optional[List[SmileyConstants]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.smileys_constants)
        return Utils.validate_return_data(response, data_model=SmileyConstants)

    @method_endpoint('/api/dialogs')
    @protected_method('messages')
    def dialogs(self) -> Optional[List[Dialog]]:
        """
        Returns list of current user's dialogs.

        :return: List of dialogs
        :rtype: Optional[List[Dialog]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.dialogs, headers=self._authorization_header)
        return Utils.validate_return_data(response, data_model=Dialog)

    @method_endpoint('/api/dialogs/:id')
    @protected_method('messages')
    def dialog(self, user_id: Union[int, str]) -> Optional[List[Message]]:
        """
        Returns list of current user's messages with certain user.

        :param user_id: ID/Nickname of the user to get dialog
        :type user_id: Union[int, str]

        :return: List of messages
        :rtype: Optional[List[Message]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.dialog(user_id), headers=self._authorization_header)
        return Utils.validate_return_data(response, data_model=Message)

    @method_endpoint('/api/dialogs/:id')
    @protected_method('messages')
    def delete_dialog(self, user_id: Union[int, str]) -> bool:
        """
        Deletes dialog of current user with certain user.

        :param user_id: ID/Nickname of the user to delete dialog
        :type user_id: Union[int, str]

        :return: Status of message deletion
        :rtype: bool
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.dialog(user_id),
            headers=self._authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/favorites/:linked_type/:linked_id(/:kind)')
    @protected_method()
    def create_favorite(self,
                        linked_type: str,
                        linked_id: int,
                        kind: str = PersonKind.NONE.value) -> bool:
        """
        Creates a favorite.

        :param linked_type: Type of object for making favorite
        :type linked_type: str

        :param linked_id: ID of linked type
        :type linked_id: int

        :param kind: Kind of linked type
            (Required when linked_type is 'Person')
        :type kind: str

        :return: Status of favorite create
        :rtype: bool
        """
        if not Utils.validate_enum_params({
                FavoriteLinkedType: linked_type,
                PersonKind: kind
        }):
            return False

        response: Dict[str,
                       Any] = self._request(self._endpoints.favorites_create(
                           linked_type, linked_id, kind),
                                            headers=self._authorization_header,
                                            request_type=RequestType.POST)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/favorites/:linked_type/:linked_id')
    @protected_method()
    def destroy_favorite(self, linked_type: str, linked_id: int) -> bool:
        """
        Destroys a favorite.

        :param linked_type: Type of object for destroying from favorite
        :type linked_type: str

        :param linked_id: ID of linked type
        :type linked_id: int

        :return: Status of favorite destroy
        :rtype: bool
        """
        if not Utils.validate_enum_params({FavoriteLinkedType: linked_type}):
            return False

        response: Dict[str,
                       Any] = self._request(self._endpoints.favorites_destroy(
                           linked_type, linked_id),
                                            headers=self._authorization_header,
                                            request_type=RequestType.DELETE)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/favorites/:id/reorder')
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
        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.favorites_reorder(favorite_id),
            headers=self._authorization_header,
            query=Utils.generate_query_dict(new_index=new_index),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response,
                                          response_code=ResponseCode.SUCCESS)

    @method_endpoint('/api/forums')
    def forums(self) -> Optional[List[Forum]]:
        """
        Returns list of forums.

        :returns: List of forums
        :rtype: Optional[List[Forum]]
        """
        response: List[Dict[str, Any]] = self._request(self._endpoints.forums)
        return Utils.validate_return_data(response, data_model=Forum)

    @method_endpoint('/api/friends/:id')
    @protected_method('friends')
    def create_friend(self, friend_id: int):
        """
        Creates (adds) new friend by ID.

        :param friend_id: ID of a friend to create (add)
        :type friend_id: int

        :return: Status of create (addition)
        :rtype: bool
        """
        response: Union[Dict[str, Any],
                        int] = self._request(self._endpoints.friend(friend_id),
                                             headers=self._authorization_header,
                                             request_type=RequestType.POST)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/friends/:id')
    @protected_method('friends')
    def destroy_friend(self, friend_id: int):
        """
        Destroys (removes) current friend by ID.

        :param friend_id: ID of a friend to destroy (remove)
        :type friend_id: int

        :return: Status of destroy (removal)
        :rtype: bool
        """
        response: Union[Dict[str, Any],
                        int] = self._request(self._endpoints.friend(friend_id),
                                             headers=self._authorization_header,
                                             request_type=RequestType.DELETE)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/genres')
    def genres(self) -> Optional[List[Genre]]:
        """
        Returns list of genres.

        :return: List of genres
        :rtype: Optional[List[Genre]]
        """
        response: List[Dict[str, Any]] = self._request(self._endpoints.genres)
        return Utils.validate_return_data(response, data_model=Genre)

    @method_endpoint('/api/mangas')
    def mangas(self,
               page: Optional[int] = None,
               limit: Optional[int] = None,
               order: Optional[str] = None,
               kind: Optional[Union[str, List[str]]] = None,
               status: Optional[Union[str, List[str]]] = None,
               season: Optional[Union[str, List[str]]] = None,
               score: Optional[int] = None,
               genre: Optional[Union[int, List[int]]] = None,
               publisher: Optional[Union[int, List[int]]] = None,
               franchise: Optional[Union[int, List[int]]] = None,
               censored: Optional[str] = None,
               my_list: Optional[Union[str, List[str]]] = None,
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
        :type order: Optional[str]

        :param kind: Type(s) of manga topic
        :type kind: Optional[Union[str, List[str]]

        :param status: Type(s) of manga status
        :type status: Optional[Union[str, List[str]]]

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
        :type censored: Optional[str]

        :param my_list: Status(-es) of manga in current user list
            **Note:** If app in restricted mode,
            this won't affect on response.
        :type my_list: Optional[Union[str, List[str]]]

        :param ids: Manga(s) ID to include
        :type ids: Optional[Union[int, List[int]]

        :param exclude_ids: Manga(s) ID to exclude
        :type exclude_ids: Optional[Union[int, List[int]]

        :param search: Search phrase to filter mangas by name
        :type search: Optional[str]

        :return: List of Mangas
        :rtype: Optional[List[Manga]]
        """
        if not Utils.validate_enum_params({
                MangaOrder: order,
                MangaKind: kind,
                MangaStatus: status,
                MangaCensorship: censored,
                MangaList: my_list
        }):
            return None

        validated_numbers = Utils.query_numbers_validator(page=[page, 100000],
                                                          limit=[limit, 50],
                                                          score=[score, 9])

        headers: Dict[str, str] = self._user_agent

        if my_list:
            headers = self._semi_protected_method('/api/mangas')

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
        return Utils.validate_return_data(response, data_model=Manga)

    @method_endpoint('/api/mangas/:id')
    def manga(self, manga_id: int) -> Optional[Manga]:
        """
        Returns info about certain manga.

        :param manga_id: Manga ID to get info
        :type manga_id: int

        :return: Manga info
        :rtype: Optional[Manga]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.manga(manga_id))
        return Utils.validate_return_data(response, data_model=Manga)

    @method_endpoint('/api/mangas/:id/roles')
    def manga_creators(self, manga_id: int) -> Optional[List[Creator]]:
        """
        Returns creators info of certain manga.

        :param manga_id: Manga ID to get creators
        :type manga_id: int

        :return: List of manga creators
        :rtype: Optional[List[Creator]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.manga_roles(manga_id))
        return Utils.validate_return_data(response, data_model=Creator)

    @method_endpoint('/api/mangas/:id/similar')
    def similar_mangas(self, manga_id: int) -> Optional[List[Manga]]:
        """
        Returns list of similar mangas for certain manga.

        :param manga_id: Manga ID to get similar mangas
        :type manga_id: int

        :return: List of similar mangas
        :rtype: Optional[List[Manga]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.similar_mangas(manga_id))
        return Utils.validate_return_data(response, data_model=Manga)

    @method_endpoint('/api/mangas/:id/related')
    def manga_related_content(self, manga_id: int) -> Optional[List[Relation]]:
        """
        Returns list of related content of certain manga.

        :param manga_id: Manga ID to get related content
        :type manga_id: int

        :return: List of relations
        :rtype: Optional[List[Relation]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.manga_related_content(manga_id))
        return Utils.validate_return_data(response, data_model=Relation)

    @method_endpoint('/api/mangas/:id/franchise')
    def manga_franchise_tree(self, manga_id: int) -> Optional[FranchiseTree]:
        """
        Returns franchise tree of certain manga.

        :param manga_id: Manga ID to get franchise tree
        :type manga_id: int

        :return: Franchise tree of certain manga
        :rtype: Optional[FranchiseTree]
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.manga_franchise_tree(manga_id))
        return Utils.validate_return_data(response, data_model=FranchiseTree)

    @method_endpoint('/api/mangas/:id/external_links')
    def manga_external_links(self, manga_id: int) -> Optional[List[Link]]:
        """
        Returns list of external links of certain manga.

        :param manga_id: Manga ID to get external links
        :type manga_id: int

        :return: List of external links
        :rtype: Optional[List[Link]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.manga_external_links(manga_id))
        return Utils.validate_return_data(response, data_model=Link)

    @method_endpoint('/api/mangas/:id/topics')
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

        :return: List of topics
        :rtype: Optional[List[Topic]]
        """
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.manga_topics(manga_id),
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit']))
        return Utils.validate_return_data(response, data_model=Topic)

    @method_endpoint('/api/messages/:id')
    @protected_method('messages')
    def message(self, message_id: int) -> Optional[Message]:
        """
        Returns message info.

        :param message_id: ID of message to get info
        :type message_id: int

        :return: Message info
        :rtype: Optional[Message]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.message(message_id),
                                            headers=self._authorization_header)
        return Utils.validate_return_data(response, data_model=Message)

    @method_endpoint('/api/messages')
    @protected_method('messages')
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

        :return: Created message info
        :rtype: Optional[Message]
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.messages,
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='message',
                                          body=body,
                                          from_id=from_id,
                                          kind='Private',
                                          to_id=to_id),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response, data_model=Message)

    @method_endpoint('/api/messages/:id')
    @protected_method('messages')
    def update_message(self, message_id: int, body: str) -> Optional[Message]:
        """
        Updates message.

        :param message_id: ID of message to update
        :type message_id: int

        :param body: New body of message
        :type body: str

        :return: Updated message info
        :rtype: Optional[Message]
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.message(message_id),
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='message', body=body),
            request_type=RequestType.PATCH)
        return Utils.validate_return_data(response, data_model=Message)

    @method_endpoint('/api/messages/:id')
    @protected_method('messages')
    def delete_message(self, message_id: int) -> bool:
        """
        Deletes message.

        :param message_id: ID of message to delete
        :type message_id: int

        :return: Status of message deletion
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.message(message_id),
            headers=self._authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_return_data(response,
                                          response_code=ResponseCode.NO_CONTENT)

    @method_endpoint('/api/messages/mark_read')
    @protected_method('messages')
    def mark_messages_read(self,
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
        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.messages_mark_read,
            headers=self._authorization_header,
            data=Utils.generate_query_dict(ids=message_ids, is_read=is_read),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response,
                                          response_code=ResponseCode.SUCCESS)

    @method_endpoint('/api/messages/read_all')
    @protected_method('messages')
    def read_all_messages(self, message_type: str) -> bool:
        """
        Reads all messages on current user's account.

        This method uses generate_query_dict for data dict,
        because there is no need for nested dictionary

        **Note:** This methods accepts as type only 'news' and
        'notifications'

        :param message_type: Type of messages to read
        :type message_type: str

        :return: Status of messages read
        :rtype: bool
        """
        if not Utils.validate_enum_params({MessageType: message_type}):
            return False

        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.messages_read_all,
            headers=self._authorization_header,
            data=Utils.generate_query_dict(type=message_type),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response,
                                          response_code=ResponseCode.SUCCESS)

    @method_endpoint('/api/messages/delete_all')
    @protected_method('messages')
    def delete_all_messages(self, message_type: str) -> bool:
        """
        Deletes all messages on current user's account.

        This method uses generate_query_dict for data dict,
        because there is no need for nested dictionary

        **Note:** This methods accepts as type only 'news' and
        'notifications'

        :param message_type: Type of messages to delete
        :type message_type: str

        :return: Status of messages deletion
        :rtype: bool
        """
        if not Utils.validate_enum_params({MessageType: message_type}):
            return False

        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.messages_delete_all,
            headers=self._authorization_header,
            data=Utils.generate_query_dict(type=message_type),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response,
                                          response_code=ResponseCode.SUCCESS)

    @method_endpoint('/api/people/:id')
    def people(self, people_id: int) -> Optional[People]:
        """
        Returns info about a person.

        :param people_id: ID of person to get info
        :type people_id: int

        :return: Info about a person
        :rtype: Optional[People]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.people(people_id))
        return Utils.validate_return_data(response, data_model=People)

    @method_endpoint('/api/people/search')
    def people_search(
            self,
            search: Optional[str] = None,
            people_kind: Optional[str] = None) -> Optional[List[People]]:
        """
        Returns list of found persons.

        **Note:** This API method only allows 'seyu',
        'mangaka' or 'producer' as kind parameter

        :param search:  Search query for persons
        :type search: Optional[str]

        :param people_kind: Kind of person for searching
        :type people_kind: Optional[str]

        :return: List of found persons
        :rtype: Optional[List[People]]
        """
        if not Utils.validate_enum_params({PersonKind: people_kind}):
            return None

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.people_search,
            query=Utils.generate_query_dict(search=search, kind=people_kind))
        return Utils.validate_return_data(response, data_model=People)

    @method_endpoint('/api/publishers')
    def publishers(self) -> Optional[List[Publisher]]:
        """
        Returns list of publishers.

        :return: List of publishers
        :rtype: Optional[List[Publisher]]
        """
        response: List[Dict[str,
                            Any]] = self._request(self._endpoints.publishers)
        return Utils.validate_return_data(response, data_model=Publisher)

    @method_endpoint('/api/ranobe')
    def ranobes(self,
                page: Optional[int] = None,
                limit: Optional[int] = None,
                order: Optional[str] = None,
                status: Optional[Union[str, List[str]]] = None,
                season: Optional[Union[str, List[str]]] = None,
                score: Optional[int] = None,
                genre: Optional[Union[int, List[int]]] = None,
                publisher: Optional[Union[int, List[int]]] = None,
                franchise: Optional[Union[int, List[int]]] = None,
                censored: Optional[str] = None,
                my_list: Optional[Union[str, List[str]]] = None,
                ids: Optional[Union[int, List[int]]] = None,
                exclude_ids: Optional[Union[int, List[int]]] = None,
                search: Optional[str] = None) -> Optional[List[Ranobe]]:
        """
        Returns ranobe list.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param order: Type of order in list
        :type order: Optional[str]

        :param status: Type(s) of ranobe status
        :type status: Optional[Union[str, List[str]]]

        :param season: Name(s) of ranobe seasons
        :type season: Optional[Union[str, List[str]]]

        :param score: Minimal ranobe score
        :type score: Optional[int]

        :param publisher: Publisher(s) ID
        :type publisher: Optional[Union[int, List[int]]

        :param genre: Genre(s) ID
        :type genre: Optional[Union[int, List[int]]

        :param franchise: Franchise(s) ID
        :type franchise: Optional[Union[int, List[int]]

        :param censored: Type of ranobe censorship
        :type censored: Optional[str]

        :param my_list: Status(-es) of ranobe in current user list
            **Note:** If app in restricted mode,
            this won't affect on response.
        :type my_list: Optional[Union[str, List[str]]]

        :param ids: Ranobe(s) ID to include
        :type ids: Optional[Union[int, List[int]]

        :param exclude_ids: Ranobe(s) ID to exclude
        :type exclude_ids: Optional[Union[int, List[int]]

        :param search: Search phrase to filter ranobe by name
        :type search: Optional[str]

        :return: List of Ranobe
        :rtype: Optional[List[Ranobe]]
        """
        if not Utils.validate_enum_params({
                RanobeOrder: order,
                RanobeStatus: status,
                RanobeList: my_list,
                RanobeCensorship: censored
        }):
            return None

        validated_numbers = Utils.query_numbers_validator(page=[page, 100000],
                                                          limit=[limit, 50],
                                                          score=[score, 9])

        headers: Dict[str, str] = self._user_agent

        if my_list:
            headers = self._semi_protected_method('/api/ranobe')

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.ranobes,
            headers=headers,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            order=order,
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
        return Utils.validate_return_data(response, data_model=Ranobe)

    @method_endpoint('/api/ranobe/:id')
    def ranobe(self, ranobe_id: int) -> Optional[Ranobe]:
        """
        Returns info about certain ranobe.

        :param ranobe_id: Ranobe ID to get info
        :type ranobe_id: int

        :return: Ranobe info
        :rtype: Optional[Ranobe]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.ranobe(ranobe_id))
        return Utils.validate_return_data(response, data_model=Ranobe)

    @method_endpoint('/api/ranobe/:id/roles')
    def ranobe_creators(self, ranobe_id: int) -> Optional[List[Creator]]:
        """
        Returns creators info of certain ranobe.

        :param ranobe_id: Ranobe ID to get creators
        :type ranobe_id: int

        :return: List of ranobe creators
        :rtype: Optional[List[Creator]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.ranobe_roles(ranobe_id))
        return Utils.validate_return_data(response, data_model=Creator)

    @method_endpoint('/api/ranobe/:id/similar')
    def similar_ranobes(self, ranobe_id: int) -> Optional[List[Ranobe]]:
        """
        Returns list of similar ranobes for certain ranobe.

        :param ranobe_id: Ranobe ID to get similar ranobes
        :type ranobe_id: int

        :return: List of similar ranobes
        :rtype: Optional[List[Ranobe]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.similar_ranobes(ranobe_id))
        return Utils.validate_return_data(response, data_model=Ranobe)

    @method_endpoint('/api/ranobe/:id/related')
    def ranobe_related_content(self,
                               ranobe_id: int) -> Optional[List[Relation]]:
        """
        Returns list of related content of certain ranobe.

        :param ranobe_id: Ranobe ID to get related content
        :type ranobe_id: int

        :return: List of relations
        :rtype: Optional[List[Relation]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.ranobe_related_content(ranobe_id))
        return Utils.validate_return_data(response, data_model=Relation)

    @method_endpoint('/api/ranobe/:id/franchise')
    def ranobe_franchise_tree(self, ranobe_id: int) -> Optional[FranchiseTree]:
        """
        Returns franchise tree of certain ranobe.

        :param ranobe_id: Ranobe ID to get franchise tree
        :type ranobe_id: int

        :return: Franchise tree of certain ranobe
        :rtype: Optional[FranchiseTree]
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.ranobe_franchise_tree(ranobe_id))
        return Utils.validate_return_data(response, data_model=FranchiseTree)

    @method_endpoint('/api/ranobe/:id/external_links')
    def ranobe_external_links(self, ranobe_id: int) -> Optional[List[Link]]:
        """
        Returns list of external links of certain ranobe.

        :param ranobe_id: Ranobe ID to get external links
        :type ranobe_id: int

        :return: List of external links
        :rtype: Optional[List[Link]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.ranobe_external_links(ranobe_id))
        return Utils.validate_return_data(response, data_model=Link)

    @method_endpoint('/api/ranobe/:id/topics')
    def ranobe_topics(self,
                      ranobe_id: int,
                      page: Optional[int] = None,
                      limit: Optional[int] = None) -> Optional[List[Topic]]:
        """
        Returns list of topics of certain ranobe.

        If some data are not provided, using default values.

        :param ranobe_id: Ranobe ID to get topics
        :type ranobe_id: int

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of topics
        :rtype: Optional[List[Topic]]
        """
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.ranobe_topics(ranobe_id),
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit']))
        return Utils.validate_return_data(response, data_model=Topic)

    @method_endpoint('/api/stats/active_users')
    def active_users(self) -> Optional[List[int]]:
        """
        Returns list of IDs of active users.

        :return: List of IDs of active users
        :rtype: Optional[List[int]]
        """
        response: List[int] = self._request(self._endpoints.active_users)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/studios')
    def studios(self) -> Optional[List[Studio]]:
        """
        Returns list of studios.

        :return: List of studios
        :rtype: Optional[List[Studio]]
        """
        response: List[Dict[str, Any]] = self._request(self._endpoints.studios)
        return Utils.validate_return_data(response, data_model=Studio)

    @method_endpoint('/api/styles/:id')
    def style(self, style_id: int) -> Optional[Style]:
        """
        Returns info about style.

        :param style_id: Style ID to get info
        :type style_id: int

        :return: Info about style
        :rtype: Optional[Style]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.style(style_id))
        return Utils.validate_return_data(response, data_model=Style)

    @method_endpoint('/api/styles/preview')
    @protected_method()
    def preview_style(self, css: str) -> Optional[Style]:
        """
        Previews style with passed CSS code.

        :param css: CSS code to preview
        :type css: str

        :return: Info about previewed style
        :rtype: Optional[Style]
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.style_preview,
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='style', css=css),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response, data_model=Style)

    @method_endpoint('/api/styles')
    @protected_method()
    def create_style(self, css: str, name: str, owner_id: int,
                     owner_type: str) -> Optional[Style]:
        """
        Creates new style.

        :param css: CSS code for style
        :type css: str

        :param name: Style name
        :type name: str

        :param owner_id: User/Club ID for style ownership
        :type owner_id: int

        :param owner_type: Type of owner (User/Club)
        :type owner_type: str

        :return: Info about previewed style
        :rtype: Optional[Style]
        """
        if not Utils.validate_enum_params({OwnerType: owner_type}):
            return None

        response: Dict[str, Any] = self._request(
            self._endpoints.styles,
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='style',
                                          css=css,
                                          name=name,
                                          owner_id=owner_id,
                                          owner_type=owner_type),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response, data_model=Style)

    @method_endpoint('/api/styles/:id')
    @protected_method()
    def update_style(self, style_id: int, css: Optional[str],
                     name: Optional[str]) -> Optional[Style]:
        """
        Updates existing style.

        :param style_id: ID of existing style for edit
        :type style_id: int

        :param css: New CSS code for style
        :type css: Optional[str]

        :param name: New style name
        :type name: Optional[str]

        :return: Info about updated style
        :rtype: Optional[Style]
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.style(style_id),
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='style', css=css,
                                          name=name),
            request_type=RequestType.PATCH)
        return Utils.validate_return_data(response, data_model=Style)

    @method_endpoint('/api/topics')
    def topics(self,
               page: Optional[int] = None,
               limit: Optional[int] = None,
               forum: Optional[str] = None,
               linked_id: Optional[int] = None,
               linked_type: Optional[str] = None,
               topic_type: Optional[str] = None) -> Optional[List[Topic]]:
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
        :rtype: Optional[List[Topic]]
        """
        if not Utils.validate_enum_params({
                ForumType: forum,
                TopicLinkedType: linked_type,
                TopicType: topic_type
        }):
            return None

        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.topics,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            forum=forum,
                                            linked_id=linked_id,
                                            linked_type=linked_type,
                                            type=topic_type))
        return Utils.validate_return_data(response, data_model=Topic)

    @method_endpoint('/api/topics/updates')
    def updates_topics(self,
                       page: Optional[int] = None,
                       limit: Optional[int] = None) -> Optional[List[Topic]]:
        """
        Returns list of NewsTopics about database updates.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of topics
        :rtype: Optional[List[Topic]]
        """
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.updates_topics,
            query=Utils.generate_query_dict(
                page=validated_numbers['page'],
                limit=validated_numbers['limit'],
            ))
        return Utils.validate_return_data(response, data_model=Topic)

    @method_endpoint('/api/topics/hot')
    def hot_topics(self, limit: Optional[int] = None) -> Optional[List[Topic]]:
        """
        Returns list of hot topics.

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of topics
        :rtype: Optional[List[Topic]]
        """
        validated_numbers = Utils.query_numbers_validator(limit=[limit, 10])

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.hot_topics,
            query=Utils.generate_query_dict(limit=validated_numbers['limit'],))
        return Utils.validate_return_data(response, data_model=Topic)

    @method_endpoint('/api/topics/:id')
    def topic(self, topic_id: int) -> Optional[Topic]:
        """
        Returns info about topic.

        :param topic_id: ID of topic to get
        :type topic_id: int

        :return: Info about topic
        :rtype: Optional[Topic]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.topic(topic_id))
        return Utils.validate_return_data(response, data_model=Topic)

    @method_endpoint('/api/topics')
    @protected_method('topics')
    def create_topic(self,
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

        response: Dict[str, Any] = self._request(
            self._endpoints.topics,
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='topic',
                                          body=body,
                                          forum_id=forum_id,
                                          linked_id=linked_id,
                                          linked_type=linked_type,
                                          title=title,
                                          type=str(
                                              TopicType.REGULAR_TOPIC.value),
                                          user_id=user_id),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response, data_model=Topic)

    @method_endpoint('/api/topics/:id')
    @protected_method('topics')
    def update_topic(self,
                     topic_id: int,
                     body: str,
                     title: str,
                     linked_id: Optional[int] = None,
                     linked_type: Optional[str] = None) -> Optional[Topic]:
        """
        Updated topic.

        :param topic_id: ID of topic to update
        :type topic_id: int

        :param body: Body of topic
        :type body: str

        :param title: Title of topic
        :type title: str

        :param linked_id: ID of linked topic (Used together with linked_type)
        :type linked_type: Optional[int]

        :param linked_type: Type of linked topic (Used together with linked_id)
        :type linked_type: Optional[str]

        :return: Updated topic info
        :rtype: Optional[Topic]
        """
        if not Utils.validate_enum_params({TopicLinkedType: linked_type}):
            return None

        response: Dict[str, Any] = self._request(
            self._endpoints.topic(topic_id),
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='topic',
                                          body=body,
                                          linked_id=linked_id,
                                          linked_type=linked_type,
                                          title=title),
            request_type=RequestType.PATCH)
        return Utils.validate_return_data(response, data_model=Topic)

    @method_endpoint('/api/topics/:id')
    @protected_method('topics')
    def delete_topic(self, topic_id: int) -> Optional[bool]:
        """
        Deletes topic.

        :param topic_id: ID of topic to delete
        :type topic_id: int

        :return: Status of topic deletion
        :rtype: bool
        """
        response: Union[Dict[str, Any],
                        int] = self._request(self._endpoints.topic(topic_id),
                                             headers=self._authorization_header,
                                             request_type=RequestType.DELETE)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/user_images')
    @protected_method('comments')
    def create_user_image(
            self,
            image_path: str,
            linked_type: Optional[str] = None) -> Optional[CreatedUserImage]:
        """
        Creates an user image.

        :param image_path: Path or URL to image to create on server
        :type image_path: str

        :param linked_type: Type of linked image
        :type linked_type: Optional[str]

        :return: Created image info
        :rtype: Optional[CreatedUserImage]
        """
        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.user_images,
            headers=self._authorization_header,
            files=Utils.get_image_data(image_path),
            data=Utils.generate_data_dict(linked_type=linked_type),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response, data_model=CreatedUserImage)

    @method_endpoint('/api/v2/user_rates')
    def user_rates(self,
                   user_id: int,
                   target_id: Optional[int] = None,
                   target_type: Optional[str] = None,
                   status: Optional[str] = None,
                   page: Optional[int] = None,
                   limit: Optional[int] = None) -> Optional[List[UserRate]]:
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
        (This field is ignored when user_id is set)
        :rtype: Optional[List[UserRate]]
        """
        if target_id is not None and target_type is None:
            logger.warning('target_type is required when passing target_id')
            return None

        if not Utils.validate_enum_params({
                UserRateTarget: target_type,
                UserRateStatus: status
        }):
            return None

        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 1000],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_rates,
            query=Utils.generate_query_dict(user_id=user_id,
                                            target_id=target_id,
                                            target_type=target_type,
                                            status=status,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit']))
        return Utils.validate_return_data(response, data_model=UserRate)

    @method_endpoint('/api/v2/user_rates/:id')
    def user_rate(self, rate_id: int) -> Optional[UserRate]:
        """
        Returns info about user rate.

        :param rate_id: ID of rate to get
        :type rate_id: int

        :return: Info about user rate
        :rtype: Optional[UserRate]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.user_rate(rate_id))
        return Utils.validate_return_data(response, data_model=UserRate)

    @method_endpoint('/api/v2/user_rates')
    @protected_method('user_rates')
    def create_user_rate(self,
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

        response: Dict[str, Any] = self._request(
            self._endpoints.user_rates,
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='user_rate',
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
        return Utils.validate_return_data(response, data_model=UserRate)

    @method_endpoint('/api/v2/user_rates/:id')
    @protected_method('user_rates')
    def update_user_rate(self,
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

        response: Dict[str, Any] = self._request(
            self._endpoints.user_rate(rate_id),
            headers=self._authorization_header,
            data=Utils.generate_data_dict(dict_name='user_rate',
                                          status=status,
                                          score=validated_numbers['score'],
                                          chapters=chapters,
                                          episodes=episodes,
                                          volumes=volumes,
                                          rewatches=rewatches,
                                          text=text),
            request_type=RequestType.PATCH)
        return Utils.validate_return_data(response, data_model=UserRate)

    @method_endpoint('/api/v2/user_rates/:id/increment')
    @protected_method('user_rates')
    def increment_user_rate(self, rate_id: int) -> Optional[UserRate]:
        """
        Increments user rate episode/chapters and return updated info.

        :param rate_id: ID of user rate to increment episode/chapters
        :type rate_id: int

        :return: Info about updated user rate
        :rtype: Optional[UserRate]
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.user_rate_increment(rate_id),
            headers=self._authorization_header,
            request_type=RequestType.POST)
        return Utils.validate_return_data(response, data_model=UserRate)

    @method_endpoint('/api/v2/user_rates/:id')
    @protected_method('user_rates')
    def delete_user_rate(self, rate_id: int) -> bool:
        """
        Deletes user rate.

        :param rate_id: ID of user rate to delete
        :type rate_id: int

        :return: Status of user rate deletion
        :rtype: bool
        """
        response: Union[Dict[str, Any],
                        int] = self._request(self._endpoints.user_rate(rate_id),
                                             headers=self._authorization_header,
                                             request_type=RequestType.DELETE)
        return Utils.validate_return_data(response,
                                          response_code=ResponseCode.NO_CONTENT)

    @method_endpoint('/api/users_rates/:type/cleanup')
    @protected_method('user_rates')
    def delete_entire_user_rates(self, user_rate_type: str) -> bool:
        """
        Deletes all user rates.

        :param user_rate_type: Type of user rates to delete
        :type user_rate_type: str

        :return: Status of user rates deletion
        :rtype: bool
        """
        if not Utils.validate_enum_params({UserRateType: user_rate_type}):
            return False

        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.user_rates_cleanup(user_rate_type),
            headers=self._authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/user_rates/:type/reset')
    @protected_method('user_rates')
    def reset_all_user_rates(self, user_rate_type: str) -> bool:
        """
        Resets all user rates.

        :param user_rate_type: Type of user rates to reset
        :type user_rate_type: UserRateType

        :return: Status of user rates reset
        :rtype: bool
        """
        if not Utils.validate_enum_params({UserRateType: user_rate_type}):
            return False

        response: Union[Dict[str, Any], int] = self._request(
            self._endpoints.user_rates_reset(user_rate_type),
            headers=self._authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/users')
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
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 100],
        )

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.users,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit']))
        return Utils.validate_return_data(response, data_model=User)

    @method_endpoint('/api/users/:id')
    def user(self,
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
        response: Dict[str, Any] = self._request(
            self._endpoints.user(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=User)

    @method_endpoint('/api/users/:id/info')
    def user_info(self,
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
        response: Dict[str, Any] = self._request(
            self._endpoints.user_info(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=User)

    @method_endpoint('/api/users/whoami')
    @protected_method()
    def current_user(self) -> Optional[User]:
        """
        Returns brief info about current user.

        Current user evaluated depending on authorization code.

        :return: Current user brief info
        :rtype: Optional[User]
        """
        response: Dict[str,
                       Any] = self._request(self._endpoints.whoami,
                                            headers=self._authorization_header)
        return Utils.validate_return_data(response, data_model=User)

    @method_endpoint('/api/users/sign_out')
    @protected_method()
    def user_sign_out(self):
        """Sends sign out request to API."""
        self._request(self._endpoints.sign_out,
                      headers=self._authorization_header)

    @method_endpoint('/api/users/:id/friends')
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

        :return: List of user's friends
        :rtype: Optional[List[User]]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_friends(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=User)

    @method_endpoint('/api/users/:id/clubs')
    def user_clubs(self,
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
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_clubs(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=Club)

    @method_endpoint('/api/users/:id/anime_rates')
    def user_anime_rates(
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

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_anime_rates(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            status=status,
                                            censored=censored))
        return Utils.validate_return_data(response, data_model=UserList)

    @method_endpoint('/api/users/:id/manga_rates')
    def user_manga_rates(
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

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_manga_rates(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            censored=censored))
        return Utils.validate_return_data(response, data_model=UserList)

    @method_endpoint('/api/users/:id/favourites')
    def user_favourites(
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
        response: Dict[str, Any] = self._request(
            self._endpoints.user_favourites(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=Favourites)

    @method_endpoint('/api/users/:id/messages')
    @protected_method('messages')
    def current_user_messages(
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

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_messages(user_id),
            headers=self._authorization_header,
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            type=message_type))
        return Utils.validate_return_data(response, data_model=Message)

    @method_endpoint('/api/users/:id/unread_messages')
    @protected_method('messages')
    def current_user_unread_messages(
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
        response: Dict[str, Any] = self._request(
            self._endpoints.user_unread_messages(user_id),
            headers=self._authorization_header,
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=UnreadMessages)

    @method_endpoint('/api/users/:id/history')
    def user_history(
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

        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_history(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname,
                                            page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            target_id=target_id,
                                            target_type=target_type))
        return Utils.validate_return_data(response, data_model=History)

    @method_endpoint('/api/users/:id/bans')
    def user_bans(self,
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
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_bans(user_id),
            query=Utils.generate_query_dict(is_nickname=is_nickname))
        return Utils.validate_return_data(response, data_model=Ban)

    @method_endpoint('/api/v2/topics/:topic_id/ignore')
    @protected_method('topics')
    def ignore_topic(self, topic_id: int) -> bool:
        """
        Set topic as ignored.

        :param topic_id: ID of topic to ignore
        :type topic_id: int

        :return: True if topic was ignored, False otherwise
        :rtype: bool
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.topic_ignore(topic_id),
            headers=self._authorization_header,
            request_type=RequestType.POST)
        return Utils.validate_return_data(response) is True

    @method_endpoint('/api/v2/topics/:topic_id/ignore')
    @protected_method('topics')
    def unignore_topic(self, topic_id: int) -> bool:
        """
        Set topic as unignored.

        :param topic_id: ID of topic to unignore
        :type topic_id: int

        :return: True if topic was unignored, False otherwise
        :rtype: bool
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.topic_ignore(topic_id),
            headers=self._authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_return_data(response) is False

    @method_endpoint('/api/v2/users/:user_id/ignore')
    @protected_method('ignores')
    def ignore_user(self, user_id: int) -> bool:
        """
        Set user as ignored.

        :param user_id: ID of topic to ignore
        :type user_id: int

        :return: True if user was ignored, False otherwise
        :rtype: bool
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_ignore(user_id),
            headers=self._authorization_header,
            request_type=RequestType.POST)
        return Utils.validate_return_data(response) is True

    @method_endpoint('/api/v2/users/:user_id/ignore')
    @protected_method('ignores')
    def unignore_user(self, user_id: int) -> bool:
        """
        Set user as unignored.

        :param user_id: ID of user to unignore
        :type user_id: int

        :return: True if user was unignored, False otherwise
        :rtype: bool
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.user_ignore(user_id),
            headers=self._authorization_header,
            request_type=RequestType.DELETE)
        return Utils.validate_return_data(response) is False

    @method_endpoint('/api/v2/abuse_requests/offtopic')
    def mark_comment_offtopic(self, comment_id: int) -> Optional[AbuseResponse]:
        """
        Mark comment as offtopic.

        :param comment_id: ID of comment to mark as offtopic
        :type comment_id: int

        :return: Object with info about abuse request
        :rtype: Optional[AbuseResponse]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.abuse_offtopic,
            data=Utils.generate_data_dict(comment_id=comment_id),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response, data_model=AbuseResponse)

    @method_endpoint('/api/v2/abuse_requests/review')
    def convert_comment_review(self,
                               comment_id: int) -> Optional[AbuseResponse]:
        """
        Convert comment to review.

        :param comment_id: ID of comment to convert to review
        :type comment_id: int

        :return: Object with info about abuse request
        :rtype: Optional[AbuseResponse]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.abuse_review,
            data=Utils.generate_data_dict(comment_id=comment_id),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response, data_model=AbuseResponse)

    @method_endpoint('/api/v2/abuse_requests/abuse')
    def create_violation_abuse_request(self, comment_id: int,
                                       reason: str) -> Optional[AbuseResponse]:
        """
        Create abuse about violation of site rules

        :param comment_id: ID of comment to create abuse request
        :type comment_id: int

        :param reason: Additional info about violation
        :type reason: str

        :return: Object with info about abuse request
        :rtype: Optional[AbuseResponse]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.abuse_violation,
            data=Utils.generate_data_dict(comment_id=comment_id, reason=reason),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response, data_model=AbuseResponse)

    @method_endpoint('/api/v2/abuse_requests/spoiler')
    def create_spoiler_abuse_request(self, comment_id: int,
                                     reason: str) -> Optional[AbuseResponse]:
        """
        Create abuse about spoiler in content.

        :param comment_id: ID of comment to create abuse request
        :type comment_id: int

        :param reason: Additional info about spoiler
        :type reason: str

        :return: Object with info about abuse request
        :rtype: Optional[AbuseResponse]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.abuse_spoiler,
            data=Utils.generate_data_dict(comment_id=comment_id, reason=reason),
            request_type=RequestType.POST)
        return Utils.validate_return_data(response, data_model=AbuseResponse)
