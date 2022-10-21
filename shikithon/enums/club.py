"""Enums for /api/clubs."""
from .enhanced_enum import EnhancedEnum


class JoinPolicy(EnhancedEnum):
    """Contains constants related for join policy setting."""
    FREE = 'free'
    MEMBER_INVITE = 'member_invite'
    ADMIN_INVITE = 'admin_invite'
    OWNER_INVITE = 'owner_invite'


class CommentPolicy(EnhancedEnum):
    """Contains constants related for comment policy setting."""
    FREE = 'free'
    MEMBERS = 'members'
    ADMINS = 'admins'


class TopicPolicy(EnhancedEnum):
    """Contains constants related for topic policy setting."""
    MEMBERS = 'members'
    ADMINS = 'admins'


class PagePolicy(EnhancedEnum):
    """Contains constants related for page policy setting."""
    MEMBERS = 'members'
    ADMINS = 'admins'


class ImageUploadPolicy(EnhancedEnum):
    """Contains constants related for image upload policy setting."""
    MEMBERS = 'members'
    ADMINS = 'admins'
