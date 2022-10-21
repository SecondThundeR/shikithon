"""
Set of utility methods for the shikithon library.

This file contains the Utils class
with all the necessary utility methods
to work with the library
"""
from io import BytesIO
from time import time
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import requests.exceptions
from loguru import logger
from requests import get
from validators import url as is_url

from shikithon.enums.enhanced_enum import EnhancedEnum
from shikithon.enums.response import ResponseCode

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
    def get_image_data(
            image_path: str
    ) -> Dict[str, Tuple[str, Union[BytesIO, bytes], str]]:
        """
        Extract image data from image path.
        If image_path is a link, fetch the image data from the link.

        :param image_path: Path to image
        :type image_path: str

        :return: Image data
        :rtype: Dict[str, Tuple[str, Union[BytesIO, bytes], str]]
        """
        if isinstance(is_url(image_path), bool):
            try:
                image_response = get(image_path, timeout=5)
                image_data = BytesIO(image_response.content)
            except requests.exceptions.Timeout as e:
                logger.error(
                    f'Timeout while fetching image from link\nDetails: {e}')
                return {}
        else:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

        return {'image': (image_path, image_data, 'multipart/form-data')}

    @staticmethod
    def generate_query_dict(
        **params_data: Optional[Union[str, bool, int, List[Union[int, str]]]]
    ) -> Dict[str, str]:
        """
        Returns valid query dict for API requests.

        This methods checks for data type and converts to valid one.

        :param params_data: API methods parameters data
        :type params_data:
            Optional[Union[str, bool, int, List[Union[int, str]]]]

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
                query_dict[key] = str(int(data))
            elif isinstance(data, int):
                query_dict[key] = str(data)
            elif isinstance(data, list):
                formatted_data: List[str] = []
                for item in data:
                    if isinstance(item, int):
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
        **dict_data: Optional[Union[str, bool, int, List[int]]]
    ) -> Union[Dict[str, str], Dict[str, Dict[str, str]]]:
        """
        Returns valid data dict for API requests.

        This methods checks for data type and converts to valid one.

        :param dict_data: API methods body data
        :type dict_data: Optional[Union[str, bool, int, List[int]]]

        :return: Valid data dictionary
        :rtype: Optional[Union[str, bool, int, List[int]]]
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
            elif isinstance(data, list):
                formatted_data: List[str] = []
                for item in data:
                    if isinstance(item, int):
                        formatted_data.append(str(item))
                    elif isinstance(item, str) and item.isdigit():
                        formatted_data.append(item)
                new_data_dict[data_dict_name][key] = ','.join(formatted_data)
            else:
                new_data_dict[data_dict_name][key] = data
        logger.debug(f'Generated data dictionary: {new_data_dict=}')
        return new_data_dict

    @staticmethod
    def validate_enum_params(
            enum_params: Dict[Type[EnhancedEnum], Union[str,
                                                        List[str]]]) -> bool:
        """
        Validates string parameter with enum values.

        Function gets dictionary with enum and string values.
        If string value is in enum values, function returns True.
        If not, throws logger.warning() and returns False

        :param enum_params: Dictionary with values to validate.
        :type enum_params: Dict[Type[EnhancedEnum], Union[str, List[str]]])

        :return: Result of validation
        :rtype: bool
        """
        enums_counter = 0
        logger.debug('Checking if enum parameters are valid')
        for enum, param in enum_params.items():
            if param is None:
                continue

            enums_counter += 1
            enum_values = enum.get_values()

            if isinstance(param, list):
                for item in param:
                    if item not in enum_values:
                        logger.warning(f'"{item}" is not valid value '
                                       f'of "{enum.get_name()}".'
                                       f'\nAccepted values: {enum_values}')
                        return False
                break

            if param not in enum_values:
                logger.warning(
                    f'"{param}" is not valid value of "{enum.get_name()}".'
                    f'\nAccepted values: {enum_values}')
                return False

        if enums_counter > 0:
            logger.debug(f'All ({enums_counter}) enum parameters are valid')
        else:
            logger.debug('There are no enum parameters to check')

        return True

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

    @staticmethod
    def validate_return_data(
        response_data: Union[List[Dict[str, Any]], Dict[str, Any], List[Any],
                             int],
        data_model: Optional[Type[Any]] = None,
        response_code: Optional[ResponseCode] = None
    ) -> Optional[Union[Type[Any], List[Type[Any]], List[Any], bool]]:
        """
        Validates passed response data and returns
        parsed models.

        :param response_data: Response data
        :type response_data: Union[List[Dict[str, Any],
            Dict[str, Any], List[Any]]]

        :param data_model: Model to convert into passed response data
        :type data_model: Optional[Type[Any]]

        :param response_code: Code of response
            (Used only when response_data is int)
        :type response_code: Optional[ResponseCode]

        :return: Parsed response data
        :rtype: Optional[Union[Type[Any], List[Type[Any]], bool]]
        """
        logger.debug(f'Validating return data: {response_data=}, '
                     f'{data_model=}, {response_code=}')
        if not response_data:
            logger.debug('Response data is empty. Returning None')
            return None

        if isinstance(response_data, int):
            logger.debug('Response data is int. Returning value '
                         'of response code comparison')
            return response_data == response_code.value

        if 'errors' in response_data or 'code' in response_data:
            logger.debug('Response data contains errors info. Returning None')
            return None

        if 'notice' in response_data or 'success' in response_data:
            logger.debug('Response data contains success info. Returning True')
            return True

        if 'is_ignored' in response_data:
            logger.debug('Response data contains is_ignored. '
                         'Returning status of is_ignored')
            return response_data['is_ignored']

        if data_model is None:
            logger.debug("Data model isn't passed. Returning response data")
            return response_data

        logger.debug('Data model is passed. Returning parsed data')
        return [data_model(**item) for item in response_data] if isinstance(
            response_data, list) else data_model(**response_data)