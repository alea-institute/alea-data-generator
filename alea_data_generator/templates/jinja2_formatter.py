"""Jinja2TemplateFormatter class for ALEA data generation."""

# Standard library imports
from typing import Any, Dict, Optional

from faker import Faker

# Third-party imports
from jinja2 import BaseLoader, Environment, TemplateNotFound

from alea_data_generator.samplers.faker_sampler import FAKER_TAG_MAP

# Local imports
from alea_data_generator.templates.template_formatter import TemplateFormatter


class Jinja2TemplateFormatter(TemplateFormatter):
    """Class for formatting templates using Jinja2 and Faker methods."""

    def __init__(
        self,
        locale: Optional[str] = None,
        seed: Optional[int] = None,
        custom_filters: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the Jinja2TemplateFormatter.

        Args:
            locale (Optional[str]): The locale to use for the Faker instance.
            seed (Optional[int]): The seed for the random number generator.
            custom_filters (Optional[Dict[str, Any]]): Custom filters to add to the Jinja2 environment.
        """
        super().__init__()
        self.faker = Faker(locale)
        if seed is not None:
            Faker.seed(seed)

        self.env = Environment(loader=BaseLoader())
        self.env.globals.update(FAKER_TAG_MAP)
        self.env.globals["faker"] = self.faker

        if custom_filters:
            self.env.filters.update(custom_filters)

    def format(self, template: str) -> str:
        """
        Format a template string using Jinja2 and Faker methods.

        Args:
            template (str): The template string containing Jinja2 syntax and Faker methods.

        Returns:
            str: The formatted template with tags replaced by their corresponding values.
        """
        try:
            jinja_template = self.env.from_string(template)
            return jinja_template.render()
        except TemplateNotFound:
            return "<Error: Template not found>"
        except Exception as e:  # pylint: disable=broad-except
            return f"<Error: {str(e)}>"

    def add_custom_filter(self, name: str, filter_func: Any) -> None:
        """
        Add a custom filter to the Jinja2 environment.

        Args:
            name (str): The name of the filter to be used in templates.
            filter_func (Any): The filter function to be added.
        """
        self.env.filters[name] = filter_func

    def add_custom_global(self, name: str, global_func: Any) -> None:
        """
        Add a custom global function to the Jinja2 environment.

        Args:
            name (str): The name of the global function to be used in templates.
            global_func (Any): The global function to be added.
        """
        self.env.globals[name] = global_func
