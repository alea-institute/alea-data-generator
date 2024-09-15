"""
Keyboard-related constants for generating typos in text data,
correcting typos in text data, or other representation or shift tasks.
"""

# imports
from typing import Dict, List, Tuple

# glissando here
PHYSICAL_LOWER_QWERTY_LAYOUT = [
    list("`1234567890-="),
    list("qwertyuiop[]\\"),
    list("asdfghjkl;'"),
    list("zxcvbnm,./"),
]

# capslock glissando here
PHYSICAL_UPPER_QWERTY_LAYOUT = [
    list("~!@#$%^&*()_+"),
    list("QWERTYUIOP{}|"),
    list('ASDFGHJKL:"'),
    list("ZXCVBNM<>?"),
]


# describe the physical layout of most keyboard fat-fingers or shift errors here
KEYBOARD_PAIRS: List[Tuple[str, str]] = [
    # Adjacent letter pairs (vertical)
    ("q", "a"),
    ("w", "s"),
    ("e", "d"),
    ("r", "f"),
    ("t", "g"),
    ("y", "h"),
    ("u", "j"),
    ("i", "k"),
    ("o", "l"),
    ("p", ";"),
    ("a", "z"),
    ("s", "x"),
    ("d", "c"),
    ("f", "v"),
    ("g", "b"),
    ("h", "n"),
    ("j", "m"),
    ("k", ","),
    ("l", "."),
    # Adjacent letter pairs (horizontal)
    ("q", "w"),
    ("w", "e"),
    ("e", "r"),
    ("r", "t"),
    ("t", "y"),
    ("y", "u"),
    ("u", "i"),
    ("i", "o"),
    ("o", "p"),
    ("a", "s"),
    ("s", "d"),
    ("d", "f"),
    ("f", "g"),
    ("g", "h"),
    ("h", "j"),
    ("j", "k"),
    ("k", "l"),
    ("z", "x"),
    ("x", "c"),
    ("c", "v"),
    ("v", "b"),
    ("b", "n"),
    ("n", "m"),
    ("m", ","),
    (",", "."),
    (".", "/"),
    # Number row mistakes
    ("1", "2"),
    ("2", "3"),
    ("3", "4"),
    ("4", "5"),
    ("5", "6"),
    ("6", "7"),
    ("7", "8"),
    ("8", "9"),
    ("9", "0"),
    ("0", "-"),
    # Special character mistakes
    ("p", "["),
    ("[", "]"),
    ("]", "\\"),
    ("l", ";"),
    (";", "'"),
    ("-", "="),
    # Shift key mistakes (capitalization errors)
    ("a", "A"),
    ("b", "B"),
    ("c", "C"),
    ("d", "D"),
    ("e", "E"),
    ("f", "F"),
    ("g", "G"),
    ("h", "H"),
    ("i", "I"),
    ("j", "J"),
    ("k", "K"),
    ("l", "L"),
    ("m", "M"),
    ("n", "N"),
    ("o", "O"),
    ("p", "P"),
    ("q", "Q"),
    ("r", "R"),
    ("s", "S"),
    ("t", "T"),
    ("u", "U"),
    ("v", "V"),
    ("w", "W"),
    ("x", "X"),
    ("y", "Y"),
    ("z", "Z"),
    # Number/symbol mistakes
    ("1", "!"),
    ("2", "@"),
    ("3", "#"),
    ("4", "$"),
    ("5", "%"),
    ("6", "^"),
    ("7", "&"),
    ("8", "*"),
    ("9", "("),
    ("0", ")"),
    ("`", "~"),
    ("-", "_"),
    ("=", "+"),
    ("[", "{"),
    ("]", "}"),
    ("\\", "|"),
    (";", ":"),
    ("'", '"'),
    (",", "<"),
    (".", ">"),
    ("/", "?"),
    # Space bar mistakes
    (" ", "n"),
    (" ", "b"),
    (" ", "v"),
    (" ", "c"),
    (" ", "x"),
    (" ", "m"),
]

# Create a reverse mapping for easy lookup
REVERSE_KEYBOARD_PAIRS: List[Tuple[str, str]] = [(b, a) for a, b in KEYBOARD_PAIRS]

# Combine both directions for a complete set of possible substitutions
ALL_KEYBOARD_PAIRS: Tuple[Tuple[str, str], ...] = tuple(
    KEYBOARD_PAIRS + REVERSE_KEYBOARD_PAIRS
)

# Translate this into a mapping from each character to a set of possible typos
KEY_ERROR_MAPPING: Dict[str, Tuple[str, ...]] = {
    a: tuple({b for a_, b in ALL_KEYBOARD_PAIRS if a_ == a})
    for a in set(a for a, _ in ALL_KEYBOARD_PAIRS)
}
