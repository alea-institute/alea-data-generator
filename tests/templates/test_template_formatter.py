import pytest

from alea_data_generator.templates.template_formatter import TemplateFormatter


@pytest.fixture
def template_formatter():
    return TemplateFormatter(tag_map={"test": lambda: "test_value"})


def test_build_pattern_map(template_formatter):
    template = "Hello, <|test|>!"
    pattern_map = template_formatter.build_pattern_map(template)
    assert ("test", None, None) in pattern_map


def test_parse_args(template_formatter):
    args_str = "('arg1', 42, True)"
    parsed_args = template_formatter.parse_args(args_str)
    assert parsed_args == ["arg1", 42, True]


def test_sample_values(template_formatter):
    pattern_map = {("test", None, None): None}
    value_map = template_formatter.sample_values(pattern_map)
    assert value_map == {("test", None, None): "test_value"}


def test_apply_template_map(template_formatter):
    template = "Hello, <|test|>!"
    value_map = {("test", None, None): "world"}
    result = template_formatter.apply_template_map(template, value_map)
    assert result == "Hello, world!"


def test_format(template_formatter):
    template = "Hello, <|test|>!"
    result = template_formatter.format(template)
    assert result == "Hello, test_value!"


def test_call_method(template_formatter):
    template = "Hello, <|test|>!"
    result = template_formatter(template)
    assert result == "Hello, test_value!"


def test_unknown_tag(template_formatter):
    template = "Hello, <|unknown|>!"
    with pytest.raises(ValueError):
        result = template_formatter.format(template)
        assert result == "Hello, <Unknown tag: unknown>!"


def test_invalid_arguments(template_formatter):
    template_formatter.tag_map["args_test"] = lambda x: x
    template = "Test: <|args_test(1, 2, 3)|>"
    result = template_formatter.format(template)
    assert result == "Test: <Error: Invalid arguments for args_test>"


def test_custom_tag_map(template_formatter):
    def name() -> str:
        return "John Doe"

    template_formatter.tag_map["name"] = name

    template = "Hello, <|name|>!"
    result = template_formatter.format(template)
    assert result == "Hello, John Doe!"

    # now test with spans
    result = template_formatter.format_with_annotations(template)
    assert result["text"] == "Hello, John Doe!"
    assert result["spans"] == [
        {"start": 7, "end": 15, "tag": "name", "value": "John Doe"}
    ]
