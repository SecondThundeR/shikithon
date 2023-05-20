"""Base class for shikithon API class."""
from __future__ import annotations

import asyncio
from contextlib import asynccontextmanager
from time import time
from typing import (Any, AsyncIterator, Awaitable, Dict, List, Optional,
                    TypedDict, TypeVar, Union, cast)

import backoff
from aiohttp import ClientSession, ContentTypeError, FormData
from loguru import logger
from pyrate_limiter import Duration, Limiter, RequestRate

from .endpoints import Endpoints
from .enums import RequestType, ResponseCode
from .exceptions import (AlreadyRunningClient, InvalidContentType,
                         MissingAppVariable, RetryLater,
                         ShikimoriAPIResponseError, ShikithonException)
from .store import NullStore, Store
from .utils import Utils

MAX_CALLS_PER_SECOND = 5
MAX_CALLS_PER_MINUTE = 90

SHIKIMORI_API_URL = 'https://shikimori.me/api'
SHIKIMORI_API_URL_V2 = 'https://shikimori.me/api/v2'
SHIKIMORI_OAUTH_URL = 'https://shikimori.me/oauth'
DEFAULT_REDIRECT_URI = 'urn:ietf:wg:oauth:2.0:oob'

RT = TypeVar('RT')


class ClientConfig(TypedDict, total=False):
    app_name: str
    client_id: str
    client_secret: str
    redirect_uri: str
    scopes: str
    auth_code: Optional[str]
    access_token: str
    refresh_token: Optional[str]
    token_expire_at: Optional[int]


class TokensDict(TypedDict):
    access_token: str
    refresh_token: str
    token_type: str
    scope: str
    created_at: int
    expires_in: int


second_rate = RequestRate(MAX_CALLS_PER_SECOND, Duration.SECOND)
minute_rate = RequestRate(MAX_CALLS_PER_MINUTE, Duration.MINUTE)
request_limiter = Limiter(second_rate, minute_rate)


