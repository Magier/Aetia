import re
from collections import Counter
from dataclasses import dataclass
from enum import IntFlag
from functools import reduce
from operator import ior
from typing import Any, Dict, List, Optional, Set, Tuple, Union
from functools import lru_cache
import networkx as nx

import utils


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
        elif attr in ["treatment", "t"]:
            return cls.TREATMENT
        elif attr in ["outcome", "o"]:
            return cls.OUTCOME
        elif attr in ["adjusted", "a"]:
            return cls.ADJUSTED
        elif attr in ["unobserved", "u"]:
            return cls.UNOBSERVED
        else:
            print(f"Can't parse node attribute: '{attr}'")
            # raise ValueError(f"Can't parse '{attr}'")
            return cls.REGULAR

    def __str__(self) -> str:
        if self == NodeAttribute.REGULAR:
            return ""
        else:
            return self.name.lower()


@dataclass
class Node:
    name: str
    attribute: NodeAttribute = NodeAttribute.REGULAR
    meta: Optional[Any] = None


@dataclass
class CausalGraph:
    nodes: Set[str] = None
    edges: Set = None
    treatment: Optional[str] = None
    outcome: Optional[str] = None
    adjusted: Set[str] = None
    unobserved: Set[str] = None
    # compounds: Dict[Set[str]] = None
    _graph: nx.DiGraph = None

    def __post_init__(self):
        self._build_graph()

    def _build_graph(self):
        self._graph = nx.DiGraph()

        if self.nodes is not None:
            self._graph.add_nodes_from(self.nodes, observed=True, parent="all")
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
        self.update_paths()

    @property
    def graph(self):
        return self._graph

    def update_paths(self):
        causal_edges = [e for path in self.get_causal_paths(as_edge_list=True) for e in path]
        biasing_edges = [e for path in self.get_biasing_paths(as_edge_list=True) for e in path]

        edge_attrs = {e: {
            "causal": e in causal_edges,
            "biasing": e in biasing_edges
        } for e in self._graph.edges()}

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
        self._graph.add_node(node_id, observed=True)

    def add_edge(self, source: str, target: str) -> None:
        self.edges.add((source, target))
        self._graph.add_edge(source, target)

    def update_node(self, node: str, attr: NodeAttribute) -> str:
        new_node_attrs = None
        if attr == NodeAttribute.TREATMENT:
            new_node_attrs = {
                self.treatment: {"treatment": False},
                node: {"treatment": True}
            }
            self.treatment = node
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
                "observed": True,
            }}
            if node in self.adjusted:
                self.adjusted.remove(node)
            if node in self.unobserved:
                self.unobserved.remove(node)

        if new_node_attrs is not None:
            nx.set_node_attributes(self._graph, new_node_attrs)

    def set_node_position(self, node: str, x, y) -> None:
        node_attr = {"position": {"x": x, "y": y}}
        nx.set_node_attributes(self._graph, {node: node_attr})

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
        self._graph.remove_node(node_id)

    def delete_edge(self, source: str, target: str) -> None:
        self.edges.remove((source, target))
        self._graph.remove_edge(source, target)

    def as_string(self) -> str:
        edges = [f"{s}[{str(self.get_node_attributes(s))}]->{t}[{str(self.get_node_attributes(t))}]" for s, t in
                 list(self.edges)]
        return "\n".join(edges)

    def get_causal_paths(self, as_edge_list: bool = False) -> List[List[Tuple]]:
        if self.treatment is None or self.outcome is None:
            return []

        if as_edge_list:
            paths = nx.all_simple_edge_paths(self._graph, self.treatment, self.outcome)
        else:
            paths = nx.all_simple_paths(self._graph, self.treatment, self.outcome)
        return list(paths)

    def get_biasing_paths(self, as_edge_list: bool = True) -> List[List[Tuple]]:
        if self.treatment is None or self.outcome is None:
            return []
        backdoor_paths = self.get_backdoor_paths(self.treatment, self.outcome, as_edge_list=True)
        biasing_paths = [path for path in backdoor_paths if not self.is_path_blocked(path, self.adjusted)]
        if not as_edge_list:
            biasing_paths = [utils.edge_path_to_node_path(p) for p in biasing_paths]
        return biasing_paths

    def get_backdoor_paths(self, source: str, target: str, as_edge_list: bool = False):
        undirected_graph = self._graph.to_undirected()
        # by definition a backdoor path is any path to the target node, which starts
        # with an edge pointing to the source node (i.e. back door)
        backdoor_paths = [
            pth
            for pth in nx.all_simple_paths(undirected_graph, source=source, target=target)
            if self._graph.has_edge(pth[1], pth[0])]

        if as_edge_list:
            backdoor_edge_paths = []
            # the identified paths are undirected; the keep consistency, the edges
            # on the path have to be in the right direction
            for path in backdoor_paths:
                fixed_path = []
                for s, t in zip(path, path[1:]):
                    fixed_path.append((s, t) if self._graph.has_edge(s, t) else (t, s))
                backdoor_edge_paths.append(fixed_path)
            backdoor_paths = backdoor_edge_paths
        return backdoor_paths

    def is_path_blocked(self, path: List[Tuple], conditioning_set: Optional[Set] = None) -> bool:
        # rule 1 (unconditional separation): is there no collider
        target_counts = Counter([target for src, target in path])
        path_nodes = set([node for edge in path for node in edge])
        colliders = {node for node, c in target_counts.items() if c > 1}
        if conditioning_set is None or len(conditioning_set) == 0:
            return len(colliders) > 0

        # rule 2 (blocking by conditioning): is a variable on the path conditioned on
        # only variables on the path are valid blockers
        blocking_nodes = conditioning_set.union(colliders).intersection(path_nodes)

        # rule 3 (conditioning on colliders): paths blocked by colliders
        # which are conditioned on (or its descendants) are 'open'
        collider_descendants = {n: nx.descendants(self._graph, n) for n in colliders}
        descendants = reduce(set.union, collider_descendants.values(), set())

        defused_colliders = colliders.union(descendants).intersection(conditioning_set)
        blocking_nodes = blocking_nodes.difference(defused_colliders)

        return len(blocking_nodes) > 0

    def get_post_treatment_nodes(self):
        return nx.descendants(self._graph, self.treatment)

    def get_unobserved_nodes(self):
        return self.unobserved


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


