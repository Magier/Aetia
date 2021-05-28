import streamlit as st
from typing import Dict, List, Tuple
from st_cytoscape_builder import st_cytoscape_builder

import utils
from ui.session_state import SessionState, get_state
from infer import ModelStage, edges_to_dot, parse_model_string
from causal_model import CausalModel, NodeAttribute


def edges_declaration_to_list(edges: str) -> List[Tuple]:
    edge_list = [tuple([n.strip() for n in e.split("->")]) for e in edges.split("\n")]
    return edge_list


def load_default_model() -> CausalModel:
    default_dag = [
        "age -> sodium",
        "age -> sbp",
        "w[unobserved] -> age",
        "sodium[treatment] -> proteinuria",
        "sodium -> mediator",
        "mediator -> sbp",
        "sbp[outcome] -> proteinuria"
    ]
    model = parse_model_string(default_dag)
    return model


def handle_cytoscape_event(cy_event: Dict, model: CausalModel) -> bool:
    st.write(cy_event)
    element_type = cy_event.get("element", None)
    element_id = cy_event.get("id", None)
    event = cy_event.get("event", None)

    st.write("Handling cytoscape event!")
    st.write(event)

    if event == "TAP":
        st.write("it was just a small tap :)")
    elif event == "DELETE_NODE":
        model.delete_node(element_id)
        return True
    elif element_type == "node[name]":
        node_attr = model.get_node_attributes(element_id)
        st.write("node attributes:")
        st.write(node_attr)
        if event == "RESET_NODE":
            event = "regular"
        try:
            attr = NodeAttribute.parse(event.lower())
            model.update_node(element_id, attr)
            return True
        except ValueError as exc:
            st.warning(f"Not sure what to do with '{event}'")
    elif event == "ADD_EDGE":
        source, target = cy_event["data"]["source"], cy_event["data"]["target"]
        model.edges.add((source, target))
        return True
    elif event == "REMOVE_EDGE":
        source, target = cy_event["data"]["source"], cy_event["data"]["target"]
        model.delete_edge(source, target)
        return True
    elif event == "ADD_NODE":
        node_id = st.text_input("Name of node:", value="",
            help="this will be the id and label for the newly created node")
        if node_id != "":
            model.add_node(node_id)
            return True
    else:
        raise NotImplementedError(f"Can't handle event for event {event}")
    return False


def show(state: SessionState):
    if "model" not in state or st.button("Load default model"):
        st.info("Loading default model")
        model = load_default_model()
        state.model = model
    else:
        model = state.model

    elements, style, layout, ctx_menu = utils.get_cytoscape_params_from_model(model)

    cy_event = st_cytoscape_builder(elements, style, layout, context_menu=ctx_menu)
    if cy_event is not None:
        if handle_cytoscape_event(cy_event, model):
            st.experimental_rerun()
