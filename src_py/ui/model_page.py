from typing import List, Tuple
import streamlit as st
from streamlit_bd_cytoscapejs import st_bd_cytoscape

import utils
from ui.session_state import get_state
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


def show(state):
    if "model" not in state or st.button("Load default model"):
        st.info("Loading default model")
        model = load_default_model()
        state.model = model
    else:
        model = state.model
        st.write(state.model)

    model_str = st.text_area("DAG:", value=model.as_string())
    model = parse_model_string(model_str)

    elements, style, layout = utils.get_cytoscape_params_from_model(model)

    tap_id = st_bd_cytoscape(elements, style, layout)
    st.write(tap_id)

    if tap_id != 0:
        node_attr = model.get_node_attributes(tap_id)
        st.write(node_attr)

        attrs = [NodeAttribute.REGULAR, NodeAttribute.TREATMENT, NodeAttribute.OUTCOME, NodeAttribute.ADJUSTED, NodeAttribute.UNOBSERVED]
        cols = st.beta_columns(len(attrs))
        actions = {
            attr: cols[i].button(f"Set {str(attr).title()}" if attr > NodeAttribute.REGULAR else "reset")
            for i, attr in enumerate(attrs)
            if node_attr != attr
        }

        st.write(f"Set treatment #{tap_id} as ")
        action = [k for k, v in actions.items() if v]
        if len(action) > 0:
             model.update_node(tap_id, action[0])
             state.model = model
        st.write(action)

        st.write(model.as_string())
