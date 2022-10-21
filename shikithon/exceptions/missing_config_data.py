"""Exception for raising on missing config data."""


class MissingConfigData(Exception):

    def __init__(self):
        super().__init__('It is impossible to initialize an API object'
                         'without missing variables. '
                         'Recheck your config and try again.')
