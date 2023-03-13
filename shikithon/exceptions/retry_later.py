"""Exception for raising on too many requests."""

from loguru import logger


class RetryLater(Exception):

    def __init__(self, error_message: str):
        logger.warning(error_message)
        super().__init__(error_message)