class Client:
    """Base client class for shikithon API class.

    Contains logic and methods for making requests to the shikimori API
    as well as validating config and etc
    """

    __slots__ = ('endpoints', '_app_name', '_store', '_auto_close_store',
                 '_session', '_config')

    def __init__(self,
                 app_name: str = 'Api Test',
                 store: Store = NullStore(),
                 auto_close_store: bool = True):
        self._app_name = app_name
        self._store = store
        self.endpoints = Endpoints(SHIKIMORI_API_URL, SHIKIMORI_API_URL_V2,
                                   SHIKIMORI_OAUTH_URL)

        self._session: Optional[ClientSession] = None
        self._config: Optional[ClientConfig] = None
        self._auto_close_store = auto_close_store

    @property
    def closed(self):
        """Checks if session is closed.

        :return: True if session is closed, False otherwise
        :rtype: bool
        """
        return self._session is None

    @property
    def restricted_mode(self):
        """Returns current restrict mode of client object.

        If true, client object can access only public methods

        :return: Current restrict mode
        :rtype: bool
        """
        return self._config is None

    @property
    def store(self):
        """Returns store object.

        :return: Store object
        :rtype: Store
        """
        return self._store

    def _set_user_agent(self, app_name: Optional[str]):
        """Updates session headers and set user agent.

        :param app_name: OAuth App name
        :type app_name: Optional[str]
        """
        if self._session is None:
            return

        if app_name is None:
            self._session.headers.pop('User-Agent', None)
            return
        self._session.headers.update({'User-Agent': app_name})

    user_agent = property(fset=_set_user_agent)

    def _set_authorization_header(self, access_token: Optional[str]):
        """Sets authorization header to current session.

        :param access_token: Access token
        :type access_token: Optional[str]
        """
        if self._session is None:
            return

        if access_token is None:
            self._session.headers.pop('Authorization', None)
            return
        self._session.headers.update(
            {'Authorization': 'Bearer ' + access_token})

    authorization_header = property(fset=_set_authorization_header)

    @property
    def config(self) -> Optional[ClientConfig]:
        """Returns current config.

        If config is not availble, returns None

        :return: Current config
        :rtype: Optional[ClientConfig]
        """
        return self._config

    @config.setter
    def config(self, config: Optional[ClientConfig]):
        """Sets new config.

        If passed config isn't valid, raises Exception

        :param config: New config data
        :type config: Optional[ClientConfig]
        """
        if config is None:
            return None

        self.validate_config(config)

        self._config = config

    def validate_config(self, config: ClientConfig):
        """Validates passed config.

        Method checks config for required dict keys

        :param config: Config to validate
        :type config: ClientConfig

        :return: True if config is valid, False otherwise
        :rtype: bool

        :raises MissingAppVariable: If config is invalid and raises is True
        """
        if not config.get('app_name'):
            raise MissingAppVariable('app_name')

        if not config.get('client_id'):
            raise MissingAppVariable('client_id')

        if not config.get('client_secret'):
            raise MissingAppVariable('client_secret')

        if not config.get('auth_code'):
            raise MissingAppVariable('auth_code')

        if not config.get('access_token'):
            raise MissingAppVariable('access_token')

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
                   scopes: str = '') -> AsyncIterator[Client]:
        """Async context manager for authentification.

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

        :return: Async iterator of client object
        :rtype: AsyncIterator[Client]

        :raises AlreadyRunningClient: If client is already running
        :raises MissingAppVariable: If some of required variables is missing
        """
        if not self.closed:
            raise AlreadyRunningClient()

        if app_name is None:
            app_name = self._app_name

        if self.store.closed:
            await self.store.open()

        try:
            async with self:
                if access_token is not None:
                    self.config = await self.store.fetch_by_access_token(
                        app_name, access_token)
                elif auth_code is not None:
                    self.config = await self.store.fetch_by_auth_code(
                        app_name, auth_code)

                if self.config is None:
                    if client_id is None or client_secret is None:
                        raise MissingAppVariable(['client_id', 'client_secret'])

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
                                token_data['created_at'] +
                                token_data['expires_in']
                        }
                    else:
                        raise MissingAppVariable(['auth_code', 'access_token'])

                    await self.store.save_config(**self.config)

                self.user_agent = self.config['app_name']
                self.authorization_header = self.config['access_token']

                yield self
        finally:
            self._config = None
            if self._auto_close_store and not self.store.closed:
                await self.store.close()

    async def get_access_token(self, client_id: str, client_secret: str,
                               auth_code: str, redirect_uri: str) -> TokensDict:
        """Returns new access token.

        :param client_id: Client ID
        :type client_id: str

        :param client_secret: Client secret
        :type client_secret: str

        :param auth_code: Authorization code
        :type auth_code: str

        :param redirect_uri: Redirect URI
        :type redirect_uri: str

        :return: New access token
        :rtype: TokensDict
        """
        logger.info('Getting new access token')

        data_dict = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code': auth_code,
            'redirect_uri': redirect_uri
        }

        tokens = await self.request(self.endpoints.oauth_token,
                                    data=data_dict,
                                    request_type=RequestType.POST,
                                    output_logging=False)
        return cast(TokensDict, tokens)

    async def refresh_access_token(
            self,
            client_id: str,
            client_secret: str,
            refresh_token: Optional[str] = None) -> TokensDict:
        """Refreshes expired access token.

        :param client_id: Client ID
        :type client_id: str

        :param client_secret: Client secret
        :type client_secret: str

        :param refresh_token: Refresh token
        :type refresh_token: Optional[str]

        :return: Refreshed access token
        :rtype: TokensDict
        """
        logger.info('Refreshing current access token')

        if refresh_token is None:
            raise ShikithonException('Missing refresh_token. Returning None')

        data_dict = {
            'grant_type': 'refresh_token',
            'client_id': client_id,
            'client_secret': client_secret,
            'refresh_token': refresh_token
        }

        tokens = await self.request(self.endpoints.oauth_token,
                                    data=data_dict,
                                    request_type=RequestType.POST,
                                    output_logging=False)
        return cast(TokensDict, tokens)

    def token_expired(self, token_expire_at: int):
        """Checks if current access token is expired.

        :return: True if token is expired, False otherwise
        :rtype: bool
        """
        logger.debug('Checking if token is expired')

        token_expiration_status = int(time()) > token_expire_at

        logger.debug(f'Token expire status: {token_expiration_status}')
        return token_expiration_status

    @backoff.on_exception(backoff.expo, RetryLater, max_time=10, max_tries=20)
    async def request(
        self,
        url: str,
        data: Optional[Union[Dict[str, Dict[str, str]], Dict[str, str]]] = None,
        form_data: Optional[FormData] = None,
        query: Optional[Dict[str, str]] = None,
        request_type: RequestType = RequestType.GET,
        output_logging: bool = True,
    ) -> Optional[Union[Any, int]]:
        """Creates request and returns response JSON.

        This method uses request_limiter library for rate limiting
        requests (Shikimori API limit: 90rpm and 5rps)

        To address duplication of methods
        for different request methods, this method
        uses RequestType enum

        :param url: URL for making request
        :type url: str

        :param data: Request body data
        :type data: Optional[Union[Dict[str, Dict[str, str]], Dict[str, str]]]

        :param form_data: Form data for multipart/form-data requests
        :type form_data: Optional[FormData]

        :param query: Query data for request
        :type query: Optional[Dict[str, str]]

        :param request_type: Type of current request
        :type request_type: RequestType

        :param output_logging: Parameter for logging JSON response
        :type output_logging: bool

        :return: Response JSON, status code or None
        :rtype: Optional[Union[Any, int]]

        :raises RetryLater: If Shikimori API returns 429 status code
        :raises ShikimoriAPIResponseError: If response status is
        not lower than 400
        :raises InvalidContentType: If response content type not JSON
        """
        if self.closed or self._session is None:
            return None

        logger.info(
            f'{request_type.value} {url}' \
            f'{Utils.convert_to_query_string(query)}')
        if output_logging:
            logger.debug(f'Request info details: {data=}, {query=}')

        if self._is_protected_request(url):
            token_expire_at = None if self.config is None else self.config.get(
                'token_expire_at')
            if isinstance(token_expire_at,
                          int) and self.token_expired(token_expire_at):
                await self._refresh_and_save_tokens()

        async with request_limiter.ratelimit('request', delay=True):
            if request_type == RequestType.GET:
                response = await self._session.get(url, params=query)
            elif request_type == RequestType.POST:
                response = await self._session.post(url,
                                                    data=form_data,
                                                    json=data,
                                                    params=query)
            elif request_type == RequestType.PUT:
                response = await self._session.put(url,
                                                   data=form_data,
                                                   json=data,
                                                   params=query)
            elif request_type == RequestType.PATCH:
                response = await self._session.patch(url,
                                                     data=form_data,
                                                     json=data,
                                                     params=query)
            elif request_type == RequestType.DELETE:
                response = await self._session.delete(url,
                                                      json=data,
                                                      params=query)
            else:
                logger.debug('Unknown request type passed. Returning None')
                return None

        await Utils.log_response_info(response, not output_logging)

        try:
            if response.status == 401 and self._is_protected_request(url):
                await self._refresh_and_save_tokens()
                return await self.request(url, data, form_data, query,
                                          request_type, output_logging)
            elif response.status == ResponseCode.RETRY_LATER.value:
                raise RetryLater('Hit retry later code. Retrying backoff')
            elif not response.ok:
                raise ShikimoriAPIResponseError(
                    method=response.method,
                    status=response.status,
                    url=repr(response.request_info.real_url),
                    text=await response.text())

            logger.debug('Check if response has empty body')
            response_text = await response.text()
            if response_text == '':
                logger.debug('Response has empty body. ' \
                    'Returning response status')
                return response.status
            elif response_text == 'null':
                logger.debug('Response is "null". Returning None')
                return None


            logger.debug('Response is not empty. ' \
                'Trying to extract JSON from response')
            try:
                json_response = await response.json()
            except ContentTypeError:
                # Special case for such method, like
                # /api/users/sign_out
                if response.content_type == 'text/plain':
                    logger.debug('Failed JSON extracting.' \
                        ' Getting response text')
                    return response_text
                logger.error("Response content type isn't valid JSON")
                raise InvalidContentType(response.content_type) from None

            if json_response is None or json_response == {}:
                logger.debug('JSON is empty. ' \
                    'Returning response status')
                return response.status

            logger.debug('Successful extraction. ' \
                    'Returning extracted data')
            return json_response
        finally:
            response.release()

    async def multiple_requests(self,
                                requests: List[Awaitable[RT]]) -> List[RT]:
        """Makes multiple requests to API at the same time.

        :param requests: List with async requests
        :type requests: List[Awaitable[RT]]

        :return: List of responses
        :rtype: List[RT]
        """
        if self.closed:
            return []

        logger.info(f'Gathering {len(requests)} requests')

        return await asyncio.gather(*requests, return_exceptions=False)

    async def _refresh_and_save_tokens(self):
        """Refreshes current access token and saves it to the store.

        Due to some problems when trying to refresh with
        Authorization header, this method sets the header to None
        before refreshing and then sets it back to the new token
        """
        if self._config is None:
            return None

        self.authorization_header = None

        token_data = await self.refresh_access_token(
            self._config['client_id'], self._config['client_secret'],
            self._config['refresh_token'])

        self.authorization_header = token_data['access_token']

        self._config.update({
            'access_token':
                token_data['access_token'],
            'refresh_token':
                token_data['refresh_token'],
            'token_expire_at':
                token_data['created_at'] + token_data['expires_in'],
        })

        self.validate_config(self._config)

        await self.store.save_config(**self._config)

    def _is_protected_request(self, url: str):
        """Checks if a protected request is being made.

        :param url: Request URL
        :type url: str

        :return: True if request is protected, False otherwise
        :rtype: bool
        """
        return not self.restricted_mode and \
                url != self.endpoints.oauth_token and \
                (self.config is not None and \
                    self.config['refresh_token'] is not None)

    async def open(self):
        """Opens session and returns self.

        :return: Client instance
        :rtype: Client
        """
        if self.closed:
            self._session = ClientSession()
            self.user_agent = self._app_name

        return self

    async def close(self):
        """Closes session."""
        if self.closed or self._session is None:
            return

        await self._session.close()
        self._session = None

    async def __aenter__(self):
        """Async context manager entry point.

        :return: Client instance
        :rtype: Client
        """
        return await self.open()

    async def __aexit__(self, *args):
        """Async context manager exit point."""
        await self.close()
