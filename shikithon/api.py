""" Shikithon API Module.

This is main module with a class
for interacting with the Shikimori API.
"""
from json import dumps
from time import time
from time import sleep
from typing import Any
from typing import Dict
from typing import List
from typing import Union
from typing import Tuple

from requests import Session
from requests import Response
from ratelimit import limits
from ratelimit import sleep_and_retry

from shikithon.enums.anime import Order
from shikithon.enums.anime import Kind
from shikithon.enums.anime import Status
from shikithon.enums.anime import Duration
from shikithon.enums.anime import Rating
from shikithon.enums.anime import Censorship
from shikithon.enums.anime import MyList
from shikithon.enums.request import RequestType
from shikithon.enums.response import ResponseCode

from shikithon.models.achievement import Achievement
from shikithon.models.anime import Anime
from shikithon.models.ban import Ban
from shikithon.models.calendar_event import CalendarEvent
from shikithon.models.creator import Creator
from shikithon.models.franchise_tree import FranchiseTree
from shikithon.models.link import Link
from shikithon.models.relation import Relation
from shikithon.models.screenshot import Screenshot
from shikithon.models.topic import Topic
from shikithon.models.user import User

from shikithon.config_cache import ConfigCache

from shikithon.decorators import protected_method

from shikithon.endpoints import Endpoints

from shikithon.exceptions import MissingConfigData
from shikithon.exceptions import MissingAppName
from shikithon.exceptions import MissingClientID
from shikithon.exceptions import MissingClientSecret
from shikithon.exceptions import MissingAppScopes
from shikithon.exceptions import MissingAuthCode
from shikithon.exceptions import AccessTokenException

