"""Shikithon API Module.

This is main module with a class
for interacting with the Shikimori API.
"""
from __future__ import annotations

import sys
from typing import Dict, Union

from loguru import logger

from .base_client import Client
from .resources import (
    AbuseRequests,
    Achievements,
    Animes,
    Appears,
    Bans,
    Calendar,
    Characters,
    Clubs,
    Comments,
    Constants,
    Dialogs,
    Favorites,
    Forums,
    Friends,
    Genres,
    Mangas,
    Messages,
    Publishers,
    Ranobes,
    Stats,
    Studios,
    Styles,
    Topics,
    UserImages,
    UserRates,
    Users,
)
from .resources.people import People


class ShikimoriAPI:
    """
    Main class for interacting with the API.
    Current API class uses base client for interacting with API.
    Also, all API methods splitted up to resources for convinient usage.
    """

    def __init__(self, config: Union[str, Dict[str, str]]):
        """
        Shikimori API class initialization.

        This magic method inits client and all resources
        for interacting with.

        :param config: Config file for API class or app name
        :type config: Union[str, Dict[str, str]]
        """
        logger.configure(handlers=[
            {
                'sink': sys.stderr,
                'level': 'INFO',
                'format': '{time} | {level} | {message}'
            },
            {
                'sink': 'shikithon_{time}.log',
                'level': 'DEBUG',
                'format': '{time} | {level} | {file}.{function}: {message}',
                'rotation': '1 MB',
                'compression': 'zip'
            },
        ])
        logger.info('Initializing API object')

        self._client = Client(config)

        self.achievements = Achievements(self._client)
        self.animes = Animes(self._client)
        self.appears = Appears(self._client)
        self.bans = Bans(self._client)
        self.calendar = Calendar(self._client)
        self.characters = Characters(self._client)
        self.clubs = Clubs(self._client)
        self.comments = Comments(self._client)
        self.constants = Constants(self._client)
        self.dialogs = Dialogs(self._client)
        self.favorites = Favorites(self._client)
        self.forums = Forums(self._client)
        self.friends = Friends(self._client)
        self.genres = Genres(self._client)
        self.mangas = Mangas(self._client)
        self.messages = Messages(self._client)
        self.people = People(self._client)
        self.publishers = Publishers(self._client)
        self.ranobes = Ranobes(self._client)
        self.stats = Stats(self._client)
        self.studios = Studios(self._client)
        self.styles = Styles(self._client)
        self.topics = Topics(self._client)
        self.user_images = UserImages(self._client)
        self.user_rates = UserRates(self._client)
        self.users = Users(self._client)
        self.abuse_requests = AbuseRequests(self._client)

        logger.info('Successfully initialized API object')

    @property
    def closed(self) -> bool:
        """Check if client is closed."""
        return self._client.closed

    async def open(self) -> ShikimoriAPI:
        """Open client and return self."""
        await self._client.open()
        return self

    async def close(self) -> None:
        """Close client."""
        await self._client.close()

    async def __aenter__(self) -> ShikimoriAPI:
        """Async context manager entry point."""
        return await self.open()

    async def __aexit__(self, *args) -> None:
        """Async context manager exit point."""
        await self.close()
