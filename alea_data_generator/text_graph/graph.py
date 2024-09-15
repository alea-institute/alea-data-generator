"""
Graph class for representing a graph of nodes and edges.
"""

from typing import Any, Dict, List, Optional

import numpy as np

from alea_data_generator.text_graph.edge import Edge
from alea_data_generator.text_graph.node import Node


class Graph:
    """
    Graph object that represents a graph of nodes and edges with a start node and execution logic.
    """

    def __init__(
        self,
        nodes: Optional[List[Node]] = None,
        edges: Optional[List[Edge]] = None,
        start_node: Optional[str] = None,
    ):
        """
        Initialize the Graph object.

        Args:
            nodes (Optional[List[Node]]): The list of nodes in the graph.
            edges (Optional[List[Edge]]): The list of edges in the graph.
            start_node (Optional[str]): The name of the start node.
        """
        self.nodes: Dict[str, Node] = (
            {node.name: node for node in nodes} if nodes else {}
        )
        self.start_node = start_node
        self.edges: Dict[str, List[Edge]] = {}
        self.execution_history: List[Dict[str, Any]] = []

        if edges:
            for edge in edges:
                self.add_edge(edge)

    def add_node(self, node: Node) -> None:
        """
        Add a node to the graph.

        Args:
            node (Node): The node to add to the graph.
        """
        self.nodes[node.name] = node

    def add_edge(self, edge: Edge) -> None:
        """
        Internal method to add an edge to the graph.

        Args:
            edge (Edge): The edge to add to the graph.

        Raises:
            ValueError: If the source or target node is not in the graph.
        """
        if edge.source not in self.nodes:
            raise ValueError(f"Node '{edge.source}' not found in the graph.")
        if edge.target not in self.nodes:
            raise ValueError(f"Node '{edge.target}' not found in the graph.")

        if edge.source not in self.edges:
            self.edges[edge.source] = []
        self.edges[edge.source].append(edge)

    def set_start_node(self, start_node: str) -> None:
        """
        Set the start node of the graph.

        Args:
            start_node (str): The name of the start node.

        Raises:
            ValueError: If the start node is not in the graph.
        """
        if start_node not in self.nodes:
            raise ValueError(f"Node '{start_node}' not found in the graph.")
        self.start_node = start_node

    def get_next_node(
        self, current_node: str, state: Dict[str, Any], **kwargs
    ) -> Optional[str]:
        """
        Get the next node based on the current node and state.

        Args:
            current_node (str): The name of the current node.
            state (Dict[str, Any]): The state of the graph.
            **kwargs: Additional keyword arguments.

        Returns:
            Optional[str]: The name of the next node.
        """
        next_nodes = []
        next_weights = []

        for edge in self.edges.get(current_node, []):
            weight = edge.get_weight(state, **kwargs)
            if weight > 0:
                next_nodes.append(edge.target)
                next_weights.append(weight)

        if not next_nodes:
            return None

        if len(next_nodes) == 1:
            return next_nodes[0]

        total_weight = sum(next_weights)
        normalized_weights = [weight / total_weight for weight in next_weights]

        return np.random.choice(next_nodes, p=normalized_weights)

    def execute(self, state: Dict[str, Any], **kwargs) -> Dict[str, Any]:
        """
        Execute the graph with the given state.

        Args:
            state (Dict[str, Any]): The initial state of the graph.
            **kwargs: Additional keyword arguments.

        Returns:
            Dict[str, Any]: The final state of the graph.
        """
        current_node = self.start_node
        while current_node:
            node = self.nodes[current_node]
            state = node.execute(state, **kwargs)
            self.execution_history.append(
                {
                    "node": current_node,
                    "input_state": node.input_state,
                    "output_state": node.output_state,
                }
            )
            current_node = self.get_next_node(current_node, state, **kwargs)

        return state
