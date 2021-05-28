import random
import pandas as pd
import numpy as np
import streamlit as st
from ui.session_state import SessionState, get_state
from infer import ModelStage


def generate_data(n, seed, beta1, alpha1, alpha2):
    """
    
    Parameters
    ----------
    n
    seed
    beta1
    alpha1
    alpha2

    Returns
    -------

    """
    # example from collider app: https://watzilei.com/shiny/collider/
    random.seed(seed)
    age_years = np.random.normal(65, 5, n)
    sodium_gr = age_years / 18 + np.random.normal(size=n)
    sbp = beta1 * sodium_gr + 2. * age_years + np.random.normal(size=n)
    proteinuria = alpha1 * sodium_gr + alpha2 * sbp + np.random.normal(size=n)
    return pd.DataFrame({
        "sbp": sbp,
        "sodium": sodium_gr,
        "age": age_years,
        "proteinuria": proteinuria
    })


def show(state: SessionState):
    st.header("Estimate")
    state = get_state()
    if state.model.stage < ModelStage.IDENTIFIED:
        st.error("Please prepare the statistical model by identifying it first!")

    if st.button("Generate data"):
        df = generate_data(n=1000, seed=777, beta1=1.05, alpha1=0.5, alpha2=0.5)
        st.dataframe(df)
