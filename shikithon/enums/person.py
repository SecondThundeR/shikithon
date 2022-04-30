"""
Enums for /api/person.

Also Kind enum is use in /api/favorites,
when linked_type is Person
"""
from enum import Enum


class Kind(Enum):
    """Contains constants related for favorite kind."""
    NONE = ""
    COMMON = "common"
    SEYU = "seyu"
    MANGAKA = "mangaka"
    PRODUCER = "producer"
    PERSON = "person"
