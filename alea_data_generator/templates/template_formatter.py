"""TemplateFormatter and FakerTemplateFormatter classes for ALEA data generation."""

# Standard library imports
import ast
import re
import tokenize
from io import StringIO
from typing import Any, Callable, Dict, Optional, Pattern, Tuple

# Third-party imports

# Local imports


class TemplateFormatter:
    """Generic class for formatting templates."""

    def __init__(
        self,
        pattern_mapper: Pattern[str] = re.compile(
            r"<\|(?P<tag>\w+)(?::(?P<index>[0-9]+|[a-z]))?(?P<args>\(.*?\))?\|>"
        ),
        tag_map: Optional[Dict[str, Callable]] = None,
    ):
        """
        Initialize the TemplateFormatter.

        Args:
            pattern_mapper (Pattern[str]): Compiled regex pattern for matching tags.
            tag_map (Optional[Dict[str, Callable]]): Custom tag map to extend or override default tags.
        """
        self.pattern = pattern_mapper
        self.tag_map = tag_map or {}

    def build_pattern_map(
        self, template: str
    ) -> Dict[Tuple[str, Optional[str], Optional[str]], Any]:
        """
        Build a mapping of tags in a template to their corresponding methods.

        Args:
            template (str): The template string containing tags.

        Returns:
            Dict[Tuple[str, Optional[str], Optional[str]], Any]: Mapping of tags to their methods.
        """
        matches = self.pattern.finditer(template)
        return {
            (match.group("tag"), match.group("index"), match.group("args")): None
            for match in matches
        }

    def parse_args(self, args_str: str) -> list:
        """
        Parse arguments from a string into a list of Python objects.

        Args:
            args_str (str): String representation of arguments.

        Returns:
            list: List of parsed Python objects.
        """
        args = []
        if args_str:
            # Remove parentheses
            args_str = args_str[1:-1]
            # Tokenize the arguments
            tokens = tokenize.generate_tokens(StringIO(args_str).readline)
            for token in tokens:
                if token.type == tokenize.STRING:
                    args.append(ast.literal_eval(token.string))
                elif token.type == tokenize.NUMBER:
                    args.append(ast.literal_eval(token.string))
                elif token.string in ("True", "False", "None"):
                    args.append(ast.literal_eval(token.string))
        return args

    def sample_values(
        self, pattern_map: Dict[Tuple[str, Optional[str], Optional[str]], Any]
    ) -> Dict[Tuple[str, Optional[str], Optional[str]], Any]:
        """
        Sample values for each method in the pattern map.

        Args:
            pattern_map (Dict[Tuple[str, Optional[str], Optional[str]], Any]): Mapping of tags to their methods.

        Returns:
            Dict[Tuple[str, Optional[str], Optional[str]], Any]: Mapping of tags to their sampled values.
        """
        value_map: dict[tuple[str, str | None, str | None], Any] = {}
        for tag, index, args in pattern_map.keys():
            if tag in self.tag_map:
                if isinstance(args, str):
                    try:
                        arg_list = self.parse_args(args)
                        value_map[(tag, index, args)] = self.tag_map[tag](*arg_list)  # type: ignore
                    except Exception:  # pylint: disable=broad-except
                        value_map[(tag, index, args)] = (
                            f"<Error: Invalid arguments for {tag}>"
                        )
                elif args is None:
                    value_map[(tag, index, args)] = self.tag_map[tag]()  # type: ignore
                else:
                    raise ValueError(f"Invalid args type for tag: {tag}")
            else:
                raise ValueError(f"Unknown tag: {tag}")
        return value_map

    def apply_template_map(
        self,
        template: str,
        value_map: Dict[Tuple[str, Optional[str], Optional[str]], Any],
    ) -> str:
        """
        Apply a mapping of tags to their corresponding values to a template.

        Args:
            template (str): The template string containing tags.
            value_map (Dict[Tuple[str, Optional[str], Optional[str]], Any]): Mapping of tags to their values.

        Returns:
            str: The template with tags replaced by their corresponding values.
        """
        output = template
        for (tag, index, args), value in value_map.items():
            tag_pattern = (
                f"<|{tag}{f':{index}' if index else ''}{args if args else ''}|>"
            )
            output = output.replace(tag_pattern, str(value))
        return output

    def format(self, template: str) -> str:
        """
        Format a template string by sampling values for each method.

        Args:
            template (str): The template string containing tags.

        Returns:
            str: The formatted template with tags replaced by their corresponding values.
        """
        pattern_map = self.build_pattern_map(template)
        value_map = self.sample_values(pattern_map)
        return self.apply_template_map(template, value_map)

    def __call__(self, template: str) -> str:
        """
        Call the format method on the template string.

        Args:
            template (str): The template string containing tags.

        Returns:
            str: The formatted template with tags replaced by their corresponding values.
        """
        return self.format(template)

    def format_with_annotations(self, template: str) -> Dict[str, Any]:
        """
        Format a template string by sampling values for each method and return annotations.

        Args:
            template (str): The template string containing tags.

        Returns:
            Dict[str, Any]: A dictionary containing the formatted text and span annotations.
        """
        # set up the pattern map and sample values
        pattern_map = self.build_pattern_map(template)
        value_map = self.sample_values(pattern_map)

        output_text = template
        spans = []
        try:
            while match := next(self.pattern.finditer(output_text)):
                start_pos = match.start()
                end_pos = match.end()
                tag = match.group("tag")
                index = match.group("index")
                args = match.group("args")
                value = value_map[(tag, index, args)]
                output_text = (
                    output_text[:start_pos] + str(value) + output_text[end_pos:]
                )
                spans.append(
                    {
                        "start": start_pos,
                        "end": start_pos + len(str(value)),
                        "tag": tag,
                        "value": str(value),
                    }
                )
        except StopIteration:
            pass

        return {"text": output_text, "spans": spans}
