"""Exception for raising on missing app variable."""
from typing import List, Union


class MissingAppVariable(Exception):

    def __init__(self, variable_name: Union[str, List[str]]):
        exception_msg = 'Missing app variable(s): '
        if isinstance(variable_name, list):
            exception_msg += ', '.join(variable_name)
        else:
            exception_msg += variable_name
        super().__init__('There is a problem with some app variables. '
                         'Recheck your config and try again.\n'
                         f'{exception_msg}')
