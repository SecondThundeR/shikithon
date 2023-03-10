"""Exception for raising on invalid request response content type."""

from loguru import logger


class InvalidContentType(Exception):

    def __init__(self, content_type: str):
        error_message = f'Invalid response content type: {content_type}'
        logger.error(error_message)
        super().__init__(error_message)
