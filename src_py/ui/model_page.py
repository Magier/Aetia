import streamlit as st
from streamlit_bd_cytoscapejs import st_bd_cytoscape

import utils
from ui.session_state import get_state
from infer import edges_to_dot



def show():
    state = get_state()

    default_dag = [
        "age -> sodium",
        "age -> sbp",
        "sodium -> proteinuria",
        "sodium -> sbp",
        "sbp -> proteinuria"
    ]

    edges = st.text_area("DAG:", value='\n'.join(default_dag))
    edge_list = edges.split("\n")

    utils.get_cytoscape_params(edgelist=)
    st.text(edges_to_dot(edges))

    streamlit_bd_cytoscapejs.


    if st.button("Set Model"):
        state.model.set_model("arstarst")
