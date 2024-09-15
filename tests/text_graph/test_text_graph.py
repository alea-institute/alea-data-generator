import random

import pytest

from alea_data_generator.text_graph import Edge, Graph, Node, TextGraph


def test_text_graph_svo():
    subj_article = Node(
        "subj_article", lambda x, _: {**x, "text": random.choice(["a", "the"])}
    )
    subj_noun = Node(
        "subj_noun",
        lambda x, _: {
            **x,
            "text": x.get("text", "") + " " + random.choice(["cat", "dog"]),
        },
    )
    verb = Node(
        "verb",
        lambda x, _: {
            **x,
            "text": x.get("text", "") + " " + random.choice(["eats", "drinks"]),
        },
    )
    obj_article = Node(
        "obj_article",
        lambda x, _: {
            **x,
            "text": x.get("text", "") + " " + random.choice(["a", "the"]),
        },
    )
    obj_noun = Node(
        "obj_noun",
        lambda x, _: {
            **x,
            "text": x.get("text", "") + " " + random.choice(["fish", "milk"]),
        },
    )

    subj_verb_edge = Edge("subj_article", "subj_noun")
    verb_obj_edge = Edge("subj_noun", "verb")
    obj_verb_edge = Edge("verb", "obj_article")
    obj_noun_edge = Edge("obj_article", "obj_noun")

    graph = TextGraph()
    graph.nodes = {
        "subj_article": subj_article,
        "subj_noun": subj_noun,
        "verb": verb,
        "obj_article": obj_article,
        "obj_noun": obj_noun,
    }
    graph.edges = {
        "subj_article": [subj_verb_edge],
        "subj_noun": [verb_obj_edge],
        "verb": [obj_verb_edge],
        "obj_article": [obj_noun_edge],
    }

    graph.set_start_node("subj_article")
    final_state = graph.execute({})
    assert "text" in final_state
    assert len(final_state["text"].split()) == 5
    assert graph.get_text() == final_state["text"]


def test_graph_creation():
    node1 = Node("node1")
    node2 = Node("node2")
    edge = Edge("node1", "node2")

    graph = Graph([node1, node2], [edge])

    assert "node1" in graph.nodes
    assert "node2" in graph.nodes
    assert "node1" in graph.edges
    assert len(graph.edges["node1"]) == 1


def test_graph_execution():
    node1 = Node("node1", lambda x, _: {**x, "value": 1})
    node2 = Node("node2", lambda x, _: {**x, "value": x["value"] + 1})
    edge = Edge("node1", "node2")

    graph = Graph([node1, node2], [edge])
    graph.set_start_node("node1")

    final_state = graph.execute({})
    assert final_state["value"] == 2


def test_graph_branching():
    start = Node("start", lambda x, _: {**x, "value": 0})
    branch1 = Node("branch1", lambda x, _: {**x, "value": x["value"] + 1})
    branch2 = Node("branch2", lambda x, _: {**x, "value": x["value"] + 2})
    end = Node("end", lambda x, _: {**x, "value": x["value"] * 2})

    edge1 = Edge("start", "branch1", weight=0.5)
    edge2 = Edge("start", "branch2", weight=0.5)
    edge3 = Edge("branch1", "end")
    edge4 = Edge("branch2", "end")

    graph = Graph([start, branch1, branch2, end], [edge1, edge2, edge3, edge4])
    graph.set_start_node("start")

    final_states = [graph.execute({}) for _ in range(100)]
    values = [state["value"] for state in final_states]
    assert set(values) == {2, 4}  # (0+1)*2 or (0+2)*2


def test_invalid_graph():
    node1 = Node("node1")
    node2 = Node("node2")
    invalid_edge = Edge("node1", "node3")

    with pytest.raises(ValueError):
        Graph([node1, node2], [invalid_edge])


def test_invalid_start_node():
    node1 = Node("node1")
    graph = Graph([node1])

    with pytest.raises(ValueError):
        graph.set_start_node("non_existent_node")


def test_empty_graph_execution():
    graph = Graph()
    assert graph.execute({}) == {}


def test_custom_weight_function():
    def custom_weight(state, kwargs):
        return state.get("value", 0) + 1

    node1 = Node("node1", lambda x, _: {**x, "value": 1})
    node2 = Node("node2", lambda x, _: {**x, "value": x["value"] + 1})
    edge = Edge("node1", "node2", weight=custom_weight)

    graph = Graph([node1, node2], [edge])
    graph.set_start_node("node1")

    final_state = graph.execute({})
    assert final_state["value"] == 2
    assert graph.edges["node1"][0].get_weight(final_state) == 3


def test_text_graph_methods():
    text_graph = TextGraph("Initial text. ")
    assert text_graph.get_text() == "Initial text. "

    text_graph.append_text("More text.")
    assert text_graph.get_text() == "Initial text. More text."

    text_graph.clear_text()
    assert text_graph.get_text() == ""

    node = Node("test_node", lambda x, _: {**x, "text": "Node text."})
    text_graph.add_node(node)
    text_graph.set_start_node("test_node")

    final_state = text_graph.execute({})
    assert final_state["text"] == "Node text."
    assert text_graph.get_text() == "Node text."
