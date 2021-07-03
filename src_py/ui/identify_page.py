import streamlit as st
from infer import ModelStage


def show():
    st.header("identify")
    if st.session_state.model.stage < ModelStage.DEFINED:
        st.error("Please create the model first!")
