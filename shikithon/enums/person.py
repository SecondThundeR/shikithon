"""Enums for `/api/person` and `/api/favorites`."""
from .enhanced_enum import EnhancedEnum


class PersonKind(EnhancedEnum):
    """Contains constants related for favorite person kind."""
    COMMON = 'common'
    SEYU = 'seyu'
    MANGAKA = 'mangaka'
    PRODUCER = 'producer'
    PERSON = 'person'


class PersonSearchKind(EnhancedEnum):
    """Contains constants related for search person kind."""
    SEYU = 'seyu'
    MANGAKA = 'mangaka'
    PRODUCER = 'producer'
