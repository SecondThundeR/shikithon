"""API resources for shikithon API class."""

from .abuse_requests import AbuseRequests
from .achievements import Achievements
from .animes import Animes
from .appears import Appears
from .bans import Bans
from .calendar import Calendar
from .characters import Characters
from .clubs import Clubs
from .comments import Comments
from .constants import Constants
from .dialogs import Dialogs
from .favorites import Favorites
from .forums import Forums
from .friends import Friends
from .genres import Genres
from .mangas import Mangas
from .messages import Messages
from .people import Person
from .publishers import Publishers
from .ranobes import Ranobes
from .stats import Stats
from .studios import Studios
from .styles import Styles
from .topics import Topics
from .user_images import UserImages
from .user_rates import UserRates
from .users import Users

__all__ = [
    'Achievements',
    'Animes',
    'Appears',
    'Bans',
    'Calendar',
    'Characters',
    'Clubs',
    'Comments',
    'Constants',
    'Dialogs',
    'Favorites',
    'Forums',
    'Friends',
    'Genres',
    'Mangas',
    'Messages',
    'Person',
    'Publishers',
    'Ranobes',
    'Stats',
    'Studios',
    'Styles',
    'Topics',
    'UserImages',
    'UserRates',
    'Users',
    'AbuseRequests',
]
