"""
Double word error method.
"""

# imports
from typing import List


# local imports
from alea_data_generator.perturbations.errors.methods.base_word import (
    BaseWordErrorMethod,
)


class DoubleWordErrorMethod(BaseWordErrorMethod):
    """
    Error method that doubles words at specified positions.
    """

    def apply_error(self, words: List[str], positions: List[int]) -> str:
        """
        Apply the double word error to the specified positions in the input words.

        Args:
            words: List of words from the input string.
            positions: List of positions to apply the error.

        Returns:
            Modified string with doubled words.
        """
        result = []
        for i, word in enumerate(words):
            result.append(word)
            if i in positions:
                result.append(word)
        return " ".join(result)
