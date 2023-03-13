"""Exceptions for shikithon API class.

Used for raising on validation of config/app data, request errors, etc.
"""

from .already_running_client import AlreadyRunningClient
from .invalid_content_type import InvalidContentType
from .missing_app_variable import MissingAppVariable
from .retry_later import RetryLater
from .shikimori_api_response_error import ShikimoriAPIResponseError
from .shikithon_exception import ShikithonException
from .store_exception import StoreException

__all__ = [
    'AlreadyRunningClient', 'MissingAppVariable', 'RetryLater',
    'StoreException', 'ShikimoriAPIResponseError', 'InvalidContentType',
    'ShikithonException'
]
