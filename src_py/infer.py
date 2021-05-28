import re
from enum import IntEnum
from typing import List, Tuple, Union
from operator import ior
from functools import reduce

from causal_model import CausalModel, NodeAttribute


class ModelStage(IntEnum):
    INITIALIZED = 0
    DEFINED = 1
    IDENTIFIED = 2
    ESTIMATED = 3
    VERIFIED = 4

    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented


class ModelBuilder:
    def __init__(self):
        self._causal_model = None
        self.stage = ModelStage.INITIALIZED
        self.causal_model = None

    def set_model(self, causal_model):
        self.stage = ModelStage.DEFINED if causal_model is not None else ModelStage.INITIALIZED
        self.causal_model = causal_model


def edges_declaration_to_list(edges: str) -> List[Tuple]:
    edge_list = [tuple([n.strip() for n in e.split("->")]) for e in edges.split("\n")]
    return edge_list


def normalize_node(node_name: str) -> Tuple[str, NodeAttribute]:
    attrs = NodeAttribute.REGULAR
    match = re.search(r"(.*)\[(.*)\]", node_name)
    if match:
        node_name, attributes = match.groups()
        try:
            attrs = reduce(ior, [NodeAttribute.parse(a) for a in attributes.split(",") if a], NodeAttribute.REGULAR)
        except ValueError as exc:
            print(f"Can't parse node attributes: '{attributes}': {exc}")
    return node_name, attrs


def parse_model_string(input: Union[str, List[str]]) -> CausalModel:
    treatment = None
    outcome = None
    adjusted = set()
    unobserved = set()
    nodes = set()
    edges = set()

    lines = input.split("\n") if isinstance(input, str) else input
    for line in lines:
        source, target, *_ = [n.strip() for n in line.split("->")]
        if len(_) > 0:
            raise NotImplementedError("Parsing of more than one edge per line are not yet supported!")

        source = normalize_node(source)
        target = normalize_node(target)

        edges.add((source[0], target[0]))

        for node, node_attr in [source, target]:
            nodes.add(node)
            if node_attr == NodeAttribute.TREATMENT:
                if treatment is not None and treatment != node:
                    raise ValueError(
                        f"There is already a defined treatment: '{treatment}''. It will be overwritten with {node}")
                treatment = node
            if node_attr == NodeAttribute.OUTCOME:
                if outcome is not None and outcome != node:
                    raise ValueError(
                        f"There is already a defined outcome: '{outcome}'. It will be overwritten with {node}")
                outcome = node
            if node_attr == NodeAttribute.UNOBSERVED:
                unobserved.add(node)
            if node_attr == NodeAttribute.ADJUSTED:
                adjusted.add(node)

    model = CausalModel(nodes, edges, treatment, outcome, adjusted, unobserved)
    return model


def edges_to_dot(edges: List[str]) -> str:
    edge_str = ";\n".join(edges)
    return f"""digraph graphname { {edge_str} }"""