def parse_edges(lines: Union[List[str], str], sep: str = ";") -> List[Tuple[Node, Node]]:
    if isinstance(lines, List):
        lines = sep.join(lines)  # multiple edges are split by ';' - if list is provided join them with the same separator, so there is no difference, if multiple edges are defined per line

    edges = []
    for line in lines.split(';'):
        if "->" in line:
            source, target, *_ = [n.strip() for n in line.split("->")]
            edges.append((source, target))
    return edges


def parse_model_string(model_string: Union[str, List[str]]) -> CausalGraph:
    treatment = None
    outcome = None
    adjusted = set()
    unobserved = set()
    nodes = set()
    edges = set()
    compounds = {}

    lines = model_string.split("\n") if isinstance(model_string, str) else model_string
    for line in lines:
        is_compound = False
        if "->" in line:
            source, target, *_ = [n.strip() for n in line.split("->")]
        elif "<-" in line:
            target, source, *_ = [n.strip() for n in line.split("<-")]
        elif "--" in line:
            target, source, *_ = [n.strip() for n in line.split("--")]  # unobserved confounding
            # TODO
        elif "∈" in line:
            source, target, *_ = [n.strip() for n in line.split("∈")]
            is_compound = True
        else:
            raise ValueError(f"No valid edge direction specified in '{line}'. Expecting either '->' or '<-'")
        if len(_) > 0:
            raise NotImplementedError("Parsing of more than one edge per line are not yet supported!")

        source = normalize_node(source)
        target = normalize_node(target)

        if is_compound:
            parent = compounds.get(target, set())
            parent.add(source)
            compounds[target] = parent
        else:
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

    model = CausalGraph(nodes, edges, treatment, outcome, adjusted, unobserved)
    return model


def get_query_from_graph(graph: CausalGraph, cause: str, effect: str) -> str:
    return f"P({effect}|do({cause}))"
