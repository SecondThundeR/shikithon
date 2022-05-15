"""
Enums for /api/person.

Also PersonKind enum is use in /api/favorites,
when linked_type is Person
"""
from enum import Enum


class PersonKind(Enum):
    """Contains constants related for favorite person kind."""
    NONE = ''
    COMMON = 'common'
    SEYU = 'seyu'
    MANGAKA = 'mangaka'
    PRODUCER = 'producer'
    PERSON = 'person'
