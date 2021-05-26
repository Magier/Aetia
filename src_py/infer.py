from os import terminal_size
import streamlit as st
import re
from enum import Enum, IntEnum, IntFlag
from typing import List, Optional, Set, Tuple, Union
from dataclasses import dataclass
from operator import ior
from functools import reduce

from altair.vegalite.v4.schema.core import Value


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


class NodeAttribute(IntFlag):
    REGULAR = 0
    TREATMENT = 1
    OUTCOME = 2
    ADJUSTED = 4
    UNOBSERVED = 8

    @classmethod
    def parse(cls, attr: str) -> "NodeAttribute":
        attr = attr.lower()
        if attr == "treatment":
            return cls.TREATMENT
        elif attr == "outcome":
            return cls.OUTCOME
        elif attr == "adjusted":
            return cls.ADJUSTED
        elif attr == "unobserved":
            return cls.UNOBSERVED
        else:
            raise ValueError(f"Can't parse '{attr}'")

    def __str__(self) -> str:
        if self == NodeAttribute.REGULAR:
            return ""
        else:
            return self.name.lower()


class ModelBuilder:
    def __init__(self):
        self._causal_model = None
        self.stage = ModelStage.INITIALIZED
        self.causal_model = None

    def set_model(self, causal_model):
        self.stage = ModelStage.DEFINED if causal_model is not None else ModelStage.INITIALIZED
        self.causal_model = causal_model


@dataclass
class CausalModel:
    nodes: Set[str] = None
    edges: Set = None
    treatment: Optional[str] = None
    outcome:  Optional[str] = None
    adjusted: Set[str] = None
    unobserved: Set[str] = None
    stage = ModelStage.INITIALIZED

    def __post_init__(self):
        if self.nodes is not None and len(self.nodes) > 0:
            self.stage = ModelStage.DEFINED

    def get_node_attributes(self, node: str) -> str:
        if self.treatment == node:
            return NodeAttribute.TREATMENT
        elif self.outcome == node:
            return NodeAttribute.OUTCOME
        elif node in self.adjusted:
            return NodeAttribute.ADJUSTED
        elif node in self.unobserved:
            return NodeAttribute.UNOBSERVED
        else:
            return NodeAttribute.REGULAR

    def add_node(self, node_id: str) -> None:
        self.nodes.add(node_id)

    def update_node(self, node: str, attr: NodeAttribute) -> None:
        if attr == NodeAttribute.TREATMENT:
            self.treatment = node
            return f"Treatment is now {self.treatment}"
        elif attr == NodeAttribute.OUTCOME:
            self.outcome = node
            return f"Outcome is now {self.outcome}/ {attr}"
        elif attr == NodeAttribute.ADJUSTED:
            self.adjusted.add(node)
            return f"Adjusted variables are now {self.adjusted}"
        elif attr == NodeAttribute.UNOBSERVED:
            self.unobserved.add(node)
            return f"Unobeserved variables are now {self.unobserved}"

    def delete_node(self, node_id: str) -> None:
        if self.treatment == node_id:
            self.treatment = None
        if self.outcome == node_id:
            self.outcome = None
        if node_id in self.adjusted:
            self.adjusted.remove(node_id)
        if node_id in self.unobserved:
            self.unobserved.remove(node_id)
        self.nodes.remove(node_id)
        self.edges = {(s, t) for s, t in self.edges if s != node_id and t !=node_id }

    def delete_edge(self, source:str, target: str) -> None:
        self.edges.remove((source, target))

    def as_string(self) -> str:
        edges = [f"{s}[{str(self.get_node_attributes(s))}]->{t}[{str(self.get_node_attributes(t))}]" for s, t in list(self.edges)]
        return "\n".join(edges)


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
                    raise ValueError(f"There is already a defined treatment: '{treatment}''. It will be overwritten with {node}")
                treatment = node
            if node_attr == NodeAttribute.OUTCOME:
                if outcome is not None and outcome != node:
                    raise ValueError(f"There is already a defined outcome: '{outcome}'. It will be overwritten with {node}")
                outcome = node
            if node_attr == NodeAttribute.UNOBSERVED:
                unobserved.add(node)
            if node_attr == NodeAttribute.ADJUSTED:
                adjusted.add(node)

    model = CausalModel(nodes, edges, treatment, outcome, adjusted, unobserved)
    return model


def edges_to_dot(edges: List[str]) -> str:
    edge_str = ";\n".join(edges)
    return f"""digraph graphname {
        {edge_str}
    }"""
