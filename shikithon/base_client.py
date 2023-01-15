"""Base class for shikithon API class."""
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from time import time
from typing import Any, Callable, cast, Dict, List, Optional, TypeVar, Union

from aiohttp import ClientSession
from aiohttp import ContentTypeError
import backoff
from loguru import logger
from pyrate_limiter import Duration
from pyrate_limiter import Limiter
from pyrate_limiter import RequestRate

from .endpoints import Endpoints
from .enums import RequestType
from .enums import ResponseCode
from .exceptions import MissingAppVariableException
from .exceptions import RetryLaterException
from .store import NullStore
from .store import Store
from .utils import Utils

MAX_CALLS_PER_SECOND = 5
MAX_CALLS_PER_MINUTE = 90

SHIKIMORI_API_URL = 'https://shikimori.one/api'
SHIKIMORI_API_URL_V2 = 'https://shikimori.one/api/v2'
SHIKIMORI_OAUTH_URL = 'https://shikimori.one/oauth'
DEFAULT_REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

RT = TypeVar('RT')

second_rate = RequestRate(MAX_CALLS_PER_SECOND, Duration.SECOND)
minute_rate = RequestRate(MAX_CALLS_PER_MINUTE, Duration.MINUTE)
request_limiter = Limiter(second_rate, minute_rate)


