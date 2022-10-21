"""Enums for shikithon API class."""

from shikithon.enums.anime import (
    AnimeCensorship,
    AnimeDuration,
    AnimeKind,
    AnimeList,
    AnimeOrder,
    AnimeRating,
    AnimeStatus,
)
from shikithon.enums.club import (
    CommentPolicy,
    ImageUploadPolicy,
    JoinPolicy,
    PagePolicy,
    TopicPolicy,
)
from shikithon.enums.comment import CommentableType
from shikithon.enums.favorite import FavoriteLinkedType
from shikithon.enums.history import TargetType
from shikithon.enums.manga import (
    MangaCensorship,
    MangaKind,
    MangaList,
    MangaOrder,
    MangaStatus,
)
from shikithon.enums.message import MessageType
from shikithon.enums.person import PersonKind
from shikithon.enums.ranobe import (
    RanobeCensorship,
    RanobeList,
    RanobeOrder,
    RanobeStatus,
)
from shikithon.enums.request import RequestType
from shikithon.enums.response import ResponseCode
from shikithon.enums.style import OwnerType
from shikithon.enums.topic import ForumType, TopicLinkedType, TopicType
from shikithon.enums.user_rate import (
    UserRateStatus,
    UserRateTarget,
    UserRateType,
)
from shikithon.enums.video import VideoKind

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
