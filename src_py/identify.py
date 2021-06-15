from typing import Optional, Set
import networkx as nx

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


def identify_backdoor(graph: CausalGraph, treatment: str, outcome: str, conditioning_set: Optional[Set[str]] = None) -> None:

    pass

def check_backdoor_criterion(graph: CausalGraph, treatment: str, outcome: str, conditioning_set: Optional[Set[str]] = None) -> bool:
    """
    Check the given graph for any backdoor paths and see if they are blocked according to the backdoor criterion.
    The backdoor criterion is satisfied if the conditioning set:
        1) blocks all backdoor paths from the treatment to the outcome
        2) does not contain any descendants of the treatment
    :param graph: the causal graph
    :param treatment: the treatment node
    :param outcome: the outcome node
    :param conditioning_set a set of nodes conditioned on.
    :return:
    """
    # a valid backdoor criterion:
    # - a single adjustment set must block all backdoor paths
    # - descendant of treatment variable must not be part of adjustment set
    # perform various checks, if minimum set is wanted, finish after first match, ordered by size of adjustment set
    # 1) check if empty set is valid

    if conditioning_set is None:
        conditioning_set = set()

    # eligible nodes for adjustment are all nodes of backdoor paths except descendants of the treatment
    backdoor_paths = graph.get_backdoor_paths(treatment, outcome, as_edge_list=True)

    # treatment_descendants = nx.descendants(graph.graph, treatment)
    treatment_descendants = graph.get_post_treatment_nodes()

    all_paths_blocked = all(graph.is_path_blocked(p, conditioning_set) for p in backdoor_paths)
    return all_paths_blocked
