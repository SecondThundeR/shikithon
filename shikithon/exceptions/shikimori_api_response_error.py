"""Exception for raising if request response status is not lower than 400."""

from loguru import logger


class ShikimoriAPIResponseError(Exception):

    def __init__(self, method: str, status: int, url: str, text: str):
        error_message = f'{method} {status} {url}\n{text}'
        logger.error(error_message)
        super().__init__(error_message)
