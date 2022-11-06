"""Enums for /api/animes/:anime_id/videos."""
from .enhanced_enum import EnhancedEnum


class VideoKind(EnhancedEnum):
    """Contains constants related for video kind."""
    PV = 'pv'
    CHARACTER_TRAILER = 'character_trailer'
    CM = 'cm'
    OP = 'op'
    ED = 'ed'
    OP_ED_CLIP = 'op_ed_clip'
    CLIP = 'clip'
    OTHER = 'other'
    EPISODE_PREVIEW = 'episode_preview'


class VideoHosting(EnhancedEnum):
    """Contains constants related for video hostings."""
    YOUTUBE = 'youtube'
    VK = 'vk'
    OK = 'ok'
    COUB = 'coub'
    RUTUBE = 'rutube'
    VIMEO = 'vimeo'
    SIBNET = 'sibnet'
    YANDEX = 'yandex'
    STREAMABLE = 'streamable'
    SMOTRET_ANIME = 'smotret_anime'
    MYVI = 'myvi'
    YOUMITE = 'youmite'
    VIULY = 'viuly'
    STORMO = 'stormo'
    MEDIAFIRE = 'mediafile'
