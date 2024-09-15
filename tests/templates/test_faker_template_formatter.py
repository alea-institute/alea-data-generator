import pytest

from alea_data_generator.templates.faker_formatter import FakerTemplateFormatter


@pytest.fixture
def faker_template_formatter():
    return FakerTemplateFormatter(seed=42)


def test_format_simple_template(faker_template_formatter):
    template = "Hello, <|name|>!"
    result = faker_template_formatter.format(template)
    assert result.startswith("Hello, ")
    assert result.endswith("!")
    assert result != template


def test_format_multiple_tags(faker_template_formatter):
    template = "<|name|> lives at <|address|> and works as a <|job|>."
    result = faker_template_formatter.format(template)
    assert " lives at " in result
    assert " and works as a " in result
    assert result != template


def test_format_indexed_tags(faker_template_formatter):
    template = "<|name:1|> and <|name:2|> are friends."
    result = faker_template_formatter.format(template)
    assert " and " in result
    assert " are friends." in result
    assert result != template


def test_format_unknown_tag(faker_template_formatter):
    template = "This is an <|unknown_tag|>."
    result = faker_template_formatter.format(template)
    assert result == "This is an <Unknown tag: unknown_tag>."


def test_consistent_results(faker_template_formatter):
    template = "<|name|> <|email|>"
    result1 = faker_template_formatter.format(template)
    result2 = faker_template_formatter.format(template)
    assert result1 != result2


def test_different_locales():
    formatter_en = FakerTemplateFormatter(locale="en_US", seed=42)
    formatter_fr = FakerTemplateFormatter(locale="fr_FR", seed=42)

    template = "<|name|> lives in <|city|>."
    result_en = formatter_en.format(template)
    result_fr = formatter_fr.format(template)

    assert result_en != result_fr


def test_custom_tag_map():
    def custom_greeting(name):
        return f"Hello, {name}!"

    custom_tags = {"greeting": custom_greeting}
    formatter = FakerTemplateFormatter(tag_map=custom_tags, seed=42)

    template = "<|greeting('Alice')|>"
    result = formatter.format(template)
    assert result == "Hello, Alice!"


def test_invalid_arguments(faker_template_formatter):
    template = "<|date('invalid', 'args')|>"
    result = faker_template_formatter.format(template)
    assert "<Error: Invalid arguments for date>" in result


def test_span_annotations(faker_template_formatter):
    template = "<|name|> <|email|>"
    result = faker_template_formatter.format_with_annotations(template)

    assert isinstance(result, dict)
    assert "text" in result
    assert "spans" in result
    assert len(result["spans"]) == 2

    print(result)
    for span in result["spans"]:
        assert result["text"][span["start"] : span["end"]] == span["value"]
