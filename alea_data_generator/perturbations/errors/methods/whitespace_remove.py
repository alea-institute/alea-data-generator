"""
Whitespace remove error method that removes whitespace characters.
"""

# imports
from typing import List

# project imports
from alea_data_generator.perturbations.errors.config import (
    ErrorConfig,
)
from alea_data_generator.perturbations.errors.methods.filter_character import (
    FilterCharacterErrorMethod,
)


class WhitespaceRemoveErrorMethod(FilterCharacterErrorMethod):
    """
    Error method that removes whitespace characters.
    """

    # override constructor to set lambda for filter_method to .isspace()
    def __init__(self, config: ErrorConfig):
        """
        Initialize the whitespace copy error method.

        Args:
            config: Error configuration.
        """
        super().__init__(config, filter_method=lambda x: x.isspace())

    def apply_error(self, input_string: str, positions: List[int]) -> str:
        """
        Apply the whitespace error by replacing whitespace with 2-5 copies.

        Args:
            input_string: Input string to apply errors to.
            positions: List of positions to apply the error.

        Returns:
            Modified string with duplicated whitespace characters.
        """
        # create a new string with duplicated whitespace characters
        new_string = input_string

        # process from right to avoid left offset changes
        for position in sorted(positions, reverse=True):
            # insert the copies
            new_string = new_string[:position] + new_string[position + 1 :]

        return new_string
