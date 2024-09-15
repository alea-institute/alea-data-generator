"""
Module for the transpose character error method.
"""

# imports
from typing import List

# local imports
from alea_data_generator.perturbations.errors.methods.base_character import (
    BaseCharacterErrorMethod,
)


class TransposeCharacterErrorMethod(BaseCharacterErrorMethod):
    """
    Error method that transposes adjacent characters at specified positions.
    """

    def apply_error(self, input_string: str, positions: List[int]) -> str:
        """
        Apply the transpose character error to the specified positions in the input string.

        Args:
            input_string: Input string to apply errors to.
            positions: List of positions to apply the error.

        Returns:
            Modified string with transposed characters.
        """
        result = list(input_string)
        for i in reversed(positions):
            if i < len(input_string) - 1:
                result[i], result[i + 1] = result[i + 1], result[i]

        return "".join(result)
