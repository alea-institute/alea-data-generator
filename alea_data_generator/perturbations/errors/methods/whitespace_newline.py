"""
Convert a space or tab to a newline character (\r, \n).
"""

import random

# imports
from typing import List

# project imports
from alea_data_generator.perturbations.errors.config import (
    ErrorConfig,
)
from alea_data_generator.perturbations.errors.methods.filter_character import (
    FilterCharacterErrorMethod,
)


class WhitespaceNewlineErrorMethod(FilterCharacterErrorMethod):
    """
    Error method that converts a space or tab to a newline character.
    """

    # override constructor to set lambda for filter_method to .isspace()
    def __init__(self, config: ErrorConfig):
        """
        Initialize the whitespace copy error method.

        Args:
            config: Error configuration.
        """
        super().__init__(config, filter_method=lambda x: x in (" ", "\t"))

    def apply_error(self, input_string: str, positions: List[int]) -> str:
        """
        Apply the whitespace error by replacing a space with a newline character.

        Args:
            input_string: Input string to apply errors to.
            positions: List of positions to apply the error.

        Returns:
            Modified string with newline whitespace characters.
        """
        return "".join(
            random.choice(("\r", "\n", "\r\n")) if i in positions else c
            for i, c in enumerate(input_string)
        )
