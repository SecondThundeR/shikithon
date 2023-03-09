"""
Set of utility methods for the shikithon library.

This file contains the Utils class
with all the necessary utility methods
to work with the library
"""

from typing import (Any, Dict, List, Optional, overload, Tuple, Type, TypeVar,
                    Union)

from aiohttp import ClientSession
from loguru import logger
from pydantic import BaseModel
from validators import url

from ..enums import ResponseCode
from ..enums.enhanced_enum import EnhancedEnum

LOWER_LIMIT_NUMBER = 1
M = TypeVar('M', bound=BaseModel)


class Utils:
    """
    Utils class.

    Contains all the necessary utility methods
    to work with the library
    """

    @staticmethod
    def convert_to_query_string(query_dict: Optional[Dict[str, str]]):
        """Converts query dict to query string for endpoint link.

        If query_dict is None or empty, returns empty string.

        :param query_dict: Query dictionary
        :type query_dict: Dict[str, str]

        :return: Query string
        :rtype: str
        """
        logger.debug(f'Converting {query_dict} to query string')

        if not query_dict:
            logger.debug('Query dictionary is None or empty. '
                         'Returning empty string')
            return ''

        query_dict_str = '&'.join(
            f'{key}={val}' for (key, val) in query_dict.items())

        query_string = f'?{query_dict_str}'

        logger.debug(f'Formed string: "{query_string}"')
        return query_string

    @staticmethod
    async def get_image_data(image_path: str):
        """Extracts image data from image path.

        If image_path is a link, fetch the image data from the link.

        :param image_path: Path to image
        :type image_path: str

        :return: Image data
        :rtype: Dict[str, bytes]
        """
        logger.debug(f'Getting image from "{image_path}"')

        if isinstance(url(image_path), bool):
            logger.debug('Image path is a link. Querying image data')
            async with ClientSession() as session:
                async with session.get(image_path) as image_response:
                    image_data = await image_response.read()
        else:
            logger.debug('Image path is local. Reading image data')
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

        logger.debug('Extracted image data. Returning')
        return {'image': image_data}

    @staticmethod
    def create_query_dict(**params_data: Optional[Any]):
        """Creates query dictionary for API request.

        This methods checks for data types and converts to valid one.

        :param params_data: Parameters data for API request
        :type params_data: Optional[Any]

        :return: Query dictionary
        :rtype: Dict[str, str]
        """
        logger.debug(
            'Generating query dictionary for request. ' \
            f'Passed {params_data=}'
        )

        query_dict: Dict[str, str] = {}

        logger.debug('Extracting data for query dictionary')
        for key, data in params_data.items():
            if data is None:
                continue
            query_dict.update({key: Utils.convert_dictionary_value(data)})

        logger.debug(f'Generated query dictionary: {query_dict=}')
        return query_dict

    @staticmethod
    def create_data_dict(**dict_data: Optional[Any]):
        """Creates data dictionary for API request.

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
                'Returning dictionary without root'
            )
            return Utils.create_query_dict(**dict_data)

        logger.debug(f'Setting root dictionary with name "{data_dict_name}"')
        new_data_dict: Dict[str, Dict[str, str]] = {data_dict_name: {}}

        logger.debug('Extracting data for data dictionary')
        for key, data in dict_data.items():
            if data is None:
                continue
            new_data_dict[data_dict_name].update(
                {key: Utils.convert_dictionary_value(data)})

        logger.debug(f'Generated data dictionary: {new_data_dict}')
        return new_data_dict

    @staticmethod
    def convert_dictionary_value(dict_value: Any):
        """Converts dictionary value to string.

        :param dict_value: Dictionary value
        :type dict_value: Any

        :return: Converted value
        :rtype: str
        """
        logger.debug(f'Converting value "{dict_value}" to string')

        if isinstance(dict_value, bool):
            return str(int(dict_value))
        elif isinstance(dict_value, int):
            return str(dict_value)
        elif isinstance(dict_value, (list, tuple)):
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
                        logger.warning(f'Parameter ({item}) is not an enum!')
                        return False
            elif not isinstance(data, EnhancedEnum):
                logger.warning(f'Parameter ({data}) is not an enum!')
                return False

        logger.debug('All passed parameters are enums!')
        return True

    @overload
    @staticmethod
    def validate_query_number(number: None, limit: int) -> None:
        ...

    @overload
    @staticmethod
    def validate_query_number(number: int, limit: int) -> int:
        ...

    @overload
    @staticmethod
    def validate_query_number(number: float, limit: int) -> int:
        ...

    @staticmethod
    def validate_query_number(number: Optional[Union[int, float]], limit: int):
        """Validates passed query number.

        If number is lower, returns lower limit, else upper limit.
        If number is None, returns or None.

        :param number: Number to validate
        :type number: Optional[Union[int, float]]

        :param limit: Upper limit for range check
        :type limit: int

        :return: Validated number
        :rtype: Optional[int]
        """
        logger.debug(f'Validating query number "{number}" '
                     f'with upper limit "{limit}"')

        if number is None:
            logger.debug('Query number is empty. Returning')
            return number

        if isinstance(number, float):
            logger.debug(f'Query number "{number}" is a float. '
                         'Converting to int')
            number = int(number)

        if number < LOWER_LIMIT_NUMBER:
            logger.debug(f'Query number "{number}" is lower '
                         f'than lower limit "{LOWER_LIMIT_NUMBER}". '
                         'Returning lower limit value')
            return LOWER_LIMIT_NUMBER

        if number > limit:
            logger.debug(f'Query number "{number}" is higher '
                         f'than upper limit "{limit}". '
                         'Returning upper limit value')
            return limit

        logger.debug(f'Returning passed query number: "{number}"')
        return number

    @staticmethod
    def validate_query_numbers(**query_numbers: Tuple[Optional[Union[int,
                                                                     float]],
                                                      int]):
        """Validates passed tuples of query numbers.

        This method uses validate_query_number method for numbers validating.

        Query numbers are passed in such form:
            { "page": (1, 100), ... }

            "page" <- Name of query number

            (1 (Passed value), 100 (Upper limit value), )

        This method outputs them like this:
            { "page": 1 }

            "page" <- Name of query number

            1 <- Validated number

        :param query_numbers: Passed query numbers to validate
        :type query_numbers: Tuple[Optional[Union[int, float]], int]

        :return: Dict of validated numbers
        :rtype: Dict[str, Optional[int]]
        """
        logger.debug(f'Validating query numbers {query_numbers}')

        validated_numbers: Dict[str, Optional[int]] = {}

        for name, data in query_numbers.items():
            number, limit = data[0], data[1]
            validated_numbers.update(
                {name: Utils.validate_query_number(number, limit)})

        logger.debug(f'Returning validated numbers: {validated_numbers}')
        return validated_numbers

    @staticmethod
    def validate_response_code(response_code: Union[int, Any],
                               check_code: ResponseCode):
        """Validates passed response code.

        :param response_code: Passed response code
        :type response_code: Union[int, Any]

        :param check_code: Response code to compare with
        :type check_code: ResponseCode

        :return: Validated response code
        :rtype: bool
        """
        logger.debug(f'Validating response code: {response_code=}, '
                     f'{check_code=}')

        if not isinstance(response_code, int):
            logger.warning(
                'Got non-int value. Cancel comparing with response code')
            return False

        response_code_value: int = check_code.value
        return response_code == response_code_value

    @overload
    @staticmethod
    def validate_response_data(
        response_data: Dict[str, Any],
        data_model: Type[M],
    ) -> Optional[M]:
        ...

    @overload
    @staticmethod
    def validate_response_data(
        response_data: List[Dict[str, Any]],
        data_model: Type[M],
    ) -> List[M]:
        ...

    @staticmethod
    def validate_response_data(
        response_data: Union[Dict[str, Any], List[Dict[str, Any]]],
        data_model: Type[M],
    ) -> Optional[Union[Optional[M], List[M]]]:
        """Validates passed response data and returns parsed models.

        :param response_data: Passed response data
        :type response_data: Union[Dict[str, Any], List[Dict[str, Any]]]

        :param data_model: Model to convert into passed response data
        :type data_model: Type[M]

        :return: Parsed response data
        :rtype: Optional[Union[List, Optional[M], List[M]]]
        """
        logger.debug('Validating and parsing response data '\
                    f'using "{data_model.__name__}" data model')
        logger.debug(f'Passed response data: {response_data}')

        if not response_data:
            logger.debug('Response data is empty. Returning')
            if isinstance(response_data, dict):
                return None
            return []

        # TODO: Implement other checks from Utils method

        return [data_model(**item) for item in response_data] if isinstance(
            response_data, list) else data_model(**response_data)
