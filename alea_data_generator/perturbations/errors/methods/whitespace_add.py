"""
Add whitespace at random positions in the input string.
"""

import random

# imports
from typing import List


# local imports
from alea_data_generator.perturbations.errors.methods.base_character import (
    BaseCharacterErrorMethod,
)


class WhitespaceAddErrorMethod(BaseCharacterErrorMethod):
    """
    Error method that adds random whitespace characters.
    """

    VALID_WHITESPACE = [" ", "\t", "\n", "\r"]

    def apply_error(self, input_string: str, positions: List[int]) -> str:
        """
        Apply the whitespace error by adding whitespace characters.

        Args:
            input_string: Input string to apply errors to.
            positions: List of positions to apply the error.

        Returns:
            Modified string with added whitespace characters.
        """
        # create a new string with doubled characters
        new_string = input_string

        # process positions in reverse to avoid offset
        for position in sorted(positions, reverse=True):
            # new char from whitespace list
            new_char = random.choice(self.VALID_WHITESPACE)

            # insert the character
            new_string = new_string[:position] + new_char + new_string[position:]

        return new_string
