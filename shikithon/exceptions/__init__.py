"""Exceptions for shikithon API class.

Used for raising on validation of config/app data.
Only RetryLater exception is used for raising on request errors.
"""

from .access_token_exception import AccessTokenException
from .missing_app_variable import MissingAppVariableException
from .missing_auth_code import MissingAuthCodeException
from .missing_config_data import MissingConfigDataException
from .retry_later import RetryLaterException

__all__ = [
    'AccessTokenException', 'MissingAuthCodeException',
    'MissingAppVariableException', 'MissingConfigDataException',
    'RetryLaterException'
]
