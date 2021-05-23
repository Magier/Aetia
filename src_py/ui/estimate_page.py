import streamlit as st
from ui.session_state import get_state
from infer import ModelStage


def show():
    st.header("Estimate")
    state = get_state()
    if state.model.stage < ModelStage.IDENTIFIED:
        st.error("Please prepare the statistical model by identifying it first!")
