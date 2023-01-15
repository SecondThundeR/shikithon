"""Exception for raising on missing authorization cade."""


class MissingAuthCode(Exception):

    def __init__(self, auth_link: str):
        super().__init__('It is impossible to initialize an API object'
                         'without missing auth code. To get one, go to '
                         f'{auth_link} and insert code in config.')
