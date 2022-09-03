"""Custom exceptions for API class."""


class MissingConfigData(Exception):

    def __init__(self):
        super().__init__('It is impossible to initialize an API object'
                         'without missing variables. '
                         'Recheck your config and try again.')


class MissingAppVariable(Exception):

    def __init__(self, variable_name: str):
        super().__init__(f'It is impossible to initialize an API object'
                         f'without missing variable "{variable_name}". '
                         f'Recheck your config and try again.')


class MissingAuthCode(Exception):

    def __init__(self, auth_link: str):
        super().__init__('It is impossible to initialize an API object'
                         'without missing auth code. To get one, go to '
                         f'{auth_link} and insert code in config.')


class AccessTokenException(Exception):

    def __init__(self, error_message: str):
        super().__init__(
            'An error occurred while receiving tokens, '
            f'here is the information from the response: {error_message}')
