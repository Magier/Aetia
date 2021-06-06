from infer import ModelBuilder
from causal_graph import CausalGraph, NodeAttribute
import streamlit as st
from ui import model_page, estimate_page, identify_page, verify_page
from ui.session_state import get_state, _get_state


PAGES = {
    "Model": model_page,
    "Identify": identify_page,
    "Estimate": estimate_page,
    "Verify": verify_page
}


def main():
    state = get_state()

    if "model" not in state:
    #     st.write(f"Model stage: {state.model.stage}")
    # else:
        st.write("No model created")
        st.write("initializing model")

    sel_page = st.sidebar.radio("Navigation", list(PAGES))
    PAGES[sel_page].show(state)

    # state.sync()


if __name__ == "__main__":
    main()
