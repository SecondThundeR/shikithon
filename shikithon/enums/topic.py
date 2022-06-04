"""Enums for /api/topics."""
from enum import Enum


class TopicsType(Enum):
    """Contains constants related for getting certain type of topic."""
    REGULAR_TOPIC = 'Topic'
    CLUB_USER_TOPIC = 'Topics::ClubUserTopic'
    ENTRY_TOPIC = 'Topics::EntryTopic'
    NEWS_TOPIC = 'Topics::NewsTopic'


class EntryTopics(Enum):
    """Contains constants related for getting certain type of topic."""
    ANIME_TOPIC = 'Topics::EntryTopics::AnimeTopic'
    ARTICLE_TOPIC = 'Topics::EntryTopics::ArticleTopic'
    CHARACTER_TOPIC = 'Topics::EntryTopics::CharacterTopic'
    CLUB_PAGE_TOPIC = 'Topics::EntryTopics::ClubPageTopic'
    CLUB_TOPIC = 'Topics::EntryTopics::ClubTopic'
    COLLECTION_TOPIC = 'Topics::EntryTopics::CollectionTopic'
    CONTEST_TOPIC = 'Topics::EntryTopics::ContestTopic'
    COSPLAY_GALLERY_TOPIC = 'Topics::EntryTopics::CosplayGalleryTopic'
    MANGA_TOPIC = 'Topics::EntryTopics::MangaTopic'
    PERSON_TOPIC = 'Topics::EntryTopics::PersonTopic'
    RANOBE_TOPIC = 'Topics::EntryTopics::RanobeTopic'
    CRITIQUE_TOPIC = 'Topics::EntryTopics::CritiqueTopic'
    REVIEW_TOPIC = 'Topics::EntryTopics::ReviewTopic'


class NewsTopics(Enum):
    """Contains constants related for getting certain type of news topic."""
    CONTEST_STATUS_TOPIC = 'Topics::NewsTopics::ContestStatusTopic'


class ForumType(Enum):
    """Contains constants related for getting certain type of forum."""
    ALL = 'all'
    ANIMANGA = 'animanga'
    SITE = 'site'
    GAMES = 'games'
    VN = 'vn'
    CONTESTS = 'contests'
    OFFTOPIC = 'offtopic'
    CLUBS = 'clubs'
    MY_CLUBS = 'my_clubs'
    CRITIQUES = 'critiques'
    NEWS = 'news'
    COLLECTIONS = 'collections'
    ARTICLES = 'articles'
    COSPLAY = 'cosplay'


class TopicLinkedType(Enum):
    """Contains constants related for getting certain linked type of topic."""
    ANIME = 'Anime'
    MANGA = 'Manga'
    RANOBE = 'Ranobe'
    CHARACTER = 'Character'
    PERSON = 'Person'
    CLUB = 'Club'
    CLUB_PAGE = 'ClubPage'
    CRITIQUE = 'Critique'
    REVIEW = 'Review'
    CONTEST = 'Contest'
    COSPLAY_GALERY = 'CosplayGallery'
    COLLECTION = 'Collection'
    ARTICLE = 'Article'
