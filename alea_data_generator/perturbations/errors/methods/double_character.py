"""
Double character error method.
"""

# imports
from typing import List


# local imports
from alea_data_generator.perturbations.errors.methods.base_character import (
    BaseCharacterErrorMethod,
)


class DoubleCharacterErrorMethod(BaseCharacterErrorMethod):
    """
    Error method that doubles characters at specified positions.
    """

    def apply_error(self, input_string: str, positions: List[int]) -> str:
        """
        Apply the double character error to the specified positions in the input string.

        Args:
            input_string: Input string to apply errors to.
            positions: List of positions to apply the error.

        Returns:
            Modified string with doubled characters.
        """
        return "".join(
            [
                char * 2 if i in positions else char
                for i, char in enumerate(input_string)
            ]
        )
