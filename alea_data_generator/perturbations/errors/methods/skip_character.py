"""
Skip character error method.
"""

# imports
from typing import List

# local imports
from alea_data_generator.perturbations.errors.methods.base_character import (
    BaseCharacterErrorMethod,
)


class SkipCharacterErrorMethod(BaseCharacterErrorMethod):
    """
    Error method that skips characters at specified positions.
    """

    def apply_error(self, input_string: str, positions: List[int]) -> str:
        """
        Apply the skip character error to the specified positions in the input string.

        Args:
            input_string: Input string to apply errors to.
            positions: List of positions to apply the error.

        Returns:
            Modified string with skipped characters.
        """
        return "".join(
            [char for i, char in enumerate(input_string) if i not in positions]
        )
