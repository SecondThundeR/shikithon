"""Base class for API resources."""
from ..base_client import Client


class BaseResource:

    def __init__(self, client: Client):
        self._client = client
