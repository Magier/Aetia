from enum import IntEnum
from dataclasses import dataclass


class ModelStage(IntEnum):
    INITIALIZED = 0
    CREATED = 1
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
        self.stage = ModelStage.CREATED if causal_model is not None else ModelStage.INITIALIZED
        self.causal_model = causal_model


@dataclass
class CausalModel:
    nodes: list[str]

    

def edges_to_dot(edges: list[str]) -> str:
    edge_str = ";\n".join(edges)
    return f"""digraph graphname {
        {edge_str}
    }"""

