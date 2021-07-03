import streamlit as st

import utils
from identify.backdoor import adjust_backdoor
from st_cytoscape_builder import st_cytoscape_builder

from utils import generate_colliderapp_data


def show():
    st.header("Estimate")
    # state = get_state()
    if "model" not in st.session_state:
        st.error("Please prepare the statistical model by identifying it first!")
    else:
        elements, style, layout, ctx_menu = utils.get_cytoscape_params_from_model(st.session_state.model)
        st_cytoscape_builder(elements, style, layout, context_menu=ctx_menu, height=400)

    if st.button("Generate data"):
        df = generate_colliderapp_data(n=1000, seed=777, beta1=1.05, alpha1=0.5, alpha2=0.5)
        st.session_state.data = df
        st.dataframe(df)

    if "data" in st.session_state:
        df = st.session_state.data

        adjusted_df = adjust_backdoor(df, st.session_state.model)

