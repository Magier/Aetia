import random
from typing import Any, Dict, Iterable, List, Set, Tuple, Optional
import networkx as nx
import numpy as np
import pandas as pd


def get_cytoscape_params_from_model(causal_model: "CausalGraph") -> Tuple[List, List, Dict, Dict]:
    # edge_list = list(causal_model.edges)
    cy_json = nx.readwrite.json_graph.cytoscape_data(causal_model._graph)
    style, layout, context_menu = get_cytoscape_params()

    nodes = cy_json["elements"]["nodes"]
    for n in nodes:
        if "position" in n["data"]:
            n["position"] = n["data"]["position"]

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


def generate_colliderapp_data(n, seed, beta1, alpha1, alpha2) -> pd.DataFrame:
    """

    Parameters
    ----------
    n
    seed
    beta1
    alpha1
    alpha2

    Returns
    -------

    """
    # example from collider app: https://watzilei.com/shiny/collider/
    random.seed(seed)
    age_years = np.random.normal(65, 5, n)
    sodium_gr = age_years / 18 + np.random.normal(size=n)
    sbp = beta1 * sodium_gr + 2. * age_years + np.random.normal(size=n)
    proteinuria = alpha1 * sodium_gr + alpha2 * sbp + np.random.normal(size=n)
    return pd.DataFrame({
        "sbp": sbp,
        "sodium": sodium_gr,
        "age": age_years,
        "proteinuria": proteinuria
    })


def generate_confounder_data(n: int, seed: int = 0, ) -> Tuple[pd.DataFrame, float]:
    e_x = np.random.normal(size=n)
    e_y = np.random.normal(size=n)
    e_z = np.random.normal(size=n)

    z = e_z > 0
    x = z + e_x > 0.5
    y = (x + z + e_y) > 2

    y_dox = (1 + z + e_x) > 2

    df = pd.DataFrame({
        "X": x,
        "Y": y,
        "Z": z
    })

    return df, float(np.mean(y_dox))


def generate_data(n, nodes: Dict[str, Tuple[int, float]], seed: int=0) -> pd.DataFrame:
    if seed != 0:
        random.seed(seed)

    raise NotImplementedError
