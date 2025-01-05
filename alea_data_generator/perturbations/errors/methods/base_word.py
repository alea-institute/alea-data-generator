"""
Base class for word-level error methods.
"""

# imports
from abc import abstractmethod
from typing import List

from alea_data_generator.perturbations.errors.config import ErrorConfig

# local imports
from alea_data_generator.perturbations.errors.methods.base import BaseErrorMethod


class BaseWordErrorMethod(BaseErrorMethod):
    """
    Base class for word-level error methods.
    """

    def __init__(self, config: ErrorConfig):
        """
        Initialize the word-level error method.

        Args:
            config: Error configuration.
        """
        super().__init__(config)
        self.input_string: str = ""

    def get_indices(self) -> List[int]:
        """
        Get the indices of all words in the input string.

        Returns:
            List of indices representing all words.
        """
        return list(range(len(self.input_string.split())))

    def execute(self, input_string: str) -> str:
        """
        Execute the word-level error method on the input string.

        Args:
            input_string: Input string to apply errors to.

        Returns:
            Modified string with applied errors.
        """
        self.input_string = input_string
        words = input_string.split()
        positions = self.get_positions(len(words), input_string)
        return self.apply_error(words, positions)

    @abstractmethod
    def apply_error(self, words: List[str], positions: List[int]) -> str:
        """
        Apply the word-level error to the specified positions in the input words.

        This method should be implemented by subclasses to define the specific error application.

        Args:
            words: List of words from the input string.
            positions: List of positions to apply the error.

        Returns:
            Modified string with applied errors.
        """
