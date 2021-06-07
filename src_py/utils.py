from causal_graph import CausalGraph
from typing import Dict, Iterable, List, Tuple, Optional
import networkx as nx


def get_cytoscape_params_from_model(causal_model: CausalGraph) -> Tuple[List, List, Dict, Dict]:
    # edge_list = list(causal_model.edges)
    cy_json = nx.readwrite.json_graph.cytoscape_data(causal_model._graph)
    style, layout, context_menu = get_cytoscape_params()

    return cy_json["elements"], style, layout, context_menu


def get_cytoscape_params() -> Tuple[List, Dict, Dict]:
    style = [
        {
            "selector": "core",
            "style": {
                "background-color": "blue"
            }
        }, {
            "selector": "node[?treatment]",
            "style": {
                "background-color": "green",
            }
        },
        {
            "selector": "node[?outcome]",
            "style": {
                "background-color": "SteelBlue",
            }
        },
        {
            "selector": "node[?adjusted]",
            "style": {
                "shape": "rectangle",
                "border-width": 2,
                "border-color": "black",
            }
        },
        {
            "selector": "node[!observed]",
            "style": {
                "background-opacity": "0",
                "border-width": 2,
                "border-color": "darkgray",
                "border-style": "dashed",
            }
        },
        {
            "selector": "node[name]:selected",
            "style": {
                "border-color": "darkred",
                "border-width": 2,
            }
        },
        {
            "selector": "edge[?causal]",
            "style": {
                "line-color": "green",
                "target-arrow-color": "green",
                "width": 4
            }
        },
        {
            "selector": "edge[?biasing]",
            "style": {
                "line-color": "red",
                "target-arrow-color": "red",
                "width": 4
            }
        },
        {
            "selector": "edge:selected",
            "style": {
                "line-color": "darkred",
                "target-arrow-color": "darkred",
                "border-width": 2,
            }
        },
    ]

    layout = {"name": 'dagre', "rankDir": "LR"}
    context_menu = {
        "node[name]": {
            "commands": [
                {
                    "content": "fa-pills",
                    "type": "symbol",
                    "event": "TREATMENT"
                }, {
                    "content": "fa-question",
                    "type": "symbol",
                    "event": "OUTCOME"
                }, {
                    "content": "fa-screwdriver",
                    "type": "symbol",
                    "event": "ADJUSTED"
                }, {
                    "content": "fa-undo",
                    "type": "symbol",
                    "event": "RESET_NODE",
                }, {
                    "content": "fa-eye-slash",
                    "type": "symbol",
                    "event": "UNOBSERVED"
                }, {
                    "content": "fa-trash-alt",
                    "type": "symbol",
                    "event": "DELETE_NODE",
                    "fillColor": "red"
                },
            ]
        },
        "edge": {
            "commands": [
                {
                    "content": "fa-trash-alt",
                    "type": "symbol",
                    "event": "REMOVE_EDGE"
                }
            ]
        },
        "core": {
            "commands": [
                {
                    "content": "fa-plus",
                    "type": "symbol",
                    "event": "ADD_NODE"
                }
            ]

        }
    }

    return style, layout, context_menu


def edge_path_to_node_path(path: List[Tuple]) -> List[str]:
    """
    Convert a path of edges to a simple list of nodes (without direction information)
    :param path: the path of edges which will be convert
    :return: a path of nodes
    """
    if len(path) == 0:
        return []

    node_path = [path[0][0]]  # first node is the source of the path
    # the remaining nodes are the destination
    node_path += [e[1] for e in node_path[1:]]
    return node_path


def node_path_to_edge_path(path: List[str], graph: nx.DiGraph) -> List[Tuple]:
    """
    Convert a path of nodes to a list of edges (with direction information)
    :param path: the path of nodes which will be convert and enriched with direction information
    :param graph: a graph providing the information about the edge direction
    :return: a path of edges
    """
    assert len(path) > 1
    edge_path = [(s, t) if graph.has_edge(s, t) else (t, s) for s, t in zip(path, path[1:])]
    return edge_path
