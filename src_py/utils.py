from infer import CausalModel
from typing import Dict, List, Tuple, Optional


def get_cytoscape_params_from_model(causal_model: CausalModel) -> Tuple[List, List, Dict, Dict]:
    edge_list = list(causal_model.edges)  #edges_declaration_to_list(edges)

    node_classes = {}
    node_classes[causal_model.treatment] = "treatment"
    node_classes[causal_model.outcome] = "outcome"

    for n in causal_model.unobserved:
        node_classes[n] = "unobserved"

    for n in causal_model.adjusted:
        node_classes[n] = "adjusted"

    return get_cytoscape_params(edge_list, causal_model.nodes, node_classes)


def get_cytoscape_params(
        edgelist: List[Tuple], nodes: Optional[List[str]] = None, node_classes: Optional[Dict]  = None
) -> Tuple[List, List, Dict, Dict]:
    edges = [
        {"data": {"id": f"{s}->{t}", "source": s, "target": t}} for s, t in edgelist
    ]

    node_iter = set(sum(edgelist, ())) if nodes is None else nodes

    nodes = []
    for node_id in node_iter:
        node = {"data": {"id": node_id, "label": node_id}}
        if node_classes is not None and node_id in node_classes:
            node["classes"] = node_classes.get(node_id, "")
        nodes.append(node)
    # nodes = [{"data": {"id": n}} for n in node_iter]
    style = [
        {"selector": "core", "style": {"background": "blue"}},
        {
            "selector": ".treatment",
            "style": {
                "background-color": "green",
            }
        },
        {
            "selector": ".outcome",
            "style": {
                "background-color": "SteelBlue",
            }
        },
        {
            "selector": ".unobserved",
            "style": {
                "background-opacity": "0",
                "border-width": 2,
                "border-color": "darkgray",
                "border-style": "dashed",
            }
        },
        {
            "selector": ":selected",
            "style": {
                "border-color": "darkred",
                "border-width": 2,
            }
        },
    ]

    layout = {"name": 'dagre', "rankDir": "LR"}

    context_menu = {
        "node": {
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
