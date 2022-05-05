"""
Set of utility methods for the shikithon library.

This file contains the Utils class
with all the necessary utility methods
to work with the library
"""
from time import time
from enum import Enum
from typing import List
from typing import Dict
from typing import Union

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
        Convert query dict to query string for link.

        :param Dict[str, str] query_dict: Query dictionary
        :return: Query string
        :rtype: str
        """
        query_dict_str = "&".join(
            f"{key}={val}" for (key, val) in query_dict.items()
        )
        return f"?{query_dict_str}"

    @staticmethod
    def convert_app_name(app_name: str) -> str:
        """
        Converts app name to snake case for use in
        config cache filename.

        :param app_name: Current OAuth app name
        :return: Converted app name for filename
        :rtype: str
        """
        return "_".join(app_name.lower().split(" "))

    @staticmethod
    def get_new_expire_time(time_expire_constant: int) -> int:
        """
        Generates new token expire time.

        :param time_expire_constant: Token lifetime value
        :return: New token expire time
        :rtype: int
        """
        return int(time()) + time_expire_constant

    @staticmethod
    def generate_query_dict(
            **params_data: Union[str, bool, int, Enum, List[int], None]
    ) -> Dict[str, str]:
        """
        Returns valid query dict for API requests.

        This methods checks for data type and converts to valid one.

        :param Union[str, bool, int, Enum, List[int], None] params_data:
            API methods parameters data
        :return: Valid query dictionary
        :rtype: Dict[str, str]
        """
        new_query: Dict[str, str] = {}
        for key, data in params_data.items():
            if data is None:
                continue
            if isinstance(data, bool):
                if data is True:
                    new_query[key]= str(int(data))
                else:
                    continue
            elif isinstance(data, int):
                new_query[key] = str(data)
            elif isinstance(data, Enum):
                new_query[key] = data.value
            elif isinstance(data, list):
                data = [
                    str(value) if value.isdigit() else value for value in data
                ]
                new_query[key] = ",".join(data)
            else:
                new_query[key] = data
        return new_query

    @staticmethod
    def validate_query_number(
            query_number: Union[int, None],
            upper_limit: int
    ) -> Union[int, None]:
        """
        Validates query number.

        If number is not in range, returns lower limit number,
        otherwise number or None.

        :param Union[int, None] query_number: Number to validate
        :param int upper_limit: Upper limit for range check
        :return: Validated value
        :rtype: Union[int, None]
        """
        if query_number is None:
            return query_number
        if query_number < LOWER_LIMIT_NUMBER or query_number > upper_limit:
            return LOWER_LIMIT_NUMBER
        return query_number
