"""Set of utility methods for the shikithon library.

This file contains the Utils class
with all the necessary utility methods
to work with the library
"""

import imghdr
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, overload

from aiohttp import ClientResponse, ClientSession, FormData
from loguru import logger
from pydantic import BaseModel, TypeAdapter
from validators import url

from ..enums import ResponseCode

LOWER_LIMIT_NUMBER = 1
CENSORED_FIELDS = (
    'access_token',
    'refresh_token',
)
M = TypeVar('M', bound=BaseModel)

R = TypeVar('R')
T = TypeVar('T')


class Utils:
    """Utils class.

    Contains all the necessary utility methods
    to work with the library
    """

    @staticmethod
    def convert_to_query_string(query_dict: Optional[Dict[str, str]]):
        """Converts query dict to query string for endpoint link.

        If query_dict is None or empty, returns empty string

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
    async def get_image_data(image_path: Optional[str]):
        """Extracts image data from image path.

        If image_path is a link, fetch the image data from the link

        :param image_path: Path to image
        :type image_path: str

        :return: Image data
        :rtype: Optional[bytes]
        """
        logger.debug(f'Getting image from "{image_path}"')

        if image_path is None:
            logger.debug('Image path is None or empty')
            return None

        if not isinstance(url(image_path), bool):
            logger.debug('Image path is local. Reading image data')
            return Utils._extract_local_image_data(image_path)

        logger.debug('Image path is a link. Querying image data')
        return await Utils._extract_remote_image_data(image_path)

    @staticmethod
    def _extract_local_image_data(image_path: str):
        """Extracts image data from local path.

        :param image_path: Path to local image
        :type image_path: str

        :return: Image data
        :rtype: Optional[bytes]
        """
        try:
            image_path_test = imghdr.what(image_path)
            if image_path_test is None:
                logger.warning('Passed image path is not a valid image')
                return None
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            logger.debug('Successfully extracted image data')
            return image_data
        except FileNotFoundError:
            logger.warning('Passed image file is not exists')
            return None

    @staticmethod
    async def _extract_remote_image_data(image_url: str):
        """Extracts image data from remote path.

        :param image_url: Path to remote image
        :type image_url: str

        :return: Image data
        :rtype: Optional[bytes]
        """
        async with ClientSession() as session:
            image_response = await session.get(image_url)
            if not image_response.content_type.startswith('image/'):
                logger.warning('Passed URL is not a valid image URL')
                return None
            logger.debug('Successfully extracted image data')
            return await image_response.read()

    @staticmethod
    def create_query_dict(**params_data: Optional[Any]):
        """Creates query dictionary for API request.

        This methods checks for data types and converts to valid one

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
            query_dict.update({key: Utils._convert_dictionary_value(data)})

        logger.debug(f'Generated query dictionary: {query_dict=}')
        return query_dict

    @staticmethod
    def create_data_dict(**dict_data: Optional[Any]):
        """Creates data dictionary for API request.

        This methods checks for data types and converts to valid one

        If dict_data doesn't contain "dict_name" key,
        generated dictionary will have "temp" as root dictionary name,
        which will be removed on return

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
                {key: Utils._convert_dictionary_value(data, data_dict=True)})

        logger.debug(f'Generated data dictionary: {new_data_dict}')
        return new_data_dict

    @staticmethod
    def _convert_dictionary_value(dict_value: Any, data_dict: bool = False):
        """Converts dictionary value to string.

        If data_dict is False, converts list values to comma-separated string.
        Otherwise, returns list value as is

        :param dict_value: Dictionary value
        :type dict_value: Any

        :param data_dict: Flag if checking value for data dictionary
        :type data_dict: bool

        :return: Converted value
        :rtype: str
        """
        logger.debug(f'Converting value "{dict_value}" to string')

        if isinstance(dict_value, bool):
            return str(int(dict_value))
        elif isinstance(dict_value, int):
            return str(dict_value)
        elif isinstance(dict_value, (list, tuple)):
            if data_dict is True:
                return dict_value
            return ','.join([str(x) for x in dict_value])
        elif isinstance(dict_value, bytes):
            return dict_value
        else:
            # If something else passed, trying to convert to string
            return str(dict_value)

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
            return [] if isinstance(response_data, list) else None

        return [data_model(**item) for item in response_data] if isinstance(
            response_data, list) else data_model(**response_data)

    @staticmethod
    def parse_mixed_response(response: Any, parse_type: Type[T]):
        """Parses response, mixed with other entities,
        that can't be parsed with validation utility.

        Due to fact, that every Manga and Ranobe can have both models as
        similar, this utility method helps parse response correctly

        :param response: Passed response data
        :type response: Any

        :param parse_type: Type for parsing response to
        :type parse_type: Type[T]

        :return: Parsed response to passed type
        :rtype: T
        """
        logger.info('Parsing response with mixed models')
        logger.info(f'Parsing using type: {parse_type}')
        adapter: TypeAdapter[T] = TypeAdapter(parse_type)
        return adapter.validate_python(response)

    @staticmethod
    def create_form_data(raw_data: Dict[str, Any]):
        """Creates form data for API request.

        Method converts dictionary with data to
        FormData object for API request

        :param raw_data: Raw data for API request
        :type raw_data: Dict[str, Any]

        :return: Form data
        :rtype: Optional[FormData]
        """
        if not isinstance(raw_data, dict):
            logger.debug('Passed data is not a dictionary')
            return None

        if any(isinstance(value, dict) for value in raw_data.values()):
            return Utils._generate_nested_form_data(raw_data)
        return Utils._generate_plain_form_data(raw_data)

    @staticmethod
    def _generate_nested_form_data(raw_data: Dict[str, Dict[str, Any]]):
        """Generates FormData for nested dictionaries.

        :param raw_data: Raw data for API request
        :type raw_data: Dict[str, Dict[str, Any]]

        :return: Generated FormData
        :rtype: FormData
        """
        form_data = FormData()
        logger.debug('Generating FormData for nested dictionaries')

        for key, value in raw_data.items():
            if isinstance(value, dict):
                for subkey, subvalue in value.items():
                    if isinstance(subvalue, list):
                        for list_value in subvalue:
                            form_data.add_field(f'{key}[{subkey}][]',
                                                list_value)
                    else:
                        form_data.add_field(f'{key}[{subkey}]', subvalue)
            else:
                form_data.add_field(key, value)

        logger.debug('Successfully created FormData object')
        return form_data

    @staticmethod
    def _generate_plain_form_data(raw_data: Dict[str, Any]):
        """Generates FormData for plain dictionary.

        :param raw_data: Raw data for API request
        :type raw_data: Dict[str, Any]

        :return: Generated FormData
        :rtype: FormData
        """
        form_data = FormData()
        logger.debug('Generating FormData for plain dictionary')

        for key, value in raw_data.items():
            if isinstance(value, list):
                for list_value in value:
                    form_data.add_field(f'{key}[]', list_value)
            form_data.add_field(key, value)

        logger.debug('Successfully generated FormData object')
        return form_data

    @staticmethod
    async def log_response_info(response: ClientResponse,
                                remove_sensitive_data: Optional[bool] = False):
        """Logs response info.

        This method extracts response status, headers and data

        :param response: Response object
        :type response: ClientResponse

        :param remove_sensitive_data: Boolean flag for censoring sensitive data
        :type remove_sensitive_data: Optional[bool]
        """
        logger.debug(f'Response status: {response.status}')
        logger.debug(f'Response headers: {response.headers}')
        if not remove_sensitive_data:
            logger.debug(f'Response data: {await response.text()}')
            return

        censored_response_data: Dict[str, Any] = await response.json()
        for key in censored_response_data.keys():
            if key in CENSORED_FIELDS:
                censored_response_data[key] = '[REDACTED]'

        logger.debug(f'Response data: {censored_response_data}')
