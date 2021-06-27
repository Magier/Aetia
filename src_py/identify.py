from causal_graph import CausalGraph

# DoWhy supports 3 effect types for identification:
# - ATE
# - NDE  (natural direct effect)
# - NIE  (natural indirect effect)


# DoWhy supports 4 identification criteria:
# - Back-door criterion
# - Front-door criterion
# - Instrumental Variables
# - Mediation (Direct and indirect effect identification)


def identify(model: CausalGraph) -> None:
    pass


def identify_frontdoor(model: CausalGraph, traetment: str, outcome: str) -> None:
    pass
