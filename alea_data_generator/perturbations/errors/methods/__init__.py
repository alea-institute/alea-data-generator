"""
This module contains the error methods that are used to generate errors in the text data.
"""

from .base import BaseErrorMethod
from .base_character import BaseCharacterErrorMethod
from .base_word import BaseWordErrorMethod
from .double_character import DoubleCharacterErrorMethod
from .double_word import DoubleWordErrorMethod
from .filter_character import FilterCharacterErrorMethod
from .hyphenate_word import HyphenateWordErrorMethod
from .keyboard_character import KeyboardCharacterErrorMethod
from .ocr_character import OCRCharacterErrorMethod
from .skip_character import SkipCharacterErrorMethod
from .skip_word import SkipWordErrorMethod
from .swap_character import SwapCharacterErrorMethod
from .transpose_character import TransposeCharacterErrorMethod
from .transpose_word import TransposeWordErrorMethod
from .whitespace_add import WhitespaceAddErrorMethod
from .whitespace_copy import WhitespaceCopyErrorMethod
from .whitespace_newline import WhitespaceNewlineErrorMethod
from .whitespace_remove import WhitespaceRemoveErrorMethod


__all__ = [
    "BaseErrorMethod",
    "BaseCharacterErrorMethod",
    "BaseWordErrorMethod",
    "DoubleCharacterErrorMethod",
    "DoubleWordErrorMethod",
    "FilterCharacterErrorMethod",
    "HyphenateWordErrorMethod",
    "KeyboardCharacterErrorMethod",
    "OCRCharacterErrorMethod",
    "SkipCharacterErrorMethod",
    "SkipWordErrorMethod",
    "SwapCharacterErrorMethod",
    "TransposeCharacterErrorMethod",
    "TransposeWordErrorMethod",
    "WhitespaceAddErrorMethod",
    "WhitespaceCopyErrorMethod",
    "WhitespaceNewlineErrorMethod",
    "WhitespaceRemoveErrorMethod",
]
