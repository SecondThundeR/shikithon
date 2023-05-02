"""Special module, which adds some functionality to enum class."""
from enum import Enum


class EnhancedEnum(Enum):
    """Enhanced enum class.

    Adds support for `__str__` for getting enum value
    when casting to string or using in f-string, etc.
    """

    def __str__(self):
        return self.value
