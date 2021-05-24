from numpy import union1d
from infer import CausalModel
from typing import Dict, List, Tuple, Optional



def get_cytoscape_params_from_model(causal_model: CausalModel) -> Tuple:
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
):
    edges = [
        {"data": {"id": f"{s}->{t}", "source": s, "target": t}} for s, t in edgelist
    ]

    node_iter = set(sum(edgelist, ())) if nodes is None else nodes

    primary_color = "darkgray"
    secondary_color = "lightgray"


    nodes = []
    for node_id in node_iter:
        node = {"data": {"id": node_id}}
        if node_classes is not None and node_id in node_classes:
            node["classes"] = node_classes.get(node_id, "")
        nodes.append(node)
    # nodes = [{"data": {"id": n}} for n in node_iter]
    style = [
        {"selector": "core", "style": {"background": "blue"}},
        {
            "selector": "node",
            "style": {
                "label": "data(id)",
                "background-color": primary_color,
                "font-size": "2em",
                "color": "darkgreen",
                "text-valign": "center",
                "text-halign": "center",
            },
        },
        {
            "selector": ".treatment",
            "style": {
                "background-color": "green",
                "color": primary_color,
            }
        },
        {
            "selector": ".outcome",
            "style": {
                "background-color": "blue",
                "color": primary_color,
            }
        },
        {
            "selector": ".unobserved",
            "style": {
                "background-color": "transparent",
                "border-width": 2,
                "border-color": primary_color,
                "border-style": "dashed",
            }
        },
        {
            "selector": "edge",
            "style": {
                "curve-style": "bezier",
                "target-arrow-shape": "triangle",
                "width": 5,
                # "line-color": "#ddd",
                "background-fill": "linear-gradient(yellow, lightgray)",
                "target-arrow-color": primary_color,
            },
        },
    ]

    layout = {"name": "breadthfirst", "directed": True, "circle": True}
    # if for_jupyter:
    #     elements = {"nodes": nodes, "edges": edges}
    # else:
    elements = nodes + edges
    return elements, style, layout