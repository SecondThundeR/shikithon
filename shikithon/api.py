"""Shikithon API Module.

This is main module with a class
for interacting with the Shikimori API.
"""
from __future__ import annotations

import sys
from typing import Optional, TypeVar

from loguru import logger

from .base_client import Client
from .resources import AbuseRequests
from .resources import Achievements
from .resources import Animes
from .resources import Appears
from .resources import Bans
from .resources import Calendar
from .resources import Characters
from .resources import Clubs
from .resources import Comments
from .resources import Constants
from .resources import Dialogs
from .resources import Favorites
from .resources import Forums
from .resources import Friends
from .resources import Genres
from .resources import Mangas
from .resources import Messages
from .resources import People
from .resources import Publishers
from .resources import Ranobes
from .resources import Stats
from .resources import Studios
from .resources import Styles
from .resources import Topics
from .resources import UserImages
from .resources import UserRates
from .resources import Users
from .store import NullStore
from .store import Store

RT = TypeVar('RT')


class ShikimoriAPI(Client):
    """Main class for interacting with the API.

    Current API class uses base client for interacting with API.
    Also, all API methods splitted up to resources for convinient usage.
    """

    __slots__ = ('achievements', 'animes', 'appears', 'bans', 'calendar',
                 'characters', 'clubs', 'comments', 'constants', 'dialogs',
                 'favorites', 'forums', 'friends', 'genres', 'mangas',
                 'messages', 'people', 'publishers', 'ranobes', 'stats',
                 'studios', 'styles', 'topics', 'user_images', 'user_rates',
                 'users', 'abuse_requests')

    def __init__(self,
                 app_name: str = 'Api Test',
                 store: Store = NullStore(),
                 auto_close_store: bool = True,
                 logging: Optional[bool] = True):
        """Shikimori API class initialization.

        This magic method inits client and all resources
        for interacting with.

        :param app_name: OAuth App name
        :type app_name: str

        :param store: Class instance for store configs
        :type store: Optional[Store]

        :param auto_close_store: Auto close store option
        :type auto_close_store: bool

        :param logging: Logging flag
        :type logging: Optional[bool]
        """
        if logging:
            logger.configure(handlers=[
                {
                    'sink': sys.stderr,
                    'level': 'INFO',
                    'format': '{time} | {level} | {message}'
                },
                {
                    'sink': 'shikithon_{time}.log',
                    'level': 'DEBUG',
                    'format': '{time} | {level} | '
                              '{file}.{function}: {message}',
                    'rotation': '5 MB',
                    'compression': 'zip'
                },
            ])
        if not logging:
            logger.disable('shikithon')

        logger.info('Initializing API object')

        super().__init__(app_name, store, auto_close_store)

        self.achievements = Achievements(self)
        self.animes = Animes(self)
        self.appears = Appears(self)
        self.bans = Bans(self)
        self.calendar = Calendar(self)
        self.characters = Characters(self)
        self.clubs = Clubs(self)
        self.comments = Comments(self)
        self.constants = Constants(self)
        self.dialogs = Dialogs(self)
        self.favorites = Favorites(self)
        self.forums = Forums(self)
        self.friends = Friends(self)
        self.genres = Genres(self)
        self.mangas = Mangas(self)
        self.messages = Messages(self)
        self.people = People(self)
        self.publishers = Publishers(self)
        self.ranobes = Ranobes(self)
        self.stats = Stats(self)
        self.studios = Studios(self)
        self.styles = Styles(self)
        self.topics = Topics(self)
        self.user_images = UserImages(self)
        self.user_rates = UserRates(self)
        self.users = Users(self)
        self.abuse_requests = AbuseRequests(self)

        logger.info('Successfully initialized API object')
