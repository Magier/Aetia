from infer import ModelBuilder
import streamlit as st
from ui import model_page, estimate_page, identify_page, verify_page
from ui.session_state import get_state


PAGES = {
    "Model": model_page,
    "Identify": identify_page,
    "Estimate": estimate_page,
    "Verify": verify_page
}


def main():
    state = get_state()

    if "model" not in state:
        st.write("initializing model")
        state.model = ModelBuilder()
    else:
        st.write(f"Model stage: {state.model.stage}")


    sel_page = st.sidebar.radio("Navigation", list(PAGES))
    PAGES[sel_page].show()


if __name__ == "__main__":
    main()