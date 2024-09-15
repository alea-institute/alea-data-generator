"""
Phonetic encoding is the representation of words or names by a code that is derived from the pronunciation of the word or name.
"""

# imports
import unicodedata
from enum import Enum
from typing import Dict, Tuple

# packages
import rapidfuzz.fuzz


class SoundexType(Enum):
    """
    Enum class for the different types of soundex encodings
    """

    SOUNDEX = "soundex"
    FUZZY_SOUNDEX = "fuzzy_soundex"
    REFINED_SOUNDEX = "refined_soundex"
    METAPHONE = "metaphone"
    DOUBLE_METAPHONE = "double_metaphone"


PHONETIC_LETTER_MAPPINGS: Dict[SoundexType, str] = {
    # mapping is translated value in A-Z order (26)
    #                     ABCDEFGHIJKLMNOPQRSTUVWXYZ
    SoundexType.SOUNDEX: "01230120022455012623010202",
    SoundexType.FUZZY_SOUNDEX: "01360240043788015936020202",
    SoundexType.REFINED_SOUNDEX: "01360240043788015936020202",
    SoundexType.METAPHONE: "AFHJKLMNPRSTWXY??B?CDEGIOUV",
}

PHONETIC_PAIR_MAPPINGS: Dict[SoundexType, Dict[str, str]] = {
    SoundexType.SOUNDEX: {
        "DG": "2",
        "GH": "2",
        "GN": "2",
        "KN": "2",
        "PH": "1",
        "MP": "5",
        "PS": "0",
        "PF": "1",
        "TCH": "6",
        "TS": "0",
    },
    SoundexType.FUZZY_SOUNDEX: {
        "CH": "8",
        "CB": "8",
        "CZ": "4",
        "DZ": "4",
        "TS": "4",
        "TZ": "4",
        "CS": "4",
        "KS": "4",
        "GN": "3",
        "KN": "3",
        "PH": "1",
        "PF": "1",
        "GH": "2",
        "SH": "9",
        "SCH": "9",
    },
    SoundexType.REFINED_SOUNDEX: {
        "CH": "8",
        "CB": "8",
        "CZ": "4",
        "DZ": "4",
        "TS": "4",
        "TZ": "4",
        "CS": "4",
        "KS": "4",
        "GN": "3",
        "KN": "3",
        "PH": "1",
        "PF": "1",
        "GH": "2",
        "SH": "9",
        "SCH": "9",
    },
    SoundexType.METAPHONE: {
        "KN": "N",
        "GN": "N",
        "PN": "N",
        "AE": "E",
        "WR": "R",
        "CK": "K",
        "PH": "F",
        "PF": "F",
        "GH": "F",
        "DG": "J",
        "MB": "M",
        "SCH": "SK",
        "TIO": "SH",
        "TIA": "SH",
        "TCH": "CH",
    },
}


