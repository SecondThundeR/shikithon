"""Exception for raising on missing app variable."""


class MissingAppVariable(Exception):

    def __init__(self, variable_name: str):
        super().__init__(f'It is impossible to initialize an API object'
                         f'without missing variable "{variable_name}". '
                         f'Recheck your config and try again.')
