"""FakerTemplateFormatter class for ALEA data generation."""

# Standard library imports
import random
import re
from typing import Any, Callable, Dict, Optional, Tuple

# packages
from faker import Faker

# projects
from alea_data_generator.samplers.faker_sampler import FAKER_TAG_MAP
from alea_data_generator.templates.template_formatter import TemplateFormatter


class FakerTemplateFormatter(TemplateFormatter):
    """Class for formatting templates using Faker methods."""

    def __init__(
        self,
        pattern_mapper: re.Pattern[str] = re.compile(
            r"<\|(?P<tag>\w+)(?::(?P<index>[0-9]+|[a-z]))?(?P<args>\(.*?\))?\|>"
        ),
        locale: Optional[str] = None,
        seed: Optional[int] = None,
        tag_map: Optional[Dict[str, Callable]] = None,
    ):
        """
        Initialize the FakerTemplateFormatter.

        Args:
            pattern_mapper (Pattern[str]): Compiled regex pattern for matching Faker tags.
            locale (Optional[str]): The locale to use for the Faker instance.
            seed (Optional[int]): The seed for the random number generator.
            tag_map (Optional[Dict[str, Callable]]): Custom tag map to extend or override default tags.
        """
        super().__init__(pattern_mapper, FAKER_TAG_MAP.copy())
        self.faker = Faker(locale)
        if seed is not None:
            random.seed(seed)
            self.faker.seed_instance(seed)
        if tag_map:
            self.tag_map.update(tag_map)

    def sample_values(
        self, pattern_map: Dict[Tuple[str, Optional[str], Optional[str]], Any]
    ) -> Dict[Tuple[str, Optional[str], Optional[str]], Any]:
        """
        Sample values for each Faker method in the pattern map.

        Args:
            pattern_map (Dict[Tuple[str, Optional[str], Optional[str]], Any]): Mapping of Faker tags to their methods.

        Returns:
            Dict[Tuple[str, Optional[str], Optional[str]], Any]: Mapping of Faker tags to their sampled values.
        """
        value_map: Dict[Tuple[str, Optional[str], Optional[str]], Any] = {}
        for tag, index, args in pattern_map.keys():
            if tag in self.tag_map:
                if args:
                    try:
                        arg_list = self.parse_args(args)
                        value_map[(tag, index, args)] = self.tag_map[tag](*arg_list)
                    except Exception as e:  # pylint: disable=broad-except
                        value_map[(tag, index, args)] = (
                            f"<Error: Invalid arguments for {tag}>: {e}"
                        )
                else:
                    value_map[(tag, index, args)] = self.tag_map[tag]()
            else:
                value_map[(tag, index, args)] = f"<Unknown tag: {tag}>"
        return value_map
