import pytest

from alea_data_generator.perturbations.errors.config import ErrorConfig, ErrorSampleType
from alea_data_generator.perturbations.errors.methods.double_word import (
    DoubleWordErrorMethod,
)
from alea_data_generator.perturbations.errors.methods.skip_word import (
    SkipWordErrorMethod,
)
from alea_data_generator.perturbations.errors.methods.transpose_word import (
    TransposeWordErrorMethod,
)


@pytest.fixture
def error_config() -> ErrorConfig:
    return ErrorConfig(
        error_sample_type=ErrorSampleType.FIXED_COUNT,
        distribution_kwargs={"count": 2},
        seed=42,
    )


def test_double_word_method(error_config: ErrorConfig) -> None:
    method = DoubleWordErrorMethod(error_config)
    input_string = "the quick brown fox"
    result = method.execute(input_string)
    assert len(result.split()) == len(input_string.split()) + 2
    assert result != input_string


def test_skip_word_method(error_config: ErrorConfig) -> None:
    method = SkipWordErrorMethod(error_config)
    input_string = "the quick brown fox"
    result = method.execute(input_string)
    assert len(result.split()) == len(input_string.split()) - 2
    assert result != input_string


def test_transpose_word_method(error_config: ErrorConfig) -> None:
    method = TransposeWordErrorMethod(error_config)
    input_string = "the quick brown fox"
    result = method.execute(input_string)
    assert len(result.split()) == len(input_string.split())
    assert result != input_string


def test_double_word_specific_positions() -> None:
    config = ErrorConfig(
        error_sample_type=ErrorSampleType.FIXED_COUNT,
        distribution_kwargs={"count": 2},
        seed=42,
    )
    method = DoubleWordErrorMethod(config)
    words = ["the", "quick", "brown", "fox"]
    result = method.apply_error(words, [1, 3])
    assert result == "the quick quick brown fox fox"


def test_skip_word_specific_positions() -> None:
    config = ErrorConfig(
        error_sample_type=ErrorSampleType.FIXED_COUNT,
        distribution_kwargs={"count": 2},
        seed=42,
    )
    method = SkipWordErrorMethod(config)
    words = ["the", "quick", "brown", "fox"]
    result = method.apply_error(words, [1, 3])
    assert result == "the brown"


def test_transpose_word_specific_positions() -> None:
    config = ErrorConfig(
        error_sample_type=ErrorSampleType.FIXED_COUNT,
        distribution_kwargs={"count": 2},
        seed=42,
    )
    method = TransposeWordErrorMethod(config)
    words = ["the", "quick", "brown", "fox"]
    result = method.apply_error(words, [0, 2])
    assert result == "quick the fox brown"


def test_error_methods_with_empty_string(error_config: ErrorConfig) -> None:
    methods = [
        DoubleWordErrorMethod(error_config),
        SkipWordErrorMethod(error_config),
        TransposeWordErrorMethod(error_config),
    ]
    for method in methods:
        result = method.execute("")
        assert result == ""


def test_error_methods_with_single_word(error_config: ErrorConfig) -> None:
    methods = [
        DoubleWordErrorMethod(error_config),
        SkipWordErrorMethod(error_config),
        TransposeWordErrorMethod(error_config),
    ]
    for method in methods:
        result = method.execute("word")
        assert len(result.split()) in [0, 1, 2]  # Depending on the method
