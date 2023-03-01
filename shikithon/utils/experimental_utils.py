"""
Experimental version of utils.py
"""

from typing import Any, Dict, Optional

from aiohttp import ClientSession
from loguru import logger
from validators import url

from ..enums.enhanced_enum import EnhancedEnum


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
            logger.debug('Query dictionary is None or empty. '
                         'Returning empty string')
            return ''

        query_dict_str = '&'.join(
            f'{key}={val}' for (key, val) in query_dict.items())

        logger.debug(f'Formed string: "{query_dict_str=}"')
        return f'?{query_dict_str}'

    @staticmethod
    async def get_image_data(image_path: str):
        """Extract image data from image path.

        If image_path is a link, fetch the image data from the link.

        :param image_path: Path to image
        :type image_path: str

        :return: Image data
        :rtype: Dict[str, bytes]
        """
        if isinstance(url(image_path), bool):
            async with ClientSession() as session:
                async with session.get(image_path) as image_response:
                    image_data = await image_response.read()
        else:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

        return {'image': image_data}

    @staticmethod
    def create_query_dict(**params_data: Optional[Any]):
        """Creates query dict for API requests.

        This methods checks for data types and converts to valid one.

        :param params_data: API methods parameters data
        :type params_data: Optional[Any]

        :return: Query dictionary
        :rtype: Dict[str, str]
        """
        logger.debug(
            'Generating query dictionary for request. ' \
            f'Passed {params_data=}'
        )

        query_dict: Dict[str, str] = {}

        for key, data in params_data.items():
            if data is None:
                continue
            if isinstance(data, bool):
                query_dict[key] = str(int(data))
            elif isinstance(data, int):
                query_dict[key] = str(data)
            elif isinstance(data, list):
                query_dict[key] = ','.join([str(x) for x in data])
            else:
                # If something else passed, trying to convert to string
                query_dict[key] = str(data)

        logger.debug(f'Generated query dictionary: {query_dict=}')
        return query_dict

    @staticmethod
    def is_enum_passed(*params: Any):
        """Checks if passed params are actually enums.

        Parameters are of the "Any" type, since
        you can pass anything when calling a library method,
        so the task of the method is to check the correctness
        of the passed enums

        :param params: Params of function to check
        :type params: Any

        :return: Check result
        :rtype: bool
        """
        logger.debug('Checking is passed params are enums')
        for data in params:
            if data is None:
                continue
            elif isinstance(data, list):
                for item in data:
                    if not isinstance(item, EnhancedEnum):
                        logger.debug('Passed parameter is not an enum!')
                        return False
            elif not isinstance(data, EnhancedEnum):
                logger.debug('Passed parameter is not an enum!')
                return False
        logger.debug('All passed parameters are enums!')
        return True