class Client:
    """Base client class for shikithon API class.

    Contains logic and methods for making requests to the shikimori API
    as well as validating config and etc.
    """

    __slots__ = ('endpoints', '_app_name', '_store', '_auto_close_store',
                 '_session', '_config')

    def __init__(self,
                 app_name: str = 'Api Test',
                 store: Store = NullStore(),
                 auto_close_store: bool = True) -> None:
        self._app_name = app_name
        self._store = store
        self.endpoints = Endpoints(SHIKIMORI_API_URL, SHIKIMORI_API_URL_V2,
                                   SHIKIMORI_OAUTH_URL)

        self._session = None
        self._config = None
        self._auto_close_store = auto_close_store

    @property
    def closed(self) -> bool:
        """Check if session is closed."""
        return self._session is None

    @property
    def restricted_mode(self) -> bool:
        """Returns current restrict mode of client object.

        If true, client object can access only public methods

        :return: Current restrict mode
        :rtype: bool
        """
        return self._config is None

    @property
    def store(self) -> Store:
        """Gets store object.

        :return: Store object
        :rtype: Store
        """
        return self._store

    @store.setter
    def store(self, store: Store):
        """Sets store object.

        :param store: Store object
        :type store: Store
        """
        if self._auto_close_store and self.store.status:
            asyncio.ensure_future(self.store.close())
        self._store = store

    @property
    def user_agent(self) -> Dict[str, str]:
        """Returns current session User-Agent.

        :return: Session User-Agent
        :rtype: Dict[str, str]
        """
        return {'User-Agent': self._session.headers['User-Agent']}

    @user_agent.setter
    def user_agent(self, app_name: str):
        """Update session headers and set user agent.

        :param app_name: OAuth App name
        :type app_name: str
        """
        if not self.closed:
            self._session.headers.update({'User-Agent': app_name})

    @property
    def authorization_header(self) -> Dict[str, str]:
        """Gets authorization header for current session.

        :return: Authorization header
        :rtype: Dict[str, str]
        """
        return {'Authorization': self._session.headers['Authorization']}

    @authorization_header.setter
    def authorization_header(self, access_token: str):
        """Sets authorization header to current session.

        :param access_token: Access token
        :type access_token: str
        """
        if not self.closed:
            self._session.headers.update(
                {'Authorization': 'Bearer ' + access_token})

    @property
    def config(self) -> Optional[Dict[str, Any]]:
        """Gets current config.

        If config is not availble, returns None.

        :return: Current config
        :rtype: Optional[Dict[str, Any]]
        """
        return self._config

    @config.setter
    def config(self, config: Dict[str, Any]):
        """Sets new config.

        If passed config isn't valid, raises Exception.

        :param config: New config data
        :type config: Dict[str, Any]
        """
        if self.is_valid_config(config):
            self._config = config

    @property
    def scopes(self) -> Optional[List[str]]:
        """Gets current app scopes.

        If app is in restricted mode, returns None.

        :return: Current scopes
        :rtype: Optional[List[str]]
        """
        if not self.restricted_mode:
            return cast(str, self._config['scopes']).split()
        return None

    def is_valid_config(self,
                        config: Dict[str, Any],
                        raises: bool = True) -> bool:
        """Validates passed config.

        Method checks config for required dict keys.
        If some of keys are missing, returns False or raises Exception
        if raises parameter is True.

        :param config: Config to validate
        :type config: Dict[str, Any]

        :param raises: If True, raises Exception if config is invalid
        :type raises: bool

        :return: True if config is valid, False otherwise
        :rtype: bool
        """
        if not config.get('app_name'):
            if raises:
                raise MissingAppVariableException('app_name')
            return False

        if not config.get('client_id'):
            if raises:
                raise MissingAppVariableException('client_id')
            return False

        if not config.get('client_secret'):
            if raises:
                raise MissingAppVariableException('client_secret')
            return False

        if not config.get('auth_code') and not config.get('access_token'):
            if raises:
                raise MissingAppVariableException('auth_code or access_token')
            return False

        if not config.get('redirect_uri'):
            config['redirect_uri'] = DEFAULT_REDIRECT_URI

        if not config.get('scopes'):
            config['scopes'] = ''

        return True

    @asynccontextmanager
    async def auth(self,
                   app_name: Optional[str] = None,
                   client_id: Optional[str] = None,
                   client_secret: Optional[str] = None,
                   auth_code: Optional[str] = None,
                   access_token: Optional[str] = None,
                   refresh_token: Optional[str] = None,
                   token_expire_at: Optional[int] = None,
                   redirect_uri: str = DEFAULT_REDIRECT_URI,
                   scopes: str = '') -> Client:
        """Async context manager for authentification.

        If client is already authentificated, raises Exception.

        :param app_name: OAuth App name
        :type app_name: Optional[str]

        :param client_id: OAuth App client id
        :type client_id: Optional[str]

        :param client_secret: OAuth App client secret
        :type client_secret: Optional[str]

        :param auth_code: OAuth App auth code
        :type auth_code: Optional[str]

        :param access_token: OAuth App access token
        :type access_token: Optional[str]

        :param refresh_token: OAuth App refresh token
        :type refresh_token: Optional[str]

        :param token_expire_at: OAuth App token expire time
        :type token_expire_at: Optional[int]

        :param redirect_uri: OAuth App redirect uri
        :type redirect_uri: str

        :param scopes: OAuth App scopes
        :type scopes: str

        :return: Client object
        :rtype: Client
        """
        if not self.closed:
            raise Exception('Client is already running')

        if app_name is None:
            app_name = self._app_name

        async with self:
            if access_token is not None:
                self.config = await self._store.fetch_by_access_token(
                    app_name, access_token)
            elif auth_code is not None:
                self.config = await self._store.fetch_by_auth_code(
                    app_name, auth_code)

            if self.config is None:
                if client_id is None or client_secret is None:
                    raise Exception(
                        'Client_id and client_secret must be defined')

                if access_token is not None:
                    self.config = {
                        'app_name': app_name,
                        'client_id': client_id,
                        'client_secret': client_secret,
                        'redirect_uri': redirect_uri,
                        'auth_code': auth_code,
                        'scopes': scopes,
                        'access_token': access_token,
                        'refresh_token': refresh_token,
                        'token_expire_at': token_expire_at
                    }
                elif auth_code is not None:
                    token_data = await self.get_access_token(
                        client_id, client_secret, auth_code, redirect_uri)
                    self.config = {
                        'app_name':
                            app_name,
                        'client_id':
                            client_id,
                        'client_secret':
                            client_secret,
                        'redirect_uri':
                            redirect_uri,
                        'auth_code':
                            auth_code,
                        'scopes':
                            token_data['scope'],
                        'access_token':
                            token_data['access_token'],
                        'refresh_token':
                            token_data['refresh_token'],
                        'token_expire_at':
                            token_data['created_at'] + token_data['expires_in']
                    }
                else:
                    raise Exception('Auth_code or access_token must be defined')

                await self._store.save_config(**self.config)

            self.user_agent = self.config['app_name']
            self.authorization_header = self.config['access_token']

            yield self

    async def get_access_token(self, client_id: str, client_secret: str,
                               auth_code: str,
                               redirect_uri: str) -> Dict[str, Any]:
        """Gets new access token.

        :param client_id: Client ID
        :type client_id: str

        :param client_secret: Client secret
        :type client_secret: str

        :param auth_code: Authorization code
        :type auth_code: str

        :param redirect_uri: Redirect URI
        :type redirect_uri: str

        :return: New access token
        :rtype: Dict[str, Any]
        """
        logger.info('Getting new access token')
        return await self.request(self.endpoints.oauth_token,
                                  data={
                                      'grant_type': 'authorization_code',
                                      'client_id': client_id,
                                      'client_secret': client_secret,
                                      'code': auth_code,
                                      'redirect_uri': redirect_uri
                                  },
                                  request_type=RequestType.POST,
                                  output_logging=False)

    async def refresh_access_token(self, client_id: str, client_secret: str,
                                   refresh_token: str) -> Dict[str, Any]:
        """Refreshes expired access token.

        :param client_id: Client ID
        :type client_id: str

        :param client_secret: Client secret
        :type client_secret: str

        :param refresh_token: Refresh token
        :type refresh_token: str

        :return: Refreshed access token
        :rtype: Dict[str, Any]
        """
        logger.info('Refreshing current access token')
        return await self.request(self.endpoints.oauth_token,
                                  data={
                                      'grant_type': 'refresh_token',
                                      'client_id': client_id,
                                      'client_secret': client_secret,
                                      'refresh_token': refresh_token
                                  },
                                  request_type=RequestType.POST,
                                  output_logging=False)

    def token_expired(self, token_expire_at: int):
        """Checks if current access token is expired.

        :return: Result of token expiration check
        :rtype: bool
        """
        logger.debug('Checking if current time is greater '
                     'than current token expire time')
        return int(time()) > token_expire_at

    @request_limiter.ratelimit('shikithon_request', delay=True)
    @backoff.on_exception(backoff.expo,
                          RetryLaterException,
                          max_time=5,
                          max_tries=10,
                          jitter=None)
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
        """Create request and return response JSON.

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

        :raises RetryLaterException: If Shikimori API returns 429 status code
        :raises Exception: If tokens not refreshed
        """
        if self.closed:
            return

        if not self.restricted_mode and \
           url != self.endpoints.oauth_token and \
           self.config['refresh_token'] is not None:
            token_expire_at = self.config['token_expire_at']
            if isinstance(token_expire_at,
                          int) and self.token_expired(token_expire_at):
                token_data = await self.refresh_access_token(
                    self.config['client_id'], self.config['client_secret'],
                    self.config['refresh_token'])
                if token_data.get('error'):
                    raise Exception(f'Tokens not refreshed: {token_data}')
                self._config.update(
                    refresh_token=token_data['refresh_token'],
                    token_expire_at=token_data['created_at'] +
                    token_data['expires_in'],
                )
                self.is_valid_config(self.config)
                await self._store.save_config(**self.config)

        logger.info(
            f'{request_type.value} {url}{Utils.convert_to_query_string(query)}')
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

        if response.status == ResponseCode.RETRY_LATER.value:
            logger.warning('Hit retry later code. Retrying backoff...')
            raise RetryLaterException

        if response.status == 401 and \
           cast(dict, await response.json()).get('error_description') \
           == 'The access token expired' and \
           not self.restricted_mode and \
           self.config['refresh_token'] is not None:
            token_data = await self.refresh_access_token(
                self.config['client_id'], self.config['client_secret'],
                self.config['refresh_token'])
            self._config.update(
                refresh_token=token_data['refresh_token'],
                token_expire_at=token_data['created_at'] +
                token_data['expires_in'],
            )
            self.is_valid_config(self.config)
            await self._store.save_config(**self.config)

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
        """Make multiple requests to API at the same time.

        :param requests: List of requests
        :type requests: List[Callable[..., RT]]

        :return: List of responses
        :rtype: List[Union[BaseException, RT]]
        """
        if self.closed:
            return []

        logger.info(f'Gathering {len(requests)} requests')
        return await asyncio.gather(*requests, return_exceptions=True)

    async def open(self) -> Client:
        """Open session and return self.

        :return: Client instance
        :rtype: Client
        """
        if self.closed:
            self._session = ClientSession()
            self.user_agent = self._app_name
            if not self.store.status:
                await self._store.open()
        return self

    async def close(self) -> None:
        """Close session."""
        if not self.closed:
            await self._session.close()
            self._session = None
            self._config = None
            if self._auto_close_store:
                await self._store.close()

    async def __aenter__(self) -> Client:
        """Async context manager entry point.

        :return: Client instance
        :rtype: Client
        """
        return await self.open()

    async def __aexit__(self, *args) -> None:
        """Async context manager exit point."""
        await self.close()
