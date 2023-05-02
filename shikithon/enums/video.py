"""Enums for `/api/animes/:anime_id/videos`."""
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
