"""
OCR-based character error method.
"""

# imports
from typing import List

# project
from alea_data_generator.data.constants.ocr import OCR_ERROR_MAPPING
from alea_data_generator.perturbations.errors.config import ErrorConfig
from alea_data_generator.perturbations.errors.methods.base_character import (
    BaseCharacterErrorMethod,
)


class OCRCharacterErrorMethod(BaseCharacterErrorMethod):
    """
    Error method that applies keyboard-based character substitutions.
    """

    def __init__(self, config: ErrorConfig):
        """
        Initialize the keyboard character error method.

        Args:
            config: Error configuration.
        """
        super().__init__(config)
        self.ocr_pairs = OCR_ERROR_MAPPING

    def apply_error(self, input_string: str, positions: List[int]) -> str:
        """
        Apply the keyboard character error to the specified positions in the input string.

        Args:
            input_string: Input string to apply errors to.
            positions: List of positions to apply the error.

        Returns:
            Modified string with keyboard-based character substitutions.
        """
        result = list(input_string)
        for i in positions:
            if input_string[i] in self.ocr_pairs:
                result[i] = self.rng.choice(self.ocr_pairs[input_string[i]])

        return "".join(result)
