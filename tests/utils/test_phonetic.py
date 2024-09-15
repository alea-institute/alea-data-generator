import pytest

from alea_data_generator.utils.phonetic import PhoneticEncoder


@pytest.mark.parametrize(
    "word1, word2, should_match",
    [
        ("hello", "helo", True),
        ("world", "wurld", True),
        ("python", "pithon", True),
        ("test", "text", True),
        ("night", "knight", False),
        ("phone", "fone", False),
        ("xylophone", "zilofone", False),
        ("cat", "dog", False),
    ],
)
def test_soundex_matching(word1, word2, should_match):
    result1 = PhoneticEncoder.soundex(word1)
    result2 = PhoneticEncoder.soundex(word2)
    assert (result1 == result2) == should_match


@pytest.mark.parametrize(
    "word1, word2, should_match",
    [
        ("hello", "helo", False),
        ("world", "wurld", True),
        ("python", "pithon", True),
        ("test", "text", False),
        ("night", "knight", False),
        ("phone", "fone", False),
        ("xylophone", "zilofone", False),
        ("cat", "dog", False),
    ],
)
def test_fuzzy_soundex_matching(word1, word2, should_match):
    result1 = PhoneticEncoder.fuzzy_soundex(word1)
    result2 = PhoneticEncoder.fuzzy_soundex(word2)
    assert (result1 == result2) == should_match


@pytest.mark.parametrize(
    "word1, word2, should_match",
    [
        ("hello", "helo", True),
        ("world", "wurld", True),
        ("python", "pithon", True),
        ("test", "text", False),
        ("night", "knight", False),
        ("phone", "fone", False),
        ("xylophone", "zilofone", False),
        ("cat", "dog", False),
    ],
)
def test_refined_soundex_matching(word1, word2, should_match):
    result1 = PhoneticEncoder.refined_soundex(word1)
    result2 = PhoneticEncoder.refined_soundex(word2)
    assert (result1 == result2) == should_match


@pytest.mark.parametrize(
    "word1, word2, should_match",
    [
        ("hello", "helo", False),
        ("world", "wurld", True),
        ("python", "pithon", True),
        ("test", "text", False),
        ("night", "knight", True),
        ("phone", "fone", True),
        ("xylophone", "zilofone", False),
        ("cat", "dog", False),
    ],
)
def test_metaphone_matching(word1, word2, should_match):
    result1 = PhoneticEncoder.metaphone(word1)
    result2 = PhoneticEncoder.metaphone(word2)
    assert (result1 == result2) == should_match


@pytest.mark.parametrize(
    "word1, word2, should_match",
    [
        ("hello", "helo", False),
        ("world", "wurld", True),
        ("python", "pithon", True),
        ("test", "text", False),
        ("night", "knight", True),
        ("phone", "fone", True),
        ("xylophone", "zilofone", False),
        ("cat", "dog", False),
    ],
)
def test_double_metaphone_matching(word1, word2, should_match):
    result1 = PhoneticEncoder.double_metaphone(word1)
    result2 = PhoneticEncoder.double_metaphone(word2)
    assert (result1[0] == result2[0] or result1[1] == result2[1]) == should_match


@pytest.mark.parametrize(
    "word1, word2, min_similarity",
    [
        ("hello", "helo", 0.8),
        ("world", "wurld", 0.7),
        ("python", "pithon", 0.7),
        ("test", "text", 0.5),
        ("night", "knight", 0.7),
        ("phone", "fone", 0.7),
        ("xylophone", "zilofone", 0.6),
        ("cat", "dog", 0.1),
    ],
)
def test_compare(word1, word2, min_similarity):
    similarity = PhoneticEncoder.compare(word1, word2)
    assert similarity >= min_similarity


def test_remove_diacritics():
    assert PhoneticEncoder.remove_diacritics("héllö") == "hello"
    assert PhoneticEncoder.remove_diacritics("çafé") == "cafe"
    assert PhoneticEncoder.remove_diacritics("naïve") == "naive"


@pytest.mark.parametrize(
    "word1, word2, min_ratio",
    [
        ("hello", "helo", 0.8),
        ("world", "wurld", 0.7),
        ("python", "pithon", 0.7),
        ("test", "text", 0.5),
    ],
)
def test_ratio_float(word1, word2, min_ratio):
    ratio = PhoneticEncoder.ratio_float(word1, word2)
    assert ratio >= min_ratio


@pytest.mark.parametrize(
    "word1, word2, min_similarity",
    [
        ("hello", "helo", 0.8),
        ("world", "wurld", 0.7),
        ("python", "pithon", 0.7),
        ("test", "text", 0.5),
    ],
)
def test_similarity_metric(word1, word2, min_similarity):
    similarity = PhoneticEncoder.similarity_metric(word1, word2)
    assert similarity >= min_similarity
