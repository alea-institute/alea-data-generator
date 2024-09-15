"""
TextGraph Edge objects that connect nodes with optionally-state-based probability.
"""

from typing import Any, Callable, Dict


# pylint: disable=unused-argument
def default_weight(state: Dict[str, Any], kwargs: Dict[str, Any]) -> float:
    """
    Default weight function that returns 1.0.

    Args:
        state (Dict[str, Any]): The state of the edge.
        kwargs (Dict[str, Any]): The metadata of the edge.

    Returns:
        float: The weight of the edge.
    """
    return 1.0


class Edge:
    """
    Edge objects that connect nodes with optionally-state-based probability.
    """

    def __init__(
        self,
        source: str,
        target: str,
        weight: (
            int | float | Callable[[Dict[str, Any], Dict[str, Any]], float]
        ) = default_weight,
    ):
        """
        Initialize the Edge object.

        Args:
            source (str): The name of the source node.
            target (str): The name of the target node.
            weight (int | float | Callable[[Dict[str, Any], Dict[str, Any]], float]): The weight of the edge.
        """
        self.source = source
        self.target = target
        self.weight = weight
        self.metadata: Dict[str, Any] = {}

    def get_weight(self, state: Dict[str, Any], **kwargs) -> float:
        """
        Get the weight of the edge.

        Args:
            state (Dict[str, Any]): The state of the edge.
            **kwargs: Additional keyword arguments.

        Returns:
            float: The weight of the edge.
        """
        if callable(self.weight):
            return self.weight(state, kwargs)
        return float(self.weight)

    def __repr__(self) -> str:
        return f"Edge(source='{self.source}', target='{self.target}', weight={self.weight}, metadata={self.metadata})"

    def __str__(self) -> str:
        return f"Edge: {self.source} -> {self.target}"
