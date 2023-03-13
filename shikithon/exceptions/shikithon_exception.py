"""General exception for raising on other errors."""

from loguru import logger


class ShikithonException(Exception):

    def __init__(self, error_message: str):
        logger.error(error_message)
        super().__init__(error_message)
