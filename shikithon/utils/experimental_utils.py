"""
Experimental version of utils.py
"""

from typing import Any, Dict, Optional, Union

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
            query_dict.update(
                {key: ExperimentalUtils.convert_dictionary_value(data)})

        logger.debug(f'Generated query dictionary: {query_dict=}')
        return query_dict

    @staticmethod
    def create_data_dict(**dict_data: Optional[Any]):
        """Creates data dict for API requests.

        This methods checks for data types and converts to valid one.

        If dict_data doesn't contain "dict_name" key,
        generated dictionary will have "temp" as root dictionary name,
        which will be removed on return.

        :param dict_data: Body data for API request
        :type dict_data: Optional[Any]

        :return: Data dictionary
        :rtype: Union[Dict[str, Dict[str, str]], Dict[str, str]]
        """
        logger.debug(
            f'Generating data dictionary for request. Passed {dict_data=}')

        logger.debug('Extracting root dictionary name')
        data_dict_name: Optional[str] = dict_data.pop('dict_name', None)

        if data_dict_name is None:
            logger.debug(
                'There is no dict_name in dict_data. ' \
                'Continuing with temporary root dictionary'
            )
            data_dict_name = 'temp'

        logger.debug(f'Setting root dictionary with name "{data_dict_name}"')
        new_data_dict: Dict[str, Dict[str, str]] = {data_dict_name: {}}

        for key, data in dict_data.items():
            if data is None:
                continue
            new_data_dict[data_dict_name].update(
                {key: ExperimentalUtils.convert_dictionary_value(data)})

        final_dict: Union[Dict[str, Dict[str, str]], Dict[str, str]]

        if data_dict_name == 'temp':
            final_dict = new_data_dict[data_dict_name]
        else:
            final_dict = new_data_dict

        logger.debug(f'Generated data dictionary: {final_dict}')
        return final_dict

    @staticmethod
    def convert_dictionary_value(dict_value: Any) -> str:
        """Converts dictionary value to string.

        :param dict_value: Dictionary value
        :type dict_value: Any

        :return: Converted value
        :rtype: str
        """
        if isinstance(dict_value, bool):
            return str(int(dict_value))
        elif isinstance(dict_value, int):
            return str(dict_value)
        elif isinstance(dict_value, list):
            return ','.join([str(x) for x in dict_value])
        else:
            # If something else passed, trying to convert to string
            return str(dict_value)

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
