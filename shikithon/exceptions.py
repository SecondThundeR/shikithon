"""Custom exceptions for API class."""


class MissingConfigData(Exception):
    pass


class MissingAppName(Exception):
    pass


class MissingClientID(Exception):
    pass


class MissingClientSecret(Exception):
    pass


class MissingAppScopes(Exception):
    pass


class MissingAuthCode(Exception):
    pass


class AccessTokenException(Exception):
    pass
