"""Special module, which adds some functionality to enum class."""
from enum import Enum
from typing import List


class EnhancedEnum(Enum):
    """
    Enhanced enum class, which adds methods for getting enum name and values.
    Used in enum validator method in utils.py.

    This helps to get rid of parameters that require an enum pass.
    Now user can pass simple strings, which will then be compared
    with the values of the required enum.
    """

    @classmethod
    def get_name(cls) -> str:
        """Returns name of the enum."""
        return cls.__name__

    @classmethod
    def get_values(cls) -> List[str]:
        """Returns values of the enum."""
        return list(map(lambda c: c.value, cls))
