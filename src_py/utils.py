from causal_model import CausalModel
from typing import Dict, Iterable, List, Tuple, Optional
import networkx as nx


def get_cytoscape_params_from_model(causal_model: CausalModel) -> Tuple[List, List, Dict, Dict]:
    edge_list = list(causal_model.edges)  # edges_declaration_to_list(edges)

    cy_json = nx.readwrite.json_graph.cytoscape_data(causal_model._graph)
    a = 5

    node_classes = {
        causal_model.treatment: "treatment",
        causal_model.outcome: "outcome"
    }

    causal_edges = causal_model.get_causal_paths(as_edge_list=True)
    edge_classes = {e: "causal" for e in causal_edges}
    biasing_edges = causal_model.get_biasing_paths(as_edge_list=True)
    biasing_edges.append(edge_list[0])
    edge_classes.update({e: "biasing" for e in biasing_edges})

    for n in causal_model.unobserved:
        node_classes[n] = "unobserved"

    for n in causal_model.adjusted:
        node_classes[n] = "adjusted"

    _, style, layout, context_menu = get_cytoscape_params(edge_list, causal_model.nodes, node_classes, edge_classes)
    return cy_json["elements"], style, layout, context_menu


def get_cytoscape_params(
        edgelist: List[Tuple],
        nodes: Optional[Iterable[str]] = None,
        node_classes: Optional[Dict] = None,
        edge_classes: Optional[Dict[Tuple, str]] = None
) -> Tuple[List, List, Dict, Dict]:
    edges = [
        {"data": {"id": f"{s}->{t}", "source": s, "target": t}} for s, t in edgelist
    ]
    # edges = []
    # for s, t in edgelist:
    #     edge = {"data": {"id": f"{s}->{t}", "source": s, "target": t}}
        # if edge_classes is not None and edge


    node_iter = set(sum(edgelist, ())) if nodes is None else nodes

    nodes = []
    for node_id in node_iter:
        node = {"data": {"id": node_id, "name": node_id}}
        if node_classes is not None and node_id in node_classes:
            node["classes"] = node_classes.get(node_id, "")
        nodes.append(node)
    # nodes = [{"data": {"id": n}} for n in node_iter]
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
            "selector": "edge[causal]",
            "style": {
                "line-color": "green",
                "target-arrow-color": "green",
                "width": 4
            }
        },
        {
            "selector": "edge[biasing]",
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

    elements = nodes + edges
    return elements, style, layout, context_menu
