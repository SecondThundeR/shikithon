"""Enums for /api/clubs."""
from enum import Enum


class JoinPolicy(Enum):
    """Contains constants related for join policy setting."""
    FREE = 'free'
    MEMBER_INVITE = 'member_invite'
    ADMIN_INVITE = 'admin_invite'
    OWNER_INVITE = 'owner_invite'


class CommentPolicy(Enum):
    """Contains constants related for comment policy setting."""
    FREE = 'free'
    MEMBERS = 'members'
    ADMINS = 'admins'


class TopicPolicy(Enum):
    """Contains constants related for topic policy setting."""
    MEMBERS = 'members'
    ADMINS = 'admins'


class PagePolicy(Enum):
    """Contains constants related for page policy setting."""
    MEMBERS = 'members'
    ADMINS = 'admins'


class ImageUploadPolicy(Enum):
    """Contains constants related for image upload policy setting."""
    MEMBERS = 'members'
    ADMINS = 'admins'
