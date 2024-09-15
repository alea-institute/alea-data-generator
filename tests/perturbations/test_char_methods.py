import pytest

from alea_data_generator.data.constants.keyboard import KEY_ERROR_MAPPING
from alea_data_generator.perturbations.errors.config import ErrorConfig, ErrorSampleType
from alea_data_generator.perturbations.errors.methods.double_character import (
    DoubleCharacterErrorMethod,
)
from alea_data_generator.perturbations.errors.methods.keyboard_character import (
    KeyboardCharacterErrorMethod,
)
from alea_data_generator.perturbations.errors.methods.skip_character import (
    SkipCharacterErrorMethod,
)
from alea_data_generator.perturbations.errors.methods.transpose_character import (
    TransposeCharacterErrorMethod,
)


@pytest.fixture
def error_config():
    return ErrorConfig(
        error_sample_type=ErrorSampleType.FIXED_COUNT,
        distribution_kwargs={"count": 2},
        seed=42,
    )


def test_double_character_method(error_config):
    method = DoubleCharacterErrorMethod(error_config)
    input_string = "hello world"
    result = method.execute(input_string)
    assert len(result) == len(input_string) + 2
    assert result != input_string


def test_skip_character_method(error_config):
    method = SkipCharacterErrorMethod(error_config)
    input_string = "hello world"
    result = method.execute(input_string)
    assert len(result) == len(input_string) - 2
    assert result != input_string


def test_transpose_character_method(error_config):
    method = TransposeCharacterErrorMethod(error_config)
    input_string = "hello world"
    result = method.execute(input_string)
    assert len(result) == len(input_string)
    assert result != input_string


def test_double_character_specific_positions():
    config = ErrorConfig(
        error_sample_type=ErrorSampleType.FIXED_COUNT,
        distribution_kwargs={"count": 2},
        seed=42,
    )
    method = DoubleCharacterErrorMethod(config)
    input_string = "abcdef"
    result = method.apply_error(input_string, [1, 3])
    assert result == "abbcddef"


def test_skip_character_specific_positions():
    config = ErrorConfig(
        error_sample_type=ErrorSampleType.FIXED_COUNT,
        distribution_kwargs={"count": 2},
        seed=42,
    )
    method = SkipCharacterErrorMethod(config)
    input_string = "abcdef"
    result = method.apply_error(input_string, [1, 3])
    assert result == "acef"


def test_transpose_character_specific_positions():
    config = ErrorConfig(
        error_sample_type=ErrorSampleType.FIXED_COUNT,
        distribution_kwargs={"count": 2},
        seed=42,
    )
    method = TransposeCharacterErrorMethod(config)
    input_string = "abcdef"
    result = method.apply_error(input_string, [1, 3])
    assert result == "acbedf"


def test_error_methods_with_empty_string(error_config):
    methods = [
        DoubleCharacterErrorMethod(error_config),
        SkipCharacterErrorMethod(error_config),
        TransposeCharacterErrorMethod(error_config),
    ]
    for method in methods:
        result = method.execute("")
        assert result == ""


def test_error_methods_with_single_character(error_config):
    methods = [
        DoubleCharacterErrorMethod(error_config),
        SkipCharacterErrorMethod(error_config),
        TransposeCharacterErrorMethod(error_config),
    ]
    for method in methods:
        result = method.execute("a")
        assert len(result) in [0, 1, 2]  # Depending on the method


def test_keyboard_character_method(error_config):
    method = KeyboardCharacterErrorMethod(error_config)
    input_string = "hello world"
    result = method.execute(input_string)
    assert len(result) == len(input_string)
    assert result != input_string

    # Check if the changes are valid keyboard substitutions
    for original, modified in zip(input_string, result):
        if original != modified:
            assert modified in KEY_ERROR_MAPPING.get(original, [])


def test_keyboard_character_specific_positions():
    config = ErrorConfig(
        error_sample_type=ErrorSampleType.FIXED_COUNT,
        distribution_kwargs={"count": 2},
        seed=42,
    )
    method = KeyboardCharacterErrorMethod(config)
    input_string = "abcdef"
    result = method.apply_error(input_string, [1, 3])
    assert len(result) == len(input_string)
    assert result != input_string

    # Check if the changes are at the correct positions and are valid substitutions
    for i, (original, modified) in enumerate(zip(input_string, result)):
        if i in [1, 3]:
            assert modified in KEY_ERROR_MAPPING.get(original, [])
        else:
            assert original == modified
