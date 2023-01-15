"""Exceptions for shikithon API class.

Used for raising on validation of config/app data, request errors, etc.
"""

from .access_token_error import AccessTokenError
from .already_running_client import AlreadyRunningClient
from .expired_access_token import ExpiredAccessToken
from .missing_app_variable import MissingAppVariable
from .missing_auth_code import MissingAuthCode
from .missing_config_data import MissingConfigData
from .retry_later import RetryLater
from .store_exception import StoreException

__all__ = [
    'AccessTokenError', 'AlreadyRunningClient', 'ExpiredAccessToken',
    'MissingAuthCode', 'MissingAppVariable', 'MissingConfigData', 'RetryLater',
    'StoreException'
]
