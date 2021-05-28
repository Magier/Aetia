from dataclasses import dataclass
from enum import IntFlag
from typing import List, Optional, Set
import networkx as nx


class NodeAttribute(IntFlag):
    REGULAR = 0
    TREATMENT = 1
    OUTCOME = 2
    ADJUSTED = 4
    UNOBSERVED = 8

    @classmethod
    def parse(cls, attr: str) -> "NodeAttribute":
        attr = attr.lower()
        if attr == "regular":
            return cls.REGULAR
        elif attr == "treatment":
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


@dataclass
class CausalModel:
    nodes: Set[str] = None
    edges: Set = None
    treatment: Optional[str] = None
    outcome: Optional[str] = None
    adjusted: Set[str] = None
    unobserved: Set[str] = None
    _graph: nx.DiGraph = None

    def __post_init__(self):
        self._build_graph()

    def _build_graph(self):
        self._graph = nx.DiGraph()

        if self.nodes is not None:
            self._graph.add_nodes_from(self.nodes, observed=True)
        if self.edges is not None:
            self._graph.add_edges_from(self.edges)

        # set node attributes
        node_attrs = {}
        if self.treatment is not None:
            node_attrs[self.treatment] = {"treatment": True}
        if self.outcome is not None:
            node_attrs[self.outcome] = {"outcome": True}
        if self.adjusted is not None:
            node_attrs.update({n: {"adjusted": True} for n in self.adjusted})
        if self.unobserved is not None:
            node_attrs.update({n: {"observed": False} for n in self.unobserved})
        nx.set_node_attributes(self._graph, node_attrs)

        # set edge attributes
        causal_edges = self.get_causal_paths(as_edge_list=True)
        edge_attrs = {e: {"causal": True} for e in causal_edges}

        biasing_edges = self.get_biasing_paths(as_edge_list=True)
        edge_attrs.update({e: {"biasing": True} for e in biasing_edges})
        nx.set_edge_attributes(self._graph, edge_attrs)

    def get_node_attributes(self, node: str) -> NodeAttribute:
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

    def update_node(self, node: str, attr: NodeAttribute) -> str:
        new_node_attrs = None
        if attr == NodeAttribute.TREATMENT:
            new_node_attrs = {
                self.treatment: {"treatment": False},
                node: {"treatment": True}
            }
            self.treatment = node
            return f"Treatment is now {self.treatment}"
        elif attr == NodeAttribute.OUTCOME:
            new_node_attrs = {
                self.outcome: {"outcome": False},
                node: {"outcome": True}
            }
            self.outcome = node
        elif attr == NodeAttribute.ADJUSTED:
            new_node_attrs = {node: {"adjusted": True}}
            self.adjusted.add(node)
        elif attr == NodeAttribute.UNOBSERVED:
            self.unobserved.add(node)
            new_node_attrs = {node: {"observed": False}}
        elif attr == NodeAttribute.REGULAR:
            # reset all other node attributes
            new_node_attrs = {node: {
                "treatment": False,
                "outcome": False,
                "adjusted": False,
                "observed": True
            }}

        if new_node_attrs is not None:
            nx.set_node_attributes(self._graph, new_node_attrs)

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
        self.edges = {(s, t) for s, t in self.edges if s != node_id and t != node_id}

    def delete_edge(self, source: str, target: str) -> None:
        self.edges.remove((source, target))

    def as_string(self) -> str:
        edges = [f"{s}[{str(self.get_node_attributes(s))}]->{t}[{str(self.get_node_attributes(t))}]" for s, t in
                 list(self.edges)]
        return "\n".join(edges)

    def get_causal_paths(self, as_edge_list: bool = False) -> List:
        if as_edge_list:
            paths = nx.all_simple_edge_paths(self._graph, self.treatment, self.outcome)
        else:
            paths = nx.all_simple_paths(self._graph, self.treatment, self.outcome)

        # the resulting generator is a list of lists, because multiple targets can be provided.
        # However, it is assumed, there is only one outcome, thus always return the first list
        return list(paths)[0]

    def get_biasing_paths(self, as_edge_list):
        return [("w", "age")]
