"""
Set of utility methods for the shikithon library.

This file contains the Utils class
with all the necessary utility methods
to work with the library
"""
from time import time
from typing import Any, Dict, List, Optional, Type, Union

from aiohttp import ClientResponse
from aiohttp import ClientSession
from loguru import logger
from validators import url as is_url

from ..enums.enhanced_enum import EnhancedEnum
from ..enums.response import ResponseCode

LOWER_LIMIT_NUMBER = 1


class Utils:
    """
    Utils class.

    Contains all the necessary utility methods
    to work with the library
    """

    @staticmethod
    def convert_to_query_string(query_dict: Dict[str, str]) -> str:
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
    def convert_app_name_to_filename(app_name: str) -> str:
        """
        Converts app name to snake case for use in
        config store filename.

        :param app_name: Current OAuth app name
        :type app_name: str

        :return: Converted app name for filename
        :rtype: str
        """
        logger.debug(f'Converting {app_name=} for stored config')
        return '_'.join(app_name.lower().split(' '))

    @staticmethod
    def get_new_expire_time(time_expire_constant: int) -> int:
        """
        Gets new token expire time.

        :param time_expire_constant: Token lifetime value
        :type time_expire_constant: int

        :return: New token expire time
        :rtype: int
        """
        logger.debug(f'Getting new expiration time with a lifetime '
                     f'of {time_expire_constant} seconds')
        return int(time()) + time_expire_constant

    @staticmethod
    async def get_image_data(image_path: str) -> Dict[str, bytes]:
        """
        Extract image data from image path.
        If image_path is a link, fetch the image data from the link.

        :param image_path: Path to image
        :type image_path: str

        :return: Image data
        :rtype: Dict[str, bytes]
        """
        if isinstance(is_url(image_path), bool):
            async with ClientSession() as session:
                async with session.get(image_path) as image_response:
                    image_data = await image_response.read()
        else:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

        return {'image': image_data}

    @staticmethod
    def create_query_dict(
        **params_data: Optional[Union[str, bool, int, List[Union[int, str]]]]
    ) -> Dict[str, str]:
        """
        Creates query dict for API requests.

        This methods checks for data types and converts to valid one.

        :param params_data: API methods parameters data
        :type params_data:
            Optional[Union[str, bool, int, List[Union[int, str]]]]

        :return: Query dictionary
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
                query_dict[key] = ','.join(data)
            else:
                query_dict[key] = data
        logger.debug(f'Generated query dictionary: {query_dict=}')
        return query_dict

    @staticmethod
    def create_data_dict(
        **dict_data: Optional[Union[str, bool, int, List[int]]]
    ) -> Union[Dict[str, str], Dict[str, Dict[str, str]]]:
        """
        Creates data dict for API requests.

        This methods checks for data types and converts to valid one.

        :param dict_data: API methods body data
        :type dict_data: Optional[Union[str, bool, int, List[int]]]

        :return: Data dictionary
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
                new_data_dict[data_dict_name][key] = ','.join(data)
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

        If string value is in enum values, function returns True,
        otherwise False

        :param enum_params: Dictionary with values to validate.
        :type enum_params: Dict[Type[EnhancedEnum], Union[str, List[str]]])

        :return: Validator result
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

        logger.debug(
            f'All ({enums_counter}) enum parameters are valid'
            if enums_counter > 0 else 'There are no enum parameters to check')

        return True

    @staticmethod
    def get_validated_query_number(query_number: Optional[int],
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

        if isinstance(query_number, float):
            logger.debug(f'Query number ("{query_number}") is float. '
                         f'Converting to int')
            query_number = int(query_number)

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
            validated_numbers[name] = (Utils.get_validated_query_number(
                data[0], data[1]))
        return validated_numbers

    @staticmethod
    def validate_response_data(
        response_data: Union[List[Dict[str, Any]], Dict[str, Any], List[Any],
                             int],
        data_model: Optional[Type[Any]] = None,
        response_code: Optional[ResponseCode] = None,
        fallback: Optional[Any] = None
    ) -> Optional[Union[Type[Any], List[Type[Any]], List[Any], Dict[str, Any],
                        bool]]:
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

        :param fallback: Fallback value to return
        :type fallback: Optional[Any]

        :return: Parsed response data
        :rtype: Optional[Union[Type[Any], List[Type[Any]],
            List[Any], Dict[str, Any], bool]]
        """
        logger.debug(f'Validating return data: {response_data=}, '
                     f'{data_model=}, {response_code=}')

        if not response_data:
            logger.debug('Response data is empty. Returning it...')
            return response_data

        if isinstance(response_data, int):
            logger.debug('Response data is int. Returning value '
                         'of response code comparison')
            return response_data == response_code.value

        if isinstance(response_data, dict) and response_data.get('errors'):
            logger.debug('Response data contains unexpected errors. '
                         'Returning fallback value...')
            logger.warning(f'Errors list: {response_data.get("errors")}')
            return fallback

        if isinstance(response_data, list) \
                and len(response_data) == 1:
            if isinstance(response_data[0], str) \
                    and response_data[0].find('Invalid') != -1:
                logger.debug('Response data contains info about invalid data. '
                             'Returning fallback value')
                logger.warning(response_data[0])
                return fallback

        if 'errors' in response_data or 'code' in response_data:
            logger.debug(
                'Response data contains errors info. Returning fallback value')
            return fallback

        if 'notice' in response_data or 'success' in response_data:
            logger.debug('Response data contains success info. Returning True')
            return True

        if 'is_ignored' in response_data and data_model is None:
            logger.debug('Response data contains is_ignored. '
                         'Returning status of is_ignored')
            return response_data.get('is_ignored')

        if data_model is None:
            logger.debug("Data model isn't passed. Returning response data")
            return response_data

        logger.debug('Data model is passed. Returning parsed data')
        return [data_model(**item) for item in response_data] if isinstance(
            response_data, list) else data_model(**response_data)

    @staticmethod
    async def extract_empty_response_data(
            response: ClientResponse) -> Union[str, int]:
        response_text = await response.text()
        response_status = response.status
        return response_status \
            if not response_text else response_text
