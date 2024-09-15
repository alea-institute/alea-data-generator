"""
Skip word error method.
"""

# imports
from typing import List

# local imports
from alea_data_generator.perturbations.errors.methods.base_word import (
    BaseWordErrorMethod,
)


class SkipWordErrorMethod(BaseWordErrorMethod):
    """
    Error method that skips words at specified positions.
    """

    def apply_error(self, words: List[str], positions: List[int]) -> str:
        """
        Apply the skip word error to the specified positions in the input words.

        Args:
            words: List of words from the input string.
            positions: List of positions to apply the error.

        Returns:
            Modified string with skipped words.
        """
        return " ".join([word for i, word in enumerate(words) if i not in positions])
