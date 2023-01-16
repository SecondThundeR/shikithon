"""Exception for raising on invalid request response content type."""


class InvalidContentType(Exception):

    def __init__(self, content_type: str) -> None:
        super().__init__(f'Invalid response content type: {content_type}')