class PhoneticEncoder:
    """
    Class to encode words using different phonetic algorithms.
    """

    @staticmethod
    def _apply_pair_mappings(word: str, soundex_type: SoundexType) -> str:
        """
        Apply pair mappings to the input word.

        Args:
            word: The input word to apply pair mappings to.
            soundex_type: The type of soundex encoding to use.

        Returns:
            The word with pair mappings applied.
        """
        for pair, replacement in PHONETIC_PAIR_MAPPINGS[soundex_type].items():
            word = word.replace(pair, replacement)
        return word

    @staticmethod
    def remove_diacritics(text: str) -> str:
        """
        Remove diacritical marks from the input text.

        Args:
            text: The input text containing diacritical marks.

        Returns:
            A string with diacritical marks removed.
        """
        # Normalize the text to decompose characters with diacritics
        normalized = unicodedata.normalize("NFKD", text)

        # Remove non-spacing marks (diacritics)
        return "".join(c for c in normalized if not unicodedata.combining(c))

    @staticmethod
    def _encode_letter(letter: str, soundex_type: SoundexType) -> str:
        """
        Encode a single letter using the specified soundex encoding.

        Args:
            letter: The letter to encode.

        Returns:
            The encoded letter.
        """
        if letter.isalpha():
            return PHONETIC_LETTER_MAPPINGS[soundex_type][
                ord(letter.upper()) - ord("A")
            ]
        return letter

    @classmethod
    def soundex(cls, word: str, length: int = 4) -> str:
        """
        Encode a word using the soundex algorithm.

        Args:
            word: The word to encode.
            length: The length of the output code.

        Returns:
            The soundex code for the input word.
        """
        if not word:
            return "0000"[:length]

        word = word.upper()
        word = cls._apply_pair_mappings(word, SoundexType.SOUNDEX)

        code = word[0]
        previous = cls._encode_letter(word[0], SoundexType.SOUNDEX)

        for letter in word[1:]:
            encoded = cls._encode_letter(letter, SoundexType.SOUNDEX)
            if encoded not in ("0", previous):
                code += encoded
                if len(code) == length:
                    break
            previous = encoded

        return (code + "0000")[:length]

    @classmethod
    def fuzzy_soundex(cls, word: str, length: int = 4) -> str:
        """
        Encode a word using the fuzzy soundex algorithm.

        Args:
            word: The word to encode.
            length: The length of the output code.

        Returns:
            The fuzzy soundex code for the input word.
        """
        if not word:
            return "0000"[:length]

        word = cls.remove_diacritics(word)
        word = word.upper()
        word = cls._apply_pair_mappings(word, SoundexType.FUZZY_SOUNDEX)

        code = word[0]
        for letter in word[1:]:
            encoded = cls._encode_letter(letter, SoundexType.FUZZY_SOUNDEX)
            if encoded != "0":
                code += encoded
                if len(code) == length:
                    break

        return (code + "0000")[:length]

    @classmethod
    def refined_soundex(cls, word: str) -> str:
        """
        Encode a word using the refined soundex algorithm.

        Args:
            word: The word to encode.

        Returns:
            The refined soundex code for the input word.
        """
        if not word:
            return ""

        word = cls.remove_diacritics(word)
        word = word.upper()
        word = cls._apply_pair_mappings(word, SoundexType.REFINED_SOUNDEX)

        code = word[0]
        for letter in word[1:]:
            encoded = cls._encode_letter(letter, SoundexType.REFINED_SOUNDEX)
            if (
                encoded != code[-1]
            ):  # only add if different from the last encoded character
                code += encoded

        return code

    # pylint: disable=too-many-branches, too-many-statements
    @classmethod
    def metaphone(cls, word: str, max_length: int = 4) -> str:
        """
        Encode a word using the metaphone algorithm.

        Args:
            word: The word to encode.
            max_length: The maximum length of the output code.

        Returns:
            The metaphone code for the input word.
        """
        if not word:
            return ""

        word = cls.remove_diacritics(word)
        word = word.upper()
        word = cls._apply_pair_mappings(word, SoundexType.METAPHONE)

        code = ""
        i = 0
        while i < len(word) and len(code) < max_length:
            c = word[i]

            if c in "AEIOU":
                if i == 0:
                    code += c
            elif c == "B":
                code += "B"
            elif c == "C":
                if i + 1 < len(word):
                    if word[i + 1] == "I" and i + 2 < len(word) and word[i + 2] == "A":
                        code += "X"
                    elif word[i + 1] in "EIY":
                        code += "S"
                    else:
                        code += "K"
                else:
                    code += "K"
            elif c == "D":
                if i + 2 < len(word) and word[i + 1] == "G" and word[i + 2] in "EIY":
                    code += "J"
                    i += 1
                else:
                    code += "T"
            elif c == "G":
                if i + 1 < len(word):
                    if word[i + 1] in "EIY":
                        code += "J"
                    else:
                        code += "K"
                else:
                    code += "K"
            elif c == "H":
                if i == 0 or word[i - 1] not in "CSPT":
                    if i + 1 < len(word) and word[i + 1] in "AEIOU":
                        code += "H"
            elif c == "K":
                if i == 0 or word[i - 1] != "C":
                    code += "K"
            elif c == "P":
                if i + 1 < len(word) and word[i + 1] == "H":
                    code += "F"
                    i += 1
                else:
                    code += "P"
            elif c == "Q":
                code += "K"
            elif c == "S":
                if i + 2 < len(word) and word[i + 1] == "I" and word[i + 2] in "AO":
                    code += "X"
                    i += 2
                else:
                    code += "S"
            elif c == "T":
                if i + 2 < len(word) and word[i + 1] == "I" and word[i + 2] in "AO":
                    code += "X"
                    i += 2
                elif i + 1 < len(word) and word[i + 1] == "H":
                    code += "0"
                    i += 1
                elif i + 2 < len(word) and word[i + 1] == "C" and word[i + 2] == "H":
                    code += "X"
                    i += 2
                else:
                    code += "T"
            elif c == "V":
                code += "F"
            elif c == "W":
                if i + 1 < len(word) and word[i + 1] in "AEIOU":
                    code += "W"
            elif c == "X":
                code += "KS"
            elif c == "Y":
                if i + 1 < len(word) and word[i + 1] in "AEIOU":
                    code += "Y"
            elif c == "Z":
                code += "S"
            elif c in "FJLMNR":
                code += c

            i += 1

        # Remove final 'S' if preceded by a consonant
        if len(code) > 1 and code[-1] == "S" and code[-2] not in "AEIOU":
            code = code[:-1]

        return code

    # pylint: disable=too-many-boolean-expressions
    @classmethod
    def double_metaphone(cls, word: str) -> Tuple[str, str]:
        """
        Encode a word using the double metaphone algorithm.

        Args:
            word: The word to encode.

        Returns:
            A tuple containing the primary and alternate metaphone codes for the input word.
        """

        word = cls.remove_diacritics(word)
        word = word.upper()
        length = len(word)
        index = 0
        metaph = ""
        alternate = ""
        current = ""
        alternate_current = ""

        def add_metaphone(primary: str, secondary: str = ""):
            nonlocal metaph, alternate, current, alternate_current
            if secondary == "":
                secondary = primary
            if current == "":
                metaph += primary
                alternate += secondary
            else:
                metaph += current
                alternate += alternate_current
            current = ""
            alternate_current = ""

        while index < length:
            c = word[index]

            if c in "AEIOU":
                if index == 0:
                    add_metaphone("A")
            elif c == "B":
                add_metaphone("P")
            elif c == "Ç":
                add_metaphone("S")
            elif c == "C":
                if (
                    index > 0
                    and word[index - 1] == "S"
                    and index + 1 < length
                    and word[index + 1] in "EIY"
                ):
                    index += 1
                elif index + 1 < length and word[index + 1] in "EIY":
                    add_metaphone("S")
                else:
                    add_metaphone("K")
            elif c == "D":
                if (
                    index + 2 < length
                    and word[index + 1] == "G"
                    and word[index + 2] in "EIY"
                ):
                    add_metaphone("J")
                    index += 2
                else:
                    add_metaphone("T")
            elif c == "F":
                add_metaphone("F")
            elif c == "G":
                if (index + 1 < length and word[index + 1] in "EIY") or (
                    index > 0
                    and word[index - 1] == "D"
                    and index + 1 < length
                    and word[index + 1] in "EIY"
                ):
                    add_metaphone("J", "K")
                else:
                    add_metaphone("K")
            elif c == "H":
                if (
                    (index == 0 or word[index - 1] in "AEIOU")
                    and index + 1 < length
                    and word[index + 1] in "AEIOU"
                ):
                    add_metaphone("H")
            elif c == "J":
                add_metaphone("J")
            elif c == "K":
                if index > 0 and word[index - 1] != "C":
                    add_metaphone("K")
            elif c == "L":
                add_metaphone("L")
            elif c == "M":
                add_metaphone("M")
            elif c == "N":
                add_metaphone("N")
            elif c == "Ñ":
                add_metaphone("N")
            elif c == "P":
                if index + 1 < length and word[index + 1] == "H":
                    add_metaphone("F")
                    index += 1
                else:
                    add_metaphone("P")
            elif c == "Q":
                add_metaphone("K")
            elif c == "R":
                add_metaphone("R")
            elif c == "S":
                if (
                    index + 2 < length
                    and word[index + 1] == "I"
                    and word[index + 2] in "AO"
                ):
                    add_metaphone("X")
                    index += 2
                else:
                    add_metaphone("S")
            elif c == "T":
                if (
                    index + 2 < length
                    and word[index + 1] == "I"
                    and word[index + 2] in "AO"
                ):
                    add_metaphone("X")
                    index += 2
                elif index + 1 < length and word[index + 1] == "H":
                    add_metaphone("0")
                    index += 1
                else:
                    add_metaphone("T")
            elif c == "V":
                add_metaphone("F")
            elif c == "W":
                if index + 1 < length and word[index + 1] in "AEIOU":
                    add_metaphone("W")
            elif c == "X":
                add_metaphone("KS")
            elif c == "Y":
                if index + 1 < length and word[index + 1] in "AEIOU":
                    add_metaphone("Y")
            elif c == "Z":
                add_metaphone("S")

            index += 1

        add_metaphone("")  # Add any remaining characters
        return metaph, alternate

    @staticmethod
    def ratio_float(a: str, b: str) -> float:
        """
        Calculate the partial ratio between two strings and return a float value between 0.0 and 1.0.

        Args:
            a: The first string to compare.
            b: The second string to compare.

        Returns:
            A float value between 0.0 and 1.0 representing the partial ratio between the two strings.
        """
        return max(0.0, min(rapidfuzz.fuzz.ratio(a, b) / 100.0, 100.0))

    @staticmethod
    def similarity_metric(a: str, b: str) -> float:
        """
        Calculate the Damerau-Levenshtein distance between two strings.

        Args:
            a: The first string to compare.
            b: The second string to compare.

        Returns:
            The Damerau-Levenshtein distance between the two strings.
        """
        return rapidfuzz.distance.DamerauLevenshtein.normalized_similarity(a, b)

    @classmethod
    def compare(cls, word1: str, word2: str) -> float:
        """
        Compare two words using a weighted average of different phonetic algorithms.

        Args:
            word1: The first word to compare.
            word2: The second word to compare.

        Returns:
            A weighted average of the similarity scores between the two words.
        """
        refined_soundex_score = cls.ratio_float(
            cls.refined_soundex(word1), cls.refined_soundex(word2)
        )
        dm1_primary, dm1_alternate = cls.double_metaphone(word1)
        dm2_primary, dm2_alternate = cls.double_metaphone(word2)
        double_metaphone_score = max(
            cls.ratio_float(dm1_primary, dm2_primary),
            cls.ratio_float(dm1_alternate, dm2_alternate),
        )

        # levenshtein directly
        levenshtein_score = cls.similarity_metric(word1, word2)

        # Calculate weighted average
        weighted_scores = (
            refined_soundex_score * 5 / 10.0
            + double_metaphone_score * 4 / 10.0
            + levenshtein_score * 1 / 10.0
        )

        return weighted_scores
