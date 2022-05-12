"""
Config caching module.

This module handles saving API config to cache file
to restore on next object initializaion
"""

from json import dumps, loads
from os import remove
from os.path import exists
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
    def config_name(app_name: str) -> str:
        """
        Returns name of config file for selected app name.

        :param app_name: Selected OAuth app name
        :type app_name: str

        :return: Config filename
        :rtype: str
        """
        return '.shikithon_' + Utils.convert_app_name(app_name)

    @staticmethod
    def config_valid(app_name: str, auth_code: str) -> bool:
        """
        Check if current config is valid.

        This method checks for config existance and
        validity by checking authorization code.

        :param app_name: OAuth App name
        :type app_name: str

        :param auth_code: OAuth code
        :type auth_code: str

        :return: Result of check
        :rtype: bool
        """
        config: Dict[str, str] = ConfigCache.get_config(app_name)
        if not config:
            return False
        if not config['auth_code'] == auth_code:
            ConfigCache.delete_config(app_name)
            return False
        return True

    @staticmethod
    def get_config(app_name: str) -> Dict[str, str]:
        """
        Returns current config from cache file.

        :param app_name: App name for config load
        :type app_name: str

        :return: Config dictionary
        :rtype: Union[Dict[str, str], None]
        """
        if exists(ConfigCache.config_name(app_name)):
            with open(ConfigCache.config_name(app_name), 'r',
                      encoding='utf-8') as config_file:
                config: Dict[str, str] = loads(config_file.read())
            return config
        return {}

    @staticmethod
    def save_config(config: Dict[str, str]) -> bool:
        """
        Creates new cache file and saves current config.

        :param config: Current config dictionary
        :type config: Dict[str, str]

        :return: True if save succeeded, False otherwise
        :rtype: bool
        """
        try:
            with open(ConfigCache.config_name(config['app_name']),
                      'w',
                      encoding='utf-8') as config_file:
                config_file.write(dumps(config))
            return True
        except IOError as err:
            print(f"Couldn't save config to file: {err}")
            return False

    @staticmethod
    def delete_config(app_name: str) -> bool:
        """
        Deletes current config file.

        :param app_name: OAuth app name
        :type app_name: str

        :return: True if delete succeeded, False otherwise
        :rtype: bool
        """
        try:
            remove(ConfigCache.config_name(app_name))
            return True
        except OSError as err:
            print(f"Couldn't remove config: {err}")
            return False
