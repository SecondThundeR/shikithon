"""Enums for /api/clubs."""
from enum import Enum


class CommentPolicy(Enum):
    """Contains constants related for comment policy setting."""
    FREE = 'free'
    MEMBERS = 'members'
    ADMINS = 'admins'


class TopicPolicy(Enum):
    """Contains constants related for topic policy setting."""
    MEMBERS = 'members'
    ADMINS = 'admins'


class ImageUploadPolicy(Enum):
    """Contains constants related for image upload policy setting."""
    MEMBERS = 'members'
    ADMINS = 'admins'
