"""Enums for shikithon API class."""

from .anime import (AnimeCensorship, AnimeDuration, AnimeKind, AnimeList,
                    AnimeOrder, AnimeRating, AnimeStatus, AnimeTopicKind)
from .club import (CommentPolicy, ImageUploadPolicy, JoinPolicy, PagePolicy,
                   TopicPolicy)
from .comment import CommentableCreateType, CommentableType
from .favorite import FavoriteLinkedType
from .history import HistoryTargetType
from .manga import (MangaCensorship, MangaKind, MangaList, MangaOrder,
                    MangaStatus)
from .message import MessageType
from .person import PersonKind, PersonSearchKind
from .ranobe import RanobeCensorship, RanobeList, RanobeOrder, RanobeStatus
from .request import RequestType
from .response import ResponseCode
from .review import ReviewOpinion
from .style import StyleOwner
from .topic import TopicForumType, TopicLinkedType, TopicType
from .user_rate import UserRateStatus, UserRateTarget, UserRateType
from .video import VideoKind

__all__ = [
    'AnimeCensorship', 'AnimeDuration', 'AnimeKind', 'AnimeTopicKind',
    'AnimeList', 'AnimeOrder', 'AnimeRating', 'AnimeStatus', 'CommentPolicy',
    'ImageUploadPolicy', 'JoinPolicy', 'PagePolicy', 'TopicPolicy',
    'CommentableType', 'CommentableCreateType', 'HistoryTargetType',
    'FavoriteLinkedType', 'MangaCensorship', 'MangaKind', 'MangaList',
    'MangaOrder', 'MangaStatus', 'MessageType', 'PersonKind',
    'PersonSearchKind', 'RanobeCensorship', 'RanobeList', 'RanobeOrder',
    'RanobeStatus', 'RequestType', 'ResponseCode', 'ReviewOpinion',
    'StyleOwner', 'TopicForumType', 'TopicLinkedType', 'TopicType',
    'UserRateStatus', 'UserRateTarget', 'UserRateType', 'VideoKind'
]
