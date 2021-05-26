import streamlit as st
from ui.session_state import SessionState, get_state
from infer import ModelStage


def show(state: SessionState):
    st.header("Verify")
    state = get_state()
    if state.model.stage < ModelStage.ESTIMATED:
        st.error("The model must be estimated before it can be verified")
