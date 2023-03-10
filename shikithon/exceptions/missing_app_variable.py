"""Exception for raising on missing app variable."""
from typing import List, Union

from loguru import logger


class MissingAppVariable(Exception):
    """Exception for raising on missing app variable."""

    def __init__(self, variable_name: Union[str, List[str]]):
        missing_variables = 'Missing app variable(s): '
        if isinstance(variable_name, list):
            missing_variables += ', '.join(variable_name)
        else:
            missing_variables += variable_name
        msg = 'There is a problem with some app variables. ' \
              'Recheck your config and try again.\n' \
              f'{missing_variables}'
        logger.error(msg)
        super().__init__(msg)
