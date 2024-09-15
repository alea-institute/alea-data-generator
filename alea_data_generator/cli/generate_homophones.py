"""
Generate homophones from a wordlist.
"""

# imports
import argparse
import json
import sys
from pathlib import Path
from typing import Optional

# packages
import tqdm

from alea_data_generator.utils.phonetic import PhoneticEncoder


def is_exception(word1: str, word2: str) -> bool:
    """
    Determine whether the pair is in the exception/false positive list.

    Args:
        word1 (str): First word.
        word2 (str): Second word.

    Returns:
        bool: Whether the pair is in the exception list.
    """

    if word1.replace("'", "").rstrip("s") == word2.replace("'", "").rstrip("s"):
        return True

    return False


def compare_words(
    word: str, prior_word: str, threshold: float
) -> Optional[tuple[str, str, float]]:
    """
    Compare two words and return a tuple if they are homophones.

    Args:
        word (str): Current word.
        prior_word (str): Previous word to compare.
        threshold (float): Threshold for phonetic similarity.

    Returns:
        Optional[tuple[str, str, float]]: Tuple of words and similarity if they are homophones, None otherwise.
    """
    if is_exception(word, prior_word):
        return None

    # skip unless the first three characters the same under soundex
    if PhoneticEncoder.similarity_metric(word[:4], prior_word[:4]) < 0.5:
        return None

    if (
        PhoneticEncoder.ratio_float(
            PhoneticEncoder.fuzzy_soundex(word),
            PhoneticEncoder.fuzzy_soundex(prior_word),
        )
        < 0.75
    ):
        return None

    try:
        similarity = PhoneticEncoder.compare(word, prior_word)
        if similarity > threshold:
            return word, prior_word, similarity
    except Exception as e:  # pylint: disable=broad-except
        print(f"Error comparing {word} and {prior_word}: {e}")

    return None


def main(wordlist_path: Path, threshold: float = 0.8) -> list[tuple[str, str, float]]:
    """
    Generate homophones from a wordlist.

    Args:
        wordlist_path (Path): Path to the wordlist.
        threshold (float): Threshold for phonetic similarity.
        max_workers (int): Maximum number of concurrent workers.

    Returns:
        list[tuple[str, str, float]]: List of homophones
    """
    words: list[str] = []
    results: list[tuple[str, str, float]] = []

    with open(wordlist_path, "rt", encoding="utf-8") as input_file:
        lines = tqdm.tqdm(input_file.read().splitlines())
        try:
            for word in lines:
                # submit the tasks and then collect them in whatever order with as_completed
                results.extend(
                    filter(
                        None,
                        [
                            compare_words(word, prior_word, threshold)
                            for prior_word in words
                        ],
                    )
                )
                # add the word and update the counts
                words.append(word)
                lines.set_postfix({"words": len(words), "results": len(results)})
        except KeyboardInterrupt:
            print("Interrupted at user request; returning partial results...")

    # return all results in alpha-sorted order for trie construction
    return results


def get_default_word_path() -> Optional[Path]:
    """
    Get the default wordlist path based on the platform info.

    Returns:
        Path to the wordlist
    """
    # check platform
    if Path("/usr/share/dict/words").exists():
        return Path("/usr/share/dict/words")

    return None


if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser(description="Generate homophones from a wordlist.")
    parser.add_argument(
        "--wordlist_path", type=Path, help="Path to the wordlist.", default=None
    )
    parser.add_argument(
        "--output_path",
        type=Path,
        help="Path to the output file.",
        default=Path("homophones.json"),
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.8,
        help="Threshold for phonetic similarity.",
    )
    args = parser.parse_args()

    # check that you're running on a platform that supports this
    wordlist_path_arg = args.wordlist_path or get_default_word_path()
    if wordlist_path_arg is None:
        print(
            "Unable to find a wordlist on this platform. Please provide a wordlist path and check that it exists."
        )
        sys.exit(1)

    # generate homophones
    homophones = main(wordlist_path_arg, args.threshold)

    # write homophones to file
    with open(args.output_path, "wt", encoding="utf-8") as output_file:
        json.dump(homophones, output_file, indent=2)
