"""
OCR-related constants for handling common OCR character recognition mistakes,
correcting OCR errors in text data, or other OCR-related tasks.
"""

# imports
from typing import Dict, List, Tuple

# common OCR character confusion pairs
OCR_PAIRS: List[Tuple[str, str]] = [
    # Number-like characters
    ("0", "D"),
    ("0", "O"),
    ("0", "Q"),
    ("0", "o"),
    ("0", "q"),
    ("1", "!"),
    ("1", "I"),
    ("1", "L"),
    ("1", "l"),
    ("1", "|"),
    ("1", "/"),
    ("1", "\\"),
    ("2", "Z"),
    ("2", "z"),
    ("3", "8"),
    ("4", "A"),
    ("5", "S"),
    ("5", "s"),
    ("6", "b"),
    ("7", "T"),
    ("7", "F"),
    ("8", "&"),
    ("8", "3"),
    ("8", "B"),
    ("9", "g"),
    ("9", "O"),
    ("9", "o"),
    ("9", "q"),
    # Uppercase letters with similar shapes
    ("A", "4"),
    ("B", "8"),
    ("C", "("),
    ("C", "c"),
    ("D", "0"),
    ("D", "O"),
    ("E", "c"),
    ("E", "o"),
    ("F", "t"),
    ("F", "+"),
    ("G", "9"),
    ("G", "q"),
    ("H", "#"),
    ("I", "!"),
    ("I", "1"),
    ("I", "l"),
    ("I", "|"),
    ("J", "i"),
    ("J", "l"),
    ("K", "k"),
    ("K", "x"),
    ("L", "1"),
    ("L", "I"),
    ("L", "l"),
    ("M", "m"),
    ("M", "n"),
    ("M", "r"),
    ("N", "h"),
    ("N", "m"),
    ("N", "n"),
    ("N", "r"),
    ("O", "0"),
    ("O", "Q"),
    ("O", "@"),
    ("O", "o"),
    ("O", "q"),
    ("P", "p"),
    ("P", "q"),
    ("Q", "0"),
    ("Q", "O"),
    ("Q", "g"),
    ("Q", "o"),
    ("Q", "q"),
    ("R", "h"),
    ("R", "m"),
    ("R", "n"),
    ("R", "r"),
    ("S", "$"),
    ("S", "5"),
    ("S", "s"),
    ("T", "7"),
    ("T", "f"),
    ("U", "u"),
    ("U", "v"),
    ("V", "U"),
    ("V", "v"),
    ("V", "w"),
    ("V", "y"),
    ("W", "w"),
    ("W", "v"),
    ("X", "%"),
    ("X", "x"),
    ("Y", "y"),
    ("Y", "v"),
    ("Z", "2"),
    ("Z", "z"),
    # Lowercase letters with similar shapes
    ("a", "@"),
    ("a", "e"),
    ("a", "o"),
    ("b", "6"),
    ("b", "h"),
    ("c", "("),
    ("c", "C"),
    ("c", "e"),
    ("c", "o"),
    ("d", "b"),
    ("d", "h"),
    ("d", "o"),
    ("e", "c"),
    ("e", "o"),
    ("f", "t"),
    ("f", "+"),
    ("g", "9"),
    ("g", "q"),
    ("h", "b"),
    ("h", "n"),
    ("h", "r"),
    ("i", "I"),
    ("i", "j"),
    ("i", "l"),
    ("i", "|"),
    ("j", "i"),
    ("j", "l"),
    ("k", "K"),
    ("k", "x"),
    ("l", "!"),
    ("l", "1"),
    ("l", "I"),
    ("l", "|"),
    ("m", "n"),
    ("m", "r"),
    ("m", "w"),
    ("n", "h"),
    ("n", "m"),
    ("n", "r"),
    ("o", "0"),
    ("o", "O"),
    ("o", "c"),
    ("o", "e"),
    ("o", "q"),
    ("p", "P"),
    ("p", "q"),
    ("q", "9"),
    ("q", "g"),
    ("q", "o"),
    ("q", "p"),
    ("r", "h"),
    ("r", "m"),
    ("r", "n"),
    ("s", "$"),
    ("s", "5"),
    ("s", "S"),
    ("t", "+"),
    ("t", "f"),
    ("u", "v"),
    ("v", "u"),
    ("v", "w"),
    ("v", "y"),
    ("w", "m"),
    ("w", "v"),
    ("x", "%"),
    ("x", "*"),
    ("x", "X"),
    ("y", "v"),
    ("z", "2"),
    ("z", "Z"),
    # Special characters with similar shapes
    ("!", "1"),
    ("!", "I"),
    ("!", "l"),
    ("!", "|"),
    ('"', "'"),
    ("#", "H"),
    ("$", "S"),
    ("$", "s"),
    ("%", "X"),
    ("%", "x"),
    ("&", "8"),
    ("'", '"'),
    ("'", "`"),
    ("(", "C"),
    ("(", "c"),
    ("(", "{"),
    ("(", "["),
    (")", "]"),
    (")", "}"),
    ("*", "x"),
    ("+", "t"),
    ("+", "f"),
    (",", "."),
    ("-", "="),
    ("-", "_"),
    ("-", "~"),
    (".", ","),
    ("/", "\\"),
    ("/", "1"),
    (":", ";"),
    (";", ":"),
    ("=", "-"),
    ("@", "a"),
    ("@", "O"),
    ("@", "o"),
    ("[", "("),
    ("]", ")"),
    ("\\", "/"),
    ("\\", "1"),
    ("{", "("),
    ("}", ")"),
    ("|", "!"),
    ("|", "1"),
    ("|", "I"),
    ("|", "l"),
    ("~", "-"),
]

# Create a reverse mapping
REVERSE_OCR_PAIRS: List[Tuple[str, str]] = [(b, a) for a, b in OCR_PAIRS]

# Combine both directions for a complete set of possible substitutions
ALL_OCR_PAIRS: Tuple[Tuple[str, str], ...] = tuple(OCR_PAIRS + REVERSE_OCR_PAIRS)

# Map each character to its possible OCR mistakes
OCR_ERROR_MAPPING: Dict[str, Tuple[str, ...]] = {
    a: tuple({b for a_, b in ALL_OCR_PAIRS if a_ == a})
    for a in set(a for a, _ in ALL_OCR_PAIRS)
}