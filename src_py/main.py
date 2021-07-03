import streamlit as st
from ui import model_page, estimate_page, identify_page, verify_page
from ui.session_state import get_state, _get_state

# TODO first time use layout alg in st_dag_builder, for updates use previous coordinates
# TODO use do calculus in general to identify causal effect
# TODO identify minimal adjustment sets (like dagitty)
#  done for backdoor paths
# TODO show that p(y|do(x=1)) != p(y|x)
# TODO implement simpson simulator
# simpson.simulator <- function(N,s,ce){
# 	Z1 <- rnorm(N,0,s)
# 	Z3 <- rnorm(N,0,s) + Z1
# 	Z5 <- rnorm(N,0,s) + Z3
# 	Z7 <- rnorm(N,0,s) + Z5
# 	U <- rnorm(N,0,s) + Z1
# 	Z6 <- rnorm(N,0,s) + Z7 + U
# 	Z4 <- rnorm(N,0,s) + Z5 + U
# 	Z2 <- rnorm(N,0,s) + Z3 + U
# 	X <- rnorm(N,0,s) + U
# 	Y <- rnorm(N,0,s) + ce*X + 10*Z7
# 	data.frame(Y,X,Z1,Z2,Z3,Z4,Z5,Z6,Z7)
# }
#
# # 1st parameter: sample size
# # 2nd parameter: noise standard deviation
# # 3rd parameter: true causal effect
# D <- simpson.simulator(1000,0.01,1)
#
# # adjusted for {Z1,Z2,Z3,Z4,Z5,Z6,Z7}
# m <- lm(D[,c(1,2,3,4,5,6,7,8,9)])
# summary(m)
# confint(m,'X')
# source: http://www.dagitty.net/learn/simpson/index.html

# Nice to have features:
# option to violate causal assumption, e.g.:
#  - faithfulness
#  - exchangeability
#  - SUTVA
#  - ??


# TODO features from Causal Fusion
# - Confounding Analysis
#   - Admissible Set
#   - Admissibility Test
#   - Instrumental Variables
#   - IV Admissibility test

# - Path Analysis
#   - d-separation
#   - is set of <nodes> independent of <nodes> conditional on <nodes>?
#   - Causal Paths
#   - Confounding Paths
#   - Biasing Paths

# - Do-Calculus Analysis
#   - Do-inspector
#   - Do-Seperation

# - Testable implications
#   - Conditional Independencies
#   - Verma Contraints


PAGES = {
    "Model": model_page,
    "Identify": identify_page,
    "Estimate": estimate_page,
    "Verify": verify_page
}


def main():
    # state = get_state()

    # if "model" not in state:
    #     st.write(f"Model stage: {state.model.stage}")
    # else:
    #     st.write("No model created")
    #     st.write("initializing model")

    sel_page = st.sidebar.radio("Navigation", list(PAGES))
    PAGES[sel_page].show()

    # state.sync()


if __name__ == "__main__":
    main()
