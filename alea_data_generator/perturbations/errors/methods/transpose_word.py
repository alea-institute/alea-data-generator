"""
Module that defines the transpose word error method.
"""

# imports
from typing import List


# local imports
from alea_data_generator.perturbations.errors.methods.base_word import (
    BaseWordErrorMethod,
)


class TransposeWordErrorMethod(BaseWordErrorMethod):
    """
    Error method that transposes adjacent words at specified positions.
    """

    def apply_error(self, words: List[str], positions: List[int]) -> str:
        """
        Apply the transpose word error to the specified positions in the input words.

        Args:
            words: List of words from the input string.
            positions: List of positions to apply the error.

        Returns:
            Modified string with transposed words.
        """
        result = words.copy()
        for i in reversed(positions):
            if i < len(words) - 1:
                result[i], result[i + 1] = result[i + 1], result[i]

        return " ".join(result)
