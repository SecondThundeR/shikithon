"""Exception for raising on access token errors."""


class AccessTokenError(Exception):

    def __init__(self, error_message: str):
        super().__init__(
            'An error occurred while receiving tokens, '
            f'here is the information from the response: {error_message}')
