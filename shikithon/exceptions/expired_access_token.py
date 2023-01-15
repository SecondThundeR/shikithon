"""Exception for raising on access token expiration."""
from typing import Any, Dict


class ExpiredAccessToken(Exception):

    def __init__(self, token_data: Dict[str, Any]):
        super().__init__(f"Tokens aren't refreshed: {token_data}.")
