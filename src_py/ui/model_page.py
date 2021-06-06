import streamlit as st
from typing import Dict, List, Tuple
from st_cytoscape_builder import st_cytoscape_builder

import utils
from ui.session_state import SessionState, get_state
from infer import ModelStage, edges_to_dot
from causal_graph import CausalGraph, NodeAttribute, parse_model_string

SAMPLE_DAGS = {
    "default": [
        "age -> sodium",
        "age -> sbp",
        "w[unobserved] -> age",
        "sodium[treatment] -> proteinuria",
        "sodium -> mediator",
        "mediator -> sbp",
        "sbp[outcome] -> proteinuria"
    ],
    "Collider": [
        "L -> A[treatment]",
        "A -> Y[outcome]",
        "L -> Y"
    ],
    "M-bias": [
        "U₁[unobserved] -> Z",
        "U₁[unobserved] -> Y[outcome]",
        "U₂[unobserved] -> A[treatment]",
        "U₂[unobserved] -> Z",
        "A -> Y"
    ],
    "frontdoor": [
        "A[treatment] -> M",
        "M -> Y[outcome]",
        "U[unobserved] -> A",
        "U -> Y"
    ],
}
# add more complex Shrier & Platt 2008: https://bmcmedresmethodol.biomedcentral.com/articles/10.1186/1471-2288-8-70


def edges_declaration_to_list(edges: str) -> List[Tuple]:
    edge_list = [tuple([n.strip() for n in e.split("->")]) for e in edges.split("\n")]
    return edge_list


def load_sample_model(model_name: str) -> CausalGraph:
    dag = SAMPLE_DAGS[model_name]
    model = parse_model_string(dag)
    return model


def handle_cytoscape_event(cy_event: Dict, model: CausalGraph) -> bool:
    st.write(cy_event)
    element_type = cy_event.get("element", None)
    element_id = cy_event.get("id", None)
    event = cy_event.get("event", None)

    st.write("Handling cytoscape event!")
    st.write(event)
    update_needed = False

    if event == "TAP":
        st.write("it was just a small tap :)")
    elif event == "DELETE_NODE":
        model.delete_node(element_id)
        update_needed = True
    elif element_type == "node[name]":
        node_attr = model.get_node_attributes(element_id)
        st.write("node attributes:")
        st.write(node_attr)
        if event == "RESET_NODE":  # to align with other events set node attribute to regular
            event = "regular"
        try:
            attr = NodeAttribute.parse(event.lower())
            model.update_node(element_id, attr)
            update_needed = True
        except ValueError as exc:
            st.warning(f"Not sure what to do with '{event}'")
    elif event == "ADD_EDGE":
        source, target = cy_event["data"]["source"], cy_event["data"]["target"]
        model.add_edge(source, target)
        update_needed = True
    elif event == "REMOVE_EDGE":
        source, target = cy_event["data"]["source"], cy_event["data"]["target"]
        model.delete_edge(source, target)
        update_needed = True
    elif event == "ADD_NODE":
        node_id = st.text_input("Name of node:", value="",
            help="this will be the id and label for the newly created node")
        if node_id != "":
            model.add_node(node_id)
            update_needed = True
    else:
        raise NotImplementedError(f"Can't handle event for event {event}")

    if update_needed:
        model.update_paths()

    return update_needed


def show(state: SessionState):
    sample_name = st.selectbox("Sample Model", list(SAMPLE_DAGS.keys()), index=0)
    if "model" not in state or st.button(f"Load {sample_name} model"):
        model = load_sample_model(sample_name)
        st.write(model)
        state.model = model
    else:
        model = state.model

    elements, style, layout, ctx_menu = utils.get_cytoscape_params_from_model(model)

    cy_event = st_cytoscape_builder(elements, style, layout, context_menu=ctx_menu)
    if cy_event is not None:
        if handle_cytoscape_event(cy_event, model):
            st.experimental_rerun()
