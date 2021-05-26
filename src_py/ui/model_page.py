import streamlit as st
from typing import Dict, List, Tuple
from st_cytoscape_builder import st_cytoscape_builder

import utils
from ui.session_state import SessionState, get_state
from infer import CausalModel, ModelStage, NodeAttribute, edges_to_dot, parse_model_string


def edges_declaration_to_list(edges: str) -> List[Tuple]:
    edge_list = [tuple([n.strip() for n in e.split("->")]) for e in edges.split("\n")]
    return edge_list


def load_default_model() -> CausalModel:
    default_dag = [
        "age -> sodium",
        "age -> sbp",
        "w[unobserved] -> age",
        "sodium[treatment] -> proteinuria",
        "sodium -> sbp",
        "sbp[outcome] -> proteinuria"
    ]
    model = parse_model_string(default_dag)
    return model


def handle_cytoscape_event(cy_event: Dict, model: CausalModel) -> None:
    st.write(cy_event)
    element_type = cy_event.get("element", None)
    element_id = cy_event.get("id", None)
    event = cy_event.get("event", None)

    if event == "TAP":
        st.write("it was just a small tap :)")
    elif event == "DELETE_NODE":
        model.delete_node(element_id)
        st.experimental_rerun()
    elif element_type == "node":
        node_attr = model.get_node_attributes(element_id)
        st.write(node_attr)
        try:
            attr = NodeAttribute.parse(event.lower())
            model.update_node(element_id, attr)
            st.experimental_rerun()
        except ValueError as exc:
            st.warning(f"Not sure what to do with '{event}'")
    elif event == "ADD_EDGE":
        source, target = cy_event["data"]["source"], cy_event["data"]["target"]
        model.edges.add((source, target))
        st.experimental_rerun()
    elif event == "REMOVE_EDGE":
        source, target = cy_event["data"]["source"], cy_event["data"]["target"]
        model.delete_edge(source, target)
        st.experimental_rerun()
    elif event == "ADD_NODE":
        node_id = st.text_input("Name of node:", value="",
            help="this will be the id and label for the newly created node")
        if node_id != "":
            model.add_node(node_id)
            st.experimental_rerun()
    else:
        raise NotImplementedError(f"Can't handle event for event {event}")


def show(state: SessionState):
    if "model" not in state or st.button("Load default model"):
        st.info("Loading default model")
        model = load_default_model()
        state.model = model
    else:
        model = state.model

    # model_str = st.text_area("DAG:", value=model.as_string())
    # model = parse_model_string(model_str)
    elements, style, layout, ctx_menu = utils.get_cytoscape_params_from_model(model)

    cy_event = st_cytoscape_builder(elements, style, layout, context_menu=ctx_menu)
    if cy_event is not None:
        handle_cytoscape_event(cy_event, model)
        state.model = model

    if st.button("Generate data"):
        generate_data(n=1000, seed=777, beta1=1.05, alpha1=0.5, alpha2=0.5)
