"""
TextGraph Node objects
"""

from typing import Any, Callable, Dict


# pylint: disable=unused-argument
def default_action(state: Dict[str, Any], kwargs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Default action function that returns a copy of the input state.

    Args:
        state (Dict[str, Any]): The state of the node.
        kwargs (Dict[str, Any]): The metadata of the node.

    Returns:
        Dict[str, Any]: The output state of the node.
    """
    return state.copy()


class Node:
    """
    Node object that represents a node in a graph.
    """

    def __init__(
        self,
        name: str,
        action: Callable[
            [Dict[str, Any], Dict[str, Any]], Dict[str, Any]
        ] = default_action,
    ):
        """
        Initialize the Node object.

        Args:
            name (str): The name of the node.
            action (Callable[[Dict[str, Any], Dict[str, Any]], Dict[str, Any]]): The action to be executed by the node.
        """
        self.name = name
        self.action = action
        self.input_state: Dict[str, Any] = {}
        self.output_state: Dict[str, Any] = {}

    def execute(self, state: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Execute the action of the node.

        Args:
            state (Dict[str, Any]): The input state of the node.
            **kwargs: Additional keyword arguments.

        Returns:
            Dict[str, Any]: The output state of the node.
        """
        self.input_state = state.copy()
        self.output_state = self.action(state, kwargs)
        return self.output_state

    def __repr__(self) -> str:
        return f"Node(name='{self.name}', action={self.action}, input_state={self.input_state}, output_state={self.output_state})"

    def __str__(self) -> str:
        return f"Node: {self.name}"
