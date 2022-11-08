"""Base class for shikithon API class."""
from __future__ import annotations

import asyncio
from json import dumps
import sys
from time import time
from typing import Any, Callable, Dict, List, Optional, Tuple, TypeVar, Union

from aiohttp import ClientSession
from aiohttp import ContentTypeError
from loguru import logger
from ratelimit import limits
from ratelimit import sleep_and_retry

from .endpoints import Endpoints
from .enums import RequestType
from .exceptions import AccessTokenException
from .exceptions import MissingAppVariable
from .exceptions import MissingAuthCode
from .exceptions import MissingConfigData
from .store import ConfigStore
from .utils import Utils

ONE_MINUTE = 60
MAX_CALLS_PER_MINUTE = 90
ONE_SECOND = 1
MAX_CALLS_PER_SECOND = 5

SHIKIMORI_API_URL = 'https://shikimori.one/api'
SHIKIMORI_API_URL_V2 = 'https://shikimori.one/api/v2'
SHIKIMORI_OAUTH_URL = 'https://shikimori.one/oauth'
DEFAULT_REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

RT = TypeVar('RT')
TOKEN_EXPIRE_TIME = 86400


class Client:
    """Base client class for shikithon API class.

    Contains logic and methods for making requests to the shikimori API
    as well as validating config and etc.

    **Note:** Due to problems with some methods,
    when the session header contains a User-Agent and authorization,
    __init__ sets only the User-Agent,
    and all protected methods independently
    provide a header with a token
    """

    def __init__(self, config: Union[str, Dict[str, str]]) -> None:
        self.endpoints = Endpoints(SHIKIMORI_API_URL, SHIKIMORI_API_URL_V2,
                                   SHIKIMORI_OAUTH_URL)
        self._session = None
        self._passed_config = config

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

    @property
    def restricted_mode(self) -> bool:
        """
        Returns current restrict mode of client object.

        If true, client object can access only public methods

        :return: Current restrict mode
        :rtype: bool
        """
        return self._restricted_mode

    @restricted_mode.setter
    def restricted_mode(self, restricted_mode: bool):
        """
        Sets new restrict mode of client object.

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
        Returns current client variables as config dictionary.

        :return: Current client variables as config dictionary
        :rtype: Dict[str, str]
        """
        logger.debug('Exporting current client config')
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
        Sets new client variables from config dictionary.

        This method calls init_config
        to reconfigure the object

        :param config: Config dictionary
        :type config: Dict[str, str]
        """
        logger.info('Setting new client config')
        self.init_config(config)

    @property
    def tokens(self) -> Tuple[str, str]:
        """
        Returns access/refresh tokens as tuple.

        :return: Access and refresh tokens tuple
        :rtype: Tuple[str, str]
        """
        return self._access_token, self._refresh_token

    @tokens.setter
    def tokens(self, tokens_data: Tuple[str, str]):
        """
        Sets new access/refresh tokens from tuple.

        :param tokens_data: New access and refresh tokens tuple
        :type tokens_data: Tuple[str, str]
        """
        self._access_token = tokens_data[0]
        self._refresh_token = tokens_data[1]

    @property
    def user_agent(self) -> Dict[str, str]:
        """
        Returns current session User-Agent.

        :return: Session User-Agent
        :rtype: Dict[str, str]
        """
        return {'User-Agent': self._session.headers['User-Agent']}

    @user_agent.setter
    def user_agent(self, app_name: str):
        """
        Update session headers and set user agent.

        :param app_name: OAuth App name
        :type app_name: str
        """
        if self._session is not None:
            self._session.headers.update({'User-Agent': app_name})

    @property
    def authorization_header(self) -> Dict[str, str]:
        """
        Returns user agent and authorization token headers dictionary.

        Needed for accessing Shikimori protected resources

        :return: Dictionary with proper user agent and autorization token
        :rtype: Dict[str, str]
        """
        header = self.user_agent
        header['Authorization'] = f'Bearer {self._access_token}'
        return header

    @logger.catch(onerror=lambda _: sys.exit(1))
    async def init_config(self, config: Union[str, Dict[str, str]]):
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
        logger.debug('Initializing client config')
        self.validate_config(config)
        self.validate_vars()
        logger.debug('Setting User-Agent with current app name')
        self.user_agent = self._app_name

        if self._restricted_mode:
            return

        if isinstance(config, dict) and not self._access_token:
            logger.debug('No tokens found')
            tokens_data = await self.get_access_token()
            self.update_tokens(tokens_data)

        if self.token_expired():
            logger.debug('Token has expired. Refreshing...')
            await self.refresh_tokens()

    @logger.catch(onerror=lambda _: sys.exit(1))
    def validate_config(self, config: Union[str, Dict[str, str]]):
        """
        Validates passed config dictionary and sets
        client variables.

        If config is string, sets only app name and change value
        of restrict mode of API object.

        Also, if config is dictionary and method detects
        a stored configuration file, it replaces passed configuration
        dictionary with the stored one.

        Raises MissingConfigData if some variables
        are missing in config dictionary

        :param config: Config dictionary or app name for validation
        :type config: Union[str, Dict[str, str]]

        :raises MissingConfigData: If any field is missing
            (Not raises if there is a stored config)
        """
        logger.debug('Validating client config')
        if isinstance(config, str):
            logger.debug('Detected app_name only. Activating restricted mode')
            self._app_name = config
            self.restricted_mode = True
            return

        try:
            logger.debug('Checking for stored config')
            stored_config, is_config_stored = ConfigStore.config_validation(
                config['app_name'], config['auth_code'])

            if is_config_stored:
                logger.debug('Replacing passed config with stored one')
                config = stored_config

                logger.debug('Extracting access tokens from config')
                self._access_token = stored_config['access_token']
                self._refresh_token = stored_config['refresh_token']
                self._token_expire = int(stored_config['token_expire'])

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
    def validate_vars(self):
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

        auth_link = self.endpoints.authorization_link(self._client_id,
                                                      self._redirect_uri,
                                                      self._scopes)
        raise MissingAuthCode(auth_link)

    @logger.catch(onerror=lambda _: sys.exit(1))
    async def get_access_token(self,
                               refresh_token: bool = False) -> Tuple[str, str]:
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

        oauth_json: Dict[str, Any] = await self.request(
            self.endpoints.oauth_token,
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
    def update_tokens(self, tokens_data: Tuple[str, str]):
        """
        Set new tokens and update token expire time.

        **Note:** This method also updates cache config file for
        future use

        :param tokens_data: Tuple with access and refresh tokens
        :type tokens_data: Tuple[str, str]
        """
        logger.debug('Updating current tokens')
        self.tokens = tokens_data
        self.store_config()

    @logger.catch(onerror=lambda _: sys.exit(1))
    async def refresh_tokens(self):
        """
        Manages tokens refreshing and caching.

        This method gets new access/refresh tokens and
        updates them in current instance, as well as
        caching new config.
        """
        tokens_data = await self.get_access_token(refresh_token=True)
        self.update_tokens(tokens_data)

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
    def store_config(self):
        """Updates token expire time and stores new config."""
        self._token_expire = Utils.get_new_expire_time(TOKEN_EXPIRE_TIME)
        ConfigStore.save_config(self.config)
        logger.debug('Expiration time and stored config file have been updated')

    @logger.catch
    def protected_method_headers(
            self, endpoint_name: str) -> Optional[Dict[str, str]]:
        """
        This method utilizes protected method decoration logic
        for such methods, which uses access tokens in some situations.

        Example: Calling animes.get_all(my_list=...),
        mangas.get_all(my_list=...) and ranobes.get_all(my_list=...)
        requires access token.

        :param endpoint_name: Name of API endpoint for calling as protected
        :type endpoint_name: str

        :return: Authorization header with correct tokens or None
        :rtype: Optional[Dict[str, str]]
        """
        logger.debug(f'Checking the possibility of using "{endpoint_name}" '
                     f'as protected method')

        if self.restricted_mode:
            logger.debug(f'It is not possible to use "{endpoint_name}" '
                         'as the protected method '
                         'due to the restricted mode')
            return None

        if self.token_expired():
            logger.debug('Token has expired. Refreshing...')
            self.refresh_tokens()

        logger.debug('All checks for use of the protected '
                     'method have been passed')
        return self.authorization_header

    @property
    def closed(self) -> bool:
        """Check if session is closed."""
        return self._session is None

    async def open(self) -> Client:
        """Open session and return self."""
        if self.closed:
            self._session = ClientSession()
            await self.init_config(self._passed_config)
        return self

    async def close(self) -> None:
        """Close session."""
        if not self.closed:
            await self._session.close()
            self._session = None

    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_SECOND, period=ONE_SECOND)
    @limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
    async def request(
        self,
        url: str,
        data: Optional[Dict[str, str]] = None,
        bytes_data: Optional[bytes] = None,
        headers: Optional[Dict[str, str]] = None,
        query: Optional[Dict[str, str]] = None,
        request_type: RequestType = RequestType.GET,
        output_logging: bool = True,
    ) -> Optional[Union[List[Dict[str, Any]], Dict[str, Any], str]]:
        """
        Create request and return response JSON.

        This method uses ratelimit library for rate limiting
        requests (Shikimori API limit: 90rpm and 5rps)

        **Note:** To address duplication of methods
        for different request methods, this method
        uses RequestType enum

        :param url: URL for making request
        :type url: str

        :param data: Request body data
        :type data: Optional[Dict[str, str]]

        :param bytes_data: Request body data in bytes
        :type bytes_data: Optional[bytes]

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
        if self.closed:
            return

        logger.info(f'{request_type.value} {url}')
        if output_logging:
            logger.debug(f'Request info details: {data=}, {headers=}, {query=}')

        if data is not None and bytes_data is not None:
            logger.debug(
                'Request body data and bytes data are sent at the same time. '
                'Splitting into one...')
            bytes_data = {**bytes_data, **data}
            data = None

        if request_type == RequestType.GET:
            response = await self._session.get(url,
                                               headers=headers,
                                               params=query)
        elif request_type == RequestType.POST:
            response = await self._session.post(url,
                                                data=bytes_data,
                                                json=data,
                                                headers=headers,
                                                params=query)
        elif request_type == RequestType.PUT:
            response = await self._session.put(url,
                                               data=bytes_data,
                                               json=data,
                                               headers=headers,
                                               params=query)
        elif request_type == RequestType.PATCH:
            response = await self._session.patch(url,
                                                 data=bytes_data,
                                                 json=data,
                                                 headers=headers,
                                                 params=query)
        elif request_type == RequestType.DELETE:
            response = await self._session.delete(url,
                                                  data=bytes_data,
                                                  json=data,
                                                  headers=headers,
                                                  params=query)
        else:
            logger.debug('Unknown request_type. Returning None')
            return None

        logger.debug('Extracting JSON from response')
        try:
            json_response = await response.json()
        except ContentTypeError:
            logger.debug('Response is not JSON. Returning status code/text')
            return await Utils.extract_empty_response_data(response)

        if output_logging:
            logger.debug(
                'Successful extraction. '
                f'Here are the details of the response: {json_response}')
            if json_response is None and response.status == 200:
                logger.debug('Response is empty. Returning status code/text')
                return await Utils.extract_empty_response_data(response)

        return json_response

    async def multiple_requests(self, requests: List[Callable[..., RT]]):
        """
        Make multiple requests to API at the same time.

        :param requests: List of requests
        :type requests: List[Callable[..., RT]]

        :return: List of responses
        :rtype: List[Union[BaseException, RT]]
        """
        if self.closed:
            return []

        logger.info(f'Gathering {len(requests)} requests')
        return await asyncio.gather(*requests, return_exceptions=True)

    async def __aenter__(self) -> Client:
        """Async context manager entry point."""
        return await self.open()

    async def __aexit__(self, *args) -> None:
        """Async context manager exit point."""
        await self.close()
