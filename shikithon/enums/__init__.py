"""Enums for shikithon API class."""

from .anime import (
    AnimeCensorship,
    AnimeDuration,
    AnimeKind,
    AnimeList,
    AnimeOrder,
    AnimeRating,
    AnimeStatus,
)
from .club import (
    CommentPolicy,
    ImageUploadPolicy,
    JoinPolicy,
    PagePolicy,
    TopicPolicy,
)
from .comment import CommentableType
from .favorite import FavoriteLinkedType
from .history import TargetType
from .manga import (
    MangaCensorship,
    MangaKind,
    MangaList,
    MangaOrder,
    MangaStatus,
)
from .message import MessageType
from .person import PersonKind
from .ranobe import RanobeCensorship, RanobeList, RanobeOrder, RanobeStatus
from .request import RequestType
from .response import ResponseCode
from .style import OwnerType
from .topic import ForumType, TopicLinkedType, TopicType
from .user_rate import UserRateStatus, UserRateTarget, UserRateType
from .video import VideoKind

__all__ = [
    'AnimeCensorship', 'AnimeDuration', 'AnimeKind', 'AnimeList', 'AnimeOrder',
    'AnimeRating', 'AnimeStatus', 'CommentPolicy', 'ImageUploadPolicy',
    'JoinPolicy', 'PagePolicy', 'TopicPolicy', 'CommentableType', 'TargetType',
    'FavoriteLinkedType', 'MangaCensorship', 'MangaKind', 'MangaList',
    'MangaOrder', 'MangaStatus', 'MessageType', 'PersonKind',
    'RanobeCensorship', 'RanobeList', 'RanobeOrder', 'RanobeStatus',
    'RequestType', 'ResponseCode', 'OwnerType', 'ForumType', 'TopicLinkedType',
    'TopicType', 'UserRateStatus', 'UserRateTarget', 'UserRateType', 'VideoKind'
]
