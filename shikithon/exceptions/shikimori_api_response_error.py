"""Exception for raising if request response status is not lower than 400."""


class ShikimoriAPIResponseError(Exception):

    def __init__(self, method: str, status: int, url: str, text: str) -> None:
        super().__init__(f'{method} {status} {url}\n{text}')
