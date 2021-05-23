from typing import List, Tuple, Optional

def get_cytoscape_params(
        edgelist: List[Tuple], nodes: Optional[List[str]] = None, for_jupyter: bool = False
):
    edges = [
        {"data": {"id": f"{s}->{t}", "source": s, "target": t}} for s, t in edgelist
    ]

    node_iter = set(sum(edgelist, ())) if nodes is None else nodes
    nodes = [{"data": {"id": n}} for n in node_iter]
    style = [
        {"selector": "core", "style": {"background": "blue"}},
        {
            "selector": "node",
            "style": {
                "label": "data(id)",
                "background-color": "gray",
                "font-size": "2em",
                "text-valign": "center",
                "text-halign": "center",
            },
        },
        {
            "selector": "edge",
            "style": {
                "curve-style": "bezier",
                "target-arrow-shape": "triangle",
                "width": 5,
                # "line-color": "#ddd",
                "background-fill": "linear-gradient(yellow, darkgray)",
                "target-arrow-color": "darkgray",
            },
        },
    ]

    layout = {"name": "breadthfirst", "directed": True, "circle": True}
    if for_jupyter:
        elements = {"nodes": nodes, "edges": edges}
    else:
        elements = nodes + edges
    return elements, style, layout