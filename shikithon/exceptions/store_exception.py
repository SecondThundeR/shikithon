"""Exception for raising on store method errors."""

from loguru import logger


class StoreException(Exception):

    def __init__(self, error_message: str):
        logger.error(error_message)
        super().__init__(error_message)
