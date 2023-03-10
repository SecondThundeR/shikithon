"""Exception for raising on already running client."""

from loguru import logger


class AlreadyRunningClient(Exception):

    def __init__(self):
        error_message = 'Client is already running'
        logger.error(error_message)
        super().__init__(error_message)
