"""Models for the Shikimori API."""

from shikithon.models.abuse_response import AbuseResponse
from shikithon.models.achievement import Achievement
from shikithon.models.anime import Anime
from shikithon.models.ban import Ban
from shikithon.models.calendar_event import CalendarEvent
from shikithon.models.character import Character
from shikithon.models.club import Club
from shikithon.models.club_image import ClubImage
from shikithon.models.comment import Comment
from shikithon.models.created_user_image import CreatedUserImage
from shikithon.models.creator import Creator
from shikithon.models.dialog import Dialog
from shikithon.models.favourites import Favourites
from shikithon.models.forum import Forum
from shikithon.models.franchise_tree import FranchiseTree
from shikithon.models.genre import Genre
from shikithon.models.history import History
from shikithon.models.link import Link
from shikithon.models.manga import Manga
from shikithon.models.message import Message
from shikithon.models.people import People
from shikithon.models.publisher import Publisher
from shikithon.models.ranobe import Ranobe
from shikithon.models.relation import Relation
from shikithon.models.screenshot import Screenshot
from shikithon.models.studio import Studio
from shikithon.models.style import Style
from shikithon.models.topic import Topic
from shikithon.models.unread_messages import UnreadMessages
from shikithon.models.user import User
from shikithon.models.user_list import UserList
from shikithon.models.user_rate import UserRate
from shikithon.models.video import Video

__all__ = [
    'Anime', 'Achievement', 'AbuseResponse', 'Ban', 'CalendarEvent',
    'Character', 'Club', 'ClubImage', 'Comment', 'CreatedUserImage', 'Creator',
    'Dialog', 'Favourites', 'Forum', 'FranchiseTree', 'Genre', 'History',
    'Link', 'Manga', 'Message', 'People', 'Publisher', 'Ranobe', 'Relation',
    'Screenshot', 'Studio', 'Style', 'Topic', 'UnreadMessages', 'User',
    'UserList', 'UserRate', 'Video'
]
__const__ = ['Anime']
