"""
Experimental version of utils.py
"""

from typing import Dict, Optional

from loguru import logger


class ExperimentalUtils:
    """
    Experimental Utils class.

    Alternative version of utils class.
    Contains new and untested functions.

    Currently used to backport all utility functions
    with proper type hints and fixes
    """

    @staticmethod
    def convert_to_query_string(query_dict: Optional[Dict[str, str]]):
        """Convert query dict to query string for endpoint link.

        If query_dict is None or empty, returns empty string.

        :param query_dict: Query dictionary
        :type query_dict: Dict[str, str]

        :return: Query string
        :rtype: str
        """
        logger.debug(f'Converting {query_dict=} to string')
        if not query_dict:
            logger.debug('Query dictionary is empty. Returning empty string...')
            return ''
        query_dict_str = '&'.join(
            f'{key}={val}' for (key, val) in query_dict.items())
        logger.debug(f'Formed {query_dict_str=}')
        return f'?{query_dict_str}'
