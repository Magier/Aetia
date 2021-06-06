from enum import IntEnum
from typing import List, Tuple


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


def edges_to_dot(edges: List[str]) -> str:
    edge_str = ";\n".join(edges)
    return f"""digraph graphname { {edge_str} }"""
