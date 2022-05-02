"""
Set of utility methods for the shikithon library.

This file contains the Utils class
with all the necessary utility methods
to work with the library
"""
from typing import Dict


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
        Api Test -> api_test

        :param app_name:
        :return: Converted app name for config cache filename
        :rtype: str
        """
        return "_".join(app_name.lower().split(" "))