SHIKIMORI_API_URL = "https://shikimori.one/api"
SHIKIMORI_API_URL_V2 = "https://shikimori.one/api/v2"
SHIKIMORI_OAUTH_URL = "https://shikimori.one/oauth"
DEFAULT_REDIRECT_URI = "urn:ietf:wg:oauth:2.0:oob"
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

        :param Dict[str, str] config: Config file for API class
        """
        self._endpoints: Endpoints = Endpoints(
            SHIKIMORI_API_URL, SHIKIMORI_API_URL_V2, SHIKIMORI_OAUTH_URL
        )
        self._session: Session = Session()

        self._app_name: str = ""
        self._client_id: str = ""
        self._client_secret: str = ""
        self._redirect_uri: str = ""
        self._scopes: str = ""
        self._auth_code: str = ""
        self._access_token: str = ""
        self._refresh_token: str = ""
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
            "app_name": self._app_name,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
            "redirect_uri": self._redirect_uri,
            "scopes": self._scopes,
            "auth_code": self._auth_code,
            "access_token": self._access_token,
            "refresh_token": self._refresh_token,
            "token_expire": str(self._token_expire)
        }

    @config.setter
    def config(self, config: Dict[str, str]):
        """
        Sets new API variables from config dictionary.

        This method calls init_config
        to reconfigure the object

        :param Dict[str, str] config: Config dictionary
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
        return {
            "User-Agent": self._session.headers["User-Agent"]
        }

    @_user_agent.setter
    def _user_agent(self, app_name: str):
        """
        Update session headers and set user agent.

        :param str app_name: OAuth App name
        """
        self._session.headers.update(
            {"User-Agent": app_name}
        )

    @property
    def _authorization_header(self) -> Dict[str, str]:
        """
        Returns user agent and authorization token headers dictionary.

        Needed for accessing Shikimori protected resources

        :return: Dictionary with proper user agent and autorization token
        :rtype: Dict[str, str]
        """
        header = self._user_agent
        header["Authorization"] = f"Bearer {self._access_token}"
        return header

    def _init_config(self, config: Dict[str, str]):
        """
        Special method for initializing an object.

        This method calls several methods:

        - Validation of config and variables
        - Customizing the session header user agent
        - Getting access/refresh tokens if they are missing

        :param Dict[str, str] config: Config dictionary
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

        :param Dict[str, str] config: Config dictionary for validation
        :raises: MissingConfigData
        """
        try:
            config_cached = False
            if ConfigCache.config_exists(config["app_name"]):
                config = ConfigCache.get_config(config["app_name"])
                config_cached = True

            self._app_name: str = config["app_name"]
            self._client_id: str = config["client_id"]
            self._client_secret: str = config["client_secret"]
            self._redirect_uri: str = config["redirect_uri"]
            self._scopes: str = config["scopes"]
            self._auth_code: str = config["auth_code"]
            if config_cached:
                self._access_token = config["access_token"]
                self._refresh_token = config["refresh_token"]
                self._token_expire = int(config["token_expire"])
        except KeyError as err:
            raise MissingConfigData(
                "It is impossible to initialize an API object"
                "without missing variables. "
                "Recheck your config and try again."
            ) from err

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

        :raises: MissingAppName, MissingClientID,
        MissingClientSecret, MissingAppScopes, MissingAuthCode
        """
        exception_msg: str = "To use the Shikimori API correctly, " \
                             "you need to pass the application "

        if not self._app_name:
            raise MissingAppName(
                exception_msg + "name"
            )

        if not self._client_id:
            raise MissingClientID(
                exception_msg + "Client ID"
            )

        if not self._client_secret:
            raise MissingClientSecret(
                exception_msg + "Client Secret"
            )

        if not self._redirect_uri:
            self._redirect_uri = DEFAULT_REDIRECT_URI

        if not self._scopes:
            raise MissingAppScopes(
                exception_msg + "scopes"
            )

        if not self._auth_code:
            auth_link: str = self._endpoints.authorization_link(
                self._client_id, self._redirect_uri, self._scopes
            )
            raise MissingAuthCode(
                exception_msg + "authorization code. To get one, go to "
                                f"{auth_link}"
            )

    def _get_access_token(self, refresh_token: bool = False) -> Tuple[str, str]:
        """
        Returns access/refresh tokens from API request.

        If refresh_token flag is set to True,
        returns refreshed access/refresh tokens.

        :param bool refresh_token: Flag for refreshing token
        instead of getting new ones
        :return: New access/refresh tokens tuple
        :rtype: Tuple[str, str]
        :raises: AccessTokenException
        """
        data: Dict[str, str] = {
            "client_id": self._client_id,
            "client_secret": self._client_secret
        }

        if refresh_token:
            data["grant_type"] = "refresh_token"
            data["refresh_token"] = self._refresh_token
        else:
            data["grant_type"] = "authorization_code"
            data["code"] = self._auth_code
            data["redirect_uri"] = self._redirect_uri

        oauth_json = self._request(
            self._endpoints.oauth_token,
            data=data,
            request_type=RequestType.POST
        )

        try:
            return oauth_json["access_token"], oauth_json["refresh_token"]
        except KeyError as err:
            error_info = dumps(oauth_json)
            raise AccessTokenException(
                "An error occurred while receiving tokens, "
                f"here is the information from the response: {error_info}"
            ) from err

    def _update_tokens(self, tokens_data: Tuple[str, str]):
        """
        Set new tokens and update token expire time.

        **Note:** This method also updates cache config file for
        future use

        :param Tuple[str, str] tokens_data: Tuple with access and refresh tokens
        """
        self._tokens = tokens_data
        self._cache_config()

    def _cache_config(self):
        """Updates token expire time and caches new config."""
        self._token_expire = int(time()) + TOKEN_EXPIRE_TIME
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
    ) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:
        """
        Create request and return response JSON.

        This method uses ratelimit library for rate limiting
        requests (Shikimori API limit: 90rpm)

        For 5rps limit, there is a check for 429 status code.
        When triggered, halt request for 0.5 second and retry

        **Note:** To address duplication of methods
        for different request methods, this method
        uses RequestType enum

        :param str url: URL for making request
        :param Union[None, Dict[str, str]] data: Request body data
        :param Union[None, Dict[str, str]] headers: Custom headers for request
        :param Union[None, Dict[str, str]] query: Query data for request
        :param RequestType request_type: Type of current request
        :return: Response JSON or None, if request fails
        :rtype: Union[List[Dict[str, Any]], Dict[str, Any], None]
        """
        response: Union[Response, None] = None

        if request_type == RequestType.GET:
            response = self._session.get(
                url, headers=headers, params=query, data=data
            )
        if request_type == RequestType.POST:
            response = self._session.post(
                url, headers=headers, params=query, data=data
            )
        if request_type == RequestType.PUT:
            response = self._session.put(
                url, headers=headers, params=query, data=data
            )
        if request_type == RequestType.PATCH:
            response = self._session.patch(
                url, headers=headers, params=query, data=data
            )
        if request_type == RequestType.DELETE:
            response = self._session.delete(
                url, headers=headers, params=query, data=data
            )

        if response.status_code == ResponseCode.RETRY_LATER.value:
            sleep(RATE_LIMIT_RPS_COOLDOWN)
            return self._request(
                url,
                data,
                headers,
                query,
                request_type
            )

        return response.json()

    def refresh_tokens(self):
        """
        Manages tokens refreshing and caching.

        This method gets new access/refresh tokens and
        updates them in current instance, as well as
        caching new config.
        """
        tokens_data: Tuple[str, str] = self._get_access_token(
            refresh_token=True
        )
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
        :return: List of achievements
        :rtype: List[Achievement]
        """
        query: Dict[str, str] = {
            "user_id": str(user_id)
        }
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.achievements,
            query=query
        )
        return [Achievement(**achievement) for achievement in response]

    def animes(
            self,
            page: int = 1,
            limit: int = 1,
            order: Order = Order.NONE,
            kind: Kind = Kind.NONE,
            status: Status = Status.NONE,
            season: str = "",
            score: int = 1,
            duration: Duration = Duration.NONE,
            rating: Rating = Rating.NONE,
            genre: Union[None, List[int]] = None,
            studio: Union[None, List[int]] = None,
            franchise: Union[None, List[int]] = None,
            censored: Censorship = Censorship.CENSORED,
            my_list: MyList = MyList.NONE,
            ids: Union[None, List[int]] = None,
            exclude_ids: Union[None, List[int]] = None,
            search: str = ""
    ) -> List[Anime]:
        """
        Returns animes list.

        If some data are not provided, using default values

        :param int page: Number of page
        :param int limit: Number of results limit
        :param Order order: Type of order in list
        :param Kind kind: Type of anime topic
        :param Status status: Type of anime status
        :param str season: Name of anime season
        :param int score: Minimal anime score
        :param Duration duration: Duration size of anime
        :param Rating rating: Type of anime rating
        :param Union[List[int], None] genre: Genres ID
        :param Union[List[int], None] studio: Studios ID
        :param Union[List[int], None] franchise: Franchises ID
        :param Censorship censored: Type of anime censorship
        :param MyList my_list: Status of anime in current user list
        :param Union[List[int], None] ids: Animes ID to include
        :param Union[List[int], None] exclude_ids: Animes ID to exclude
        :param str search: Search phrase to filter animes by name.

        :returns: Animes list
        :rtype: List[Anime]
        """
        if page < 1 or page > 10000:
            page = 1

        if limit < 1 or limit > 50:
            limit = 1

        if score < 1 or score > 9:
            score = 1

        if genre is None:
            genre = []
        if studio is None:
            studio = []
        if franchise is None:
            franchise = []
        if ids is None:
            ids = []
        if exclude_ids is None:
            exclude_ids = []

        query: Dict[str, str] = {
            "page": str(page),
            "limit": str(limit),
            "order": order.value,
            "kind": kind.value,
            "status": status.value,
            "season": season,
            "score": str(score),
            "duration": duration.value,
            "rating": rating.value,
            "genre": ",".join(
                [str(genre_id) for genre_id in genre]
            ),
            "studio": ",".join(
                [str(studio_id) for studio_id in studio]
            ),
            "franchise": ",".join(
                [str(franchise_id) for franchise_id in franchise]
            ),
            "censored": censored.value,
            "mylist": my_list.value,
            "ids": ",".join(
                [str(anime_id) for anime_id in ids]
            ),
            "exclude_ids": ",".join(
                [str(anime_id) for anime_id in exclude_ids]
            ),
            "search": search
        }
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.animes,
            query=query
        )
        return [Anime(**anime) for anime in response]

    def anime(self, anime_id: int) -> Anime:
        """
        Returns info about certain anime.

        :param int anime_id: Anime ID to get
        :return: Anime info
        :rtype: Anime
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.anime(anime_id)
        )
        return Anime(**response)

    def anime_creators(self, anime_id: int) -> List[Creator]:
        """
        Returns creators info of certain anime.

        :param anime_id: Anime ID to get creators
        :return: List of anime creators
        :rtype: List[Creator]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_roles(anime_id)
        )
        return [Creator(**creator) for creator in response]

    def similar_animes(self, anime_id: int) -> List[Anime]:
        """
        Returns list of similar animes for certain anime.

        :param int anime_id: Anime ID to get similar animes
        :return: List of similar animes
        :rtype: List[Anime]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.similar_animes(anime_id)
        )
        return [Anime(**anime) for anime in response]

    def anime_related_content(self, anime_id: int) -> List[Relation]:
        """
        Returns list of related content of certain anime.

        :param int anime_id: Anime ID to get related content
        :return: List of relations
        :rtype: List[Relation]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_related_content(anime_id)
        )
        return [Relation(**relation) for relation in response]

    def anime_screenshots(self, anime_id: int) -> List[Screenshot]:
        """
        Returns list of screenshot links of certain anime.

        :param int anime_id: Anime ID to get screenshot links
        :return: List of screenshot links
        :rtype: List[Screenshot]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_screenshots(anime_id)
        )
        return [Screenshot(**screenshot) for screenshot in response]

    def anime_franchise_tree(self, anime_id: int) -> FranchiseTree:
        """
        Returns franchise tree of certain anime.

        :param int anime_id: Anime ID to get franchise tree
        :return: Franchise tree of certain anime
        :rtype: FranchiseTree
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.anime_franchise_tree(anime_id)
        )
        return FranchiseTree(**response)

    def anime_external_links(self, anime_id: int) -> List[Link]:
        """
        Returns list of external links of certain anime.

        :param int anime_id: Anime ID to get external links
        :return: List of external links
        :rtype: List[Link]
        """
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_external_links(anime_id)
        )
        return [Link(**link) for link in response]

    def anime_topics(
            self,
            anime_id: int,
            page: int = 1,
            limit: int = 1,
            kind: Status = Status.EPISODE,
            episode: int = 1
    ) -> List[Topic]:
        """
        Returns list of topics of certain anime.

        If some data are not provided, using default values.

        :param int anime_id: Anime ID to get topics
        :param int page: Number of page
        :param int limit: Number of results limit
        :param Status kind: Status of anime
        :param int episode: Number of anime episode
        :return: List of topics
        :rtype: List[Topic]
        """
        if page < 1 or page > 100000:
            page = 1

        if limit < 1 or limit > 30:
            limit = 1

        query: Dict[str, str] = {
            "page": str(page),
            "limit": str(limit),
            "kind": kind.value,
            "episode": str(episode)
        }
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.anime_topics(anime_id),
            query=query
        )
        return [Topic(**topic) for topic in response]

    def bans(self, page: int = 1, limit: int = 1) -> List[Ban]:
        """
        Returns list of recent bans on Shikimori.

        Current API method returns `limit + 1` elements,
        if API has next page.

        :param int page: Number of page
        :param int limit: Number of results
        :return: List of recent bans
        :rtype: List[Ban]
        """
        if page < 1 or page > 100000:
            page = 1

        if limit < 1 or limit > 30:
            limit = 1

        query: Dict[str, str] = {
            "page": str(page),
            "limit": str(limit)
        }
        response: List[Dict[str, Any]] = self._request(
            self._endpoints.bans_list,
            query=query
        )
        return [Ban(**ban) for ban in response]

    def calendar(
            self,
            censored: Censorship = Censorship.CENSORED
    ) -> List[CalendarEvent]:
        """
        Returns current calendar events.

        :param Censorship censored: Status of censorship for events
        :return: List of calendar events
        :rtype: List[CalendarEvent]
        """
        query: Dict[str, str] = {
            "censored": censored.value
        }
        res: List[Dict[str, Any]] = self._request(
            self._endpoints.calendar,
            query=query
        )
        return [CalendarEvent(**calendar_event) for calendar_event in res]

    @protected_method
    def current_user(self) -> User:
        """
        Returns brief info about current user.

        Current user evaluated depending on authorization code.

        :return: User object
        :rtype: User
        """
        response: Dict[str, Any] = self._request(
            self._endpoints.whoami,
            headers=self._authorization_header
        )
        return User(**response)
