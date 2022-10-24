"""
Config storing module.

This module handles saving API config to own file
to use on next object initializaion
"""

from json import dumps
from json import loads
from os import remove
from os.path import exists
from typing import Any, Dict, Optional, Tuple

from loguru import logger

from ..utils import Utils


class ConfigStore:
    """
    Config storing class.

    This class has several methods for
    saving/restoring config from a file.

    In addition, there is a method
    to check if config file is exists.

    On saving, class takes ".shikithon_" and
    combining with the current app_name
    for generating config file name.
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
        logger.debug('Generating config filename')
        return '.shikithon_' + Utils.convert_app_name_to_filename(app_name)

    @staticmethod
    def config_validation(app_name: str,
                          auth_code: str) -> Tuple[Dict[str, Any], bool]:
        """
        Gets stored config and validates it.

        :param app_name: Current app name
        :type app_name: str

        :param auth_code: Current authorization code
        :type auth_code: str

        :return: Tuple with config and validation status.
            On successful validation, returns stored config and True,
            otherwise, empty dictionary and False
        :rtype: Tuple[Dict[str, Any], bool]
        """
        store_config = ConfigStore.get_config(app_name)
        if store_config is None:
            logger.debug('There are no stored config')
            return {}, False

        logger.debug('Found stored config. Checking...')

        if auth_code and store_config['auth_code'] != auth_code:
            logger.debug('Mismatch of provided and stored auth codes. '
                         'Deleting old stored config')
            ConfigStore.delete_config(app_name)
            return {}, False

        logger.debug('Stored config is valid')
        return store_config, True

    @staticmethod
    def get_config(app_name: str) -> Optional[Dict[str, str]]:
        """
        Returns current config from file.

        :param app_name: App name for config load
        :type app_name: str

        :return: Config dictionary or None
        :rtype: Optional[Dict[str, str]]
        """
        config_name = ConfigStore.config_name(app_name)
        logger.debug(f'Getting "{config_name}" config')

        if exists(config_name):
            with open(config_name, 'r', encoding='utf-8') as config_file:
                config: Dict[str, str] = loads(config_file.read())
            return config

        logger.warning('Config file doesn\'t exist. Returning None')
        return None

    @staticmethod
    def save_config(config: Dict[str, str]) -> bool:
        """
        Creates new file and saves current config.

        :param config: Current config dictionary
        :type config: Dict[str, str]

        :return: True if save succeeded, False otherwise
        :rtype: bool
        """
        config_name = ConfigStore.config_name(config['app_name'])
        logger.debug(f'Saving config to "{config_name}"')

        try:
            with open(config_name, 'w', encoding='utf-8') as config_file:
                config_file.write(dumps(config, indent=4))
            return True
        except IOError as err:
            logger.warning(f'Couldn\'t save config to file: {err}')
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
        config_name = ConfigStore.config_name(app_name)
        logger.debug(f'Deleting config "{config_name}"')

        try:
            remove(config_name)
            return True
        except OSError as err:
            logger.warning(f"Couldn't delete config: {err}")
            return False
