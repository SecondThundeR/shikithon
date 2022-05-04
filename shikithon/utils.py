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
            **params_data: Dict[str, Union[int, Enum, List[int]]]
    ) -> Dict[str, str]:
        """
        Returns valid query dict for API requests.

        This methods checks for data type and converts to valid one.

        :param Dict[str, Union[int, Enum, List[int]]] params_data:
            API methods parameters data
        :return: Valid query dictionary
        :rtype: Dict[str, str]
        """
        new_query: Dict[str, str] = {}
        for key, data in params_data.items():
            if isinstance(data, int):
                new_query[key] = str(data)
            if isinstance(data, Enum):
                new_query[key] = data.value
            if isinstance(data, list):
                data = [
                    str(value) if value.isdigit() else value for value in data
                ]
                new_query[key] = ",".join(data)
        return new_query
