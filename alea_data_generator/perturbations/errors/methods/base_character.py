"""
Base class for character-level error methods.
"""

# pylint: disable=duplicate-code

# imports
from typing import List


# project
from alea_data_generator.perturbations.errors.config import ErrorConfig
from alea_data_generator.perturbations.errors.methods.base import BaseErrorMethod


class BaseCharacterErrorMethod(BaseErrorMethod):
    """
    Base class for character-level error methods.
    """

    def __init__(self, config: ErrorConfig):
        """
        Initialize the character-level error method.

        Args:
            config: Error configuration.
        """
        super().__init__(config)
        self.input_string: str = ""

    def get_indices(self) -> List[int]:
        """
        Get the indices of all characters in the input string.

        Returns:
            List of indices representing all characters.
        """
        return list(range(len(self.input_string)))

    def execute(self, input_string: str) -> str:
        """
        Execute the character-level error method on the input string.

        Args:
            input_string: Input string to apply errors to.

        Returns:
            Modified string with applied errors.
        """
        self.input_string = input_string
        positions = self.get_positions(len(input_string), input_string)
        return self.apply_error(input_string, positions)

    def apply_error(self, input_string: str, positions: List[int]) -> str:
        """
        Apply the character-level error to the specified positions in the input string.

        This method should be implemented by subclasses to define the specific error application.

        Args:
            input_string: Input string to apply errors to.
            positions: List of positions to apply the error.

        Returns:
            Modified string with applied errors.
        """
        raise NotImplementedError("Subclasses must implement the apply_error method.")
