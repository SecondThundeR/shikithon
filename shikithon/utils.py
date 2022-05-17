"""
Set of utility methods for the shikithon library.

This file contains the Utils class
with all the necessary utility methods
to work with the library
"""
from enum import Enum
from time import time
from typing import Any, Dict, List, Optional, Union

from loguru import logger

LOWER_LIMIT_NUMBER = 1


class Utils:
    """
    Utils class.

    Contains all the necessary utility methods
    to work with the library
    """

    @staticmethod
    def prepare_query_dict(query_dict: Dict[str, str]) -> str:
        """
        Convert query dict to query string for endpoint link.

        :param query_dict: Query dictionary
        :type query_dict: Dict[str, str]

        :return: Query string
        :rtype: str
        """
        logger.debug(f'Converting {query_dict=} to string')
        query_dict_str = '&'.join(
            f'{key}={val}' for (key, val) in query_dict.items())
        logger.debug(f'Formed {query_dict_str=}')
        return f'?{query_dict_str}'

    @staticmethod
    def convert_app_name(app_name: str) -> str:
        """
        Converts app name to snake case for use in
        config cache filename.

        :param app_name: Current OAuth app name
        :type app_name: str

        :return: Converted app name for filename
        :rtype: str
        """
        logger.debug(f'Converting {app_name=} for cached config')
        return '_'.join(app_name.lower().split(' '))

    @staticmethod
    def get_new_expire_time(time_expire_constant: int) -> int:
        """
        Generates new token expire time.

        :param time_expire_constant: Token lifetime value
        :type time_expire_constant: int

        :return: New token expire time
        :rtype: int
        """
        logger.debug(f'Getting new expiration time with a lifetime '
                     f'of {time_expire_constant} seconds')
        return int(time()) + time_expire_constant

    @staticmethod
    def generate_query_dict(
        **params_data: Optional[Union[str, bool, int, Enum, List[Union[int,
                                                                       str]]]]
    ) -> Dict[str, str]:
        """
        Returns valid query dict for API requests.

        This methods checks for data type and converts to valid one.

        :param params_data: API methods parameters data
        :type params_data:
            Optional[Union[str, bool, int, Enum, List[Union[int, str]]]]

        :return: Valid query dictionary
        :rtype: Dict[str, str]
        """
        logger.debug(
            f'Generating query dictionary for request. Passed {params_data=}')
        query_dict: Dict[str, str] = {}
        for key, data in params_data.items():
            if data is None:
                continue
            if isinstance(data, bool):
                if data is True:
                    query_dict[key] = str(int(data))
                else:
                    continue
            elif isinstance(data, int):
                query_dict[key] = str(data)
            elif isinstance(data, Enum):
                query_dict[key] = data.value
            elif isinstance(data, list):
                formatted_data: List[str] = []
                for item in data:
                    if isinstance(item, Enum):
                        formatted_data.append(item.value)
                    elif isinstance(item, int):
                        formatted_data.append(str(item))
                    elif isinstance(item, str) and item.isdigit():
                        formatted_data.append(item)
                query_dict[key] = ','.join(formatted_data)
            else:
                query_dict[key] = data
        logger.debug(f'Generated query dictionary: {query_dict=}')
        return query_dict

    @staticmethod
    def generate_data_dict(
        **dict_data: Optional[Union[str, bool, int, Enum, List[int]]]
    ) -> Union[Dict[str, str], Dict[str, Dict[str, str]]]:
        """
        Returns valid data dict for API requests.

        This methods checks for data type and converts to valid one.

        :param dict_data: API methods body data
        :type dict_data: Optional[Union[str, bool, int, Enum, List[int]]]

        :return: Valid data dictionary
        :rtype: Optional[Union[str, bool, int, Enum, List[int]]]
        """
        logger.debug(
            f'Generating data dictionary for request. Passed {dict_data=}')
        if 'dict_name' not in dict_data:
            logger.debug(
                'There is no dict_name in dict_data. Returning empty dictionary'
            )
            return {}

        logger.debug('Extracting root dictionary name')
        data_dict_name: str = dict_data['dict_name']
        dict_data.pop('dict_name')

        logger.debug(f'Setting root dictionary "{data_dict_name}"')
        new_data_dict: Dict[str, Dict[str, Any]] = {data_dict_name: {}}
        for key, data in dict_data.items():
            if data is None:
                continue
            if isinstance(data, bool):
                new_data_dict[data_dict_name][key] = data
            elif isinstance(data, int):
                new_data_dict[data_dict_name][key] = str(data)
            elif isinstance(data, Enum):
                new_data_dict[data_dict_name][key] = data.value
            elif isinstance(data, list):
                formatted_data: List[str] = []
                for item in data:
                    if isinstance(item, Enum):
                        formatted_data.append(item.value)
                    elif isinstance(item, int):
                        formatted_data.append(str(item))
                    elif isinstance(item, str) and item.isdigit():
                        formatted_data.append(item)
                new_data_dict[data_dict_name][key] = ','.join(formatted_data)
            else:
                new_data_dict[data_dict_name][key] = data
        logger.debug(f'Generated data dictionary: {new_data_dict=}')
        return new_data_dict

    @staticmethod
    def validate_query_number(query_number: Optional[int],
                              upper_limit: int) -> Optional[int]:
        """
        Validates query number.

        If number is lower, returns lower limit, else upper limit.
        If number is None, returns or None.

        :param query_number: Number to validate
        :type query_number: Optional[int]

        :param upper_limit: Upper limit for range check
        :type upper_limit: int

        :return: Validated number
        :rtype: Optional[int]
        """
        logger.debug(f'Validating query number ("{query_number}") '
                     f'with upper limit ("{upper_limit}")')
        if query_number is None:
            logger.debug('Query number is "None"')
            return query_number

        if query_number < LOWER_LIMIT_NUMBER:
            logger.debug(f'Query number ("{query_number}") is lower '
                         f'than lower limit ("{LOWER_LIMIT_NUMBER}"). '
                         f'Returning {LOWER_LIMIT_NUMBER=}')
            return LOWER_LIMIT_NUMBER

        if query_number > upper_limit:
            logger.debug(f'Query number ("{query_number}") is higher '
                         f'than upper limit ("{upper_limit}"). '
                         f'Returning {upper_limit=}')
            return upper_limit

        logger.debug(f'Returning passed query number ("{query_number}")')
        return query_number

    @staticmethod
    def query_numbers_validator(**query_numbers: List[Optional[int]]
                               ) -> Dict[str, Optional[int]]:
        """
        Gets all query numbers to validate and returns validated numbers.

        This method uses validate_query_number method for validating.

        Query numbers are passed in such form:
            { "page": [1, 100], ... }

            "page" <- Name of query number

            [1 (Passed value), 100 (Upper limit value)]

        This method outputs them like this:
            { "page": 1 }

            "page" <- Name of query number

            1 <- Validated number

        :param query_numbers: Passed query numbers to validate
        :type query_numbers: List[Optional[int]]
        :return: Dict of validated numbers
        :rtype: Dict[str, Optional[int]]
        """
        validated_numbers: Dict[str, Optional[int]] = {}
        for name, data in query_numbers.items():
            logger.debug(f'Checking "{name}" parameter')
            validated_numbers[name] = (Utils.validate_query_number(
                data[0], data[1]))
        return validated_numbers
