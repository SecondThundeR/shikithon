"""Exception for raising on store method erros."""


class StoreException(Exception):

    def __init__(self, error_message: str):
        super().__init__(error_message)
