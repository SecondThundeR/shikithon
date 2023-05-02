"""Enums for `/api/reviews`."""
from .enhanced_enum import EnhancedEnum


class ReviewOpinion(EnhancedEnum):
    """Contains constants related for review opinion type."""
    POSITIVE = 'positive'
    NEUTRAL = 'neutral'
    NEGATIVE = 'negative'
