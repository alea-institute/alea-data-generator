"""
TextGraph class to store and manipulate text data in the graph.
"""

# imports
from typing import Any, Dict

# project
from alea_data_generator.text_graph import Graph


class TextGraph(Graph):
    """
    TextGraph class to store and manipulate text data in the graph
    """

    def __init__(self, text: str = ""):
        """
        TextGraph constructor

        Args:
            text (str): Initial text to be added to the graph
        """
        super().__init__()
        self.text = text

    def execute(self, state: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Execute the graph with the given state and update the text attribute.

        Args:
            state (Dict[str, Any]): The initial state to start the execution.
            **kwargs: Additional keyword arguments.

        Returns:
            Dict[str, Any]: The final state after the execution.
        """
        state = super().execute(state, **kwargs)
        self.text += state.get("text", "")
        return state

    def get_text(self) -> str:
        """
        Get the current text stored in the TextGraph.

        Returns:
            str: The current text.
        """
        return self.text

    def clear_text(self) -> None:
        """
        Clear the current text stored in the TextGraph.
        """
        self.text = ""

    def append_text(self, new_text: str) -> None:
        """
        Append new text to the existing text in the TextGraph.

        Args:
            new_text (str): The text to be appended.
        """
        self.text += new_text
