"""
Set of utility methods for the shikithon library.

This file contains the Utils class
with all the necessary utility methods
to work with the library
"""
from typing import Any, Dict, List, Optional, Type, Union

from loguru import logger

from ..enums import ResponseCode


class Utils:
    """
    Utils class.

    Contains all the necessary utility methods
    to work with the library
    """

    @staticmethod
    def validate_response_data(
        response_data: Union[List[Dict[str, Any]], Dict[str, Any], List[Any],
                             int],
        data_model: Optional[Type[Any]] = None,
        response_code: Optional[ResponseCode] = None,
        fallback: Optional[Any] = None
    ) -> Optional[Union[Type[Any], List[Type[Any]], List[Any], Dict[str, Any],
                        bool]]:
        """Validates passed response data and returns parsed models.

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
