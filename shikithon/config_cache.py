"""
Config caching module.

This module handles saving API config to cache file
to restore on next object initializaion
"""


from os.path import exists
from json import dumps
from json import loads
from typing import Dict

from shikithon.utils import Utils


class ConfigCache:
    """
    Config caching class.

    This class has several methods for
    saving/restoring config from a cache file.

    In addition, there is a method
    to check if config cache file is exists.

    On saving, class takes ".shikithon_" and
    combining with the current app_name
    for generating cache file name.
    This allows to use multiple configs without
    getting new authorization codes for old configs.

    This class was created due
    to the behavior of Shikithon OAuth when
    the server refuses to use the authentication code
    when there was a second attempt to get new access tokens,
    not refreshing them
    """
    @staticmethod
    def config_exists(app_name: str) -> bool:
        """
        Checks if cache config is exists.

        :param str app_name: Current app name
        :return: True if file exists, False otherwise
        :rtype: bool
        """
        config_file_name: str = ".shikithon_" + Utils.convert_app_name(
            app_name
        )
        return exists(config_file_name)

    @staticmethod
    def get_config(app_name: str) -> Dict[str, str]:
        """
        Returns current config from cache file.

        :param str app_name: App name for config load
        :return: Config dictionary
        :rtype: Dict[str, str]
        """
        config_file_name: str = ".shikithon_" + Utils.convert_app_name(
            app_name
        )
        with open(config_file_name, "r", encoding="utf-8") as config_file:
            config: Dict[str, str] = loads(config_file.read())
        return config

    @staticmethod
    def save_config(config: Dict[str, str]) -> bool:
        """
        Creates new cache file and saves current config.

        :param Dict[str, str] config: Current config dictionary
        :return: True if save succeeded, False otherwise
        :rtype: bool
        """
        try:
            config_file_name: str = ".shikithon_" + Utils.convert_app_name(
                config["app_name"]
            )
            with open(config_file_name, "w", encoding="utf-8") as config_file:
                config_file.write(dumps(config))
            return True
        except IOError as err:
            print(f"Couldn't save config to file: {err}")
            return False
