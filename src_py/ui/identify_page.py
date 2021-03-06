import streamlit as st
from ui.session_state import SessionState, get_state
from infer import ModelStage


def show(state: SessionState):
    st.header("identify")
    state = get_state()
    if state.model.stage < ModelStage.DEFINED:
        st.error("Please create the model first!")
