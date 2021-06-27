from typing import Dict, List, Set

from causal_graph import CausalGraph
# from .backdoor import check_backdoor_criterion, identify_backdoor
import src_py.identify.backdoor as backdoor
import src_py.identify.frontdoor as frontdoor
import src_py.identify.do_calculus as do_calculus


def get_adjustment_set(graph: CausalGraph, treatment: str, outcome: str) -> Dict[str, List[Set[str]]]:
    return {
        "backdoor": backdoor.get_adjustment_sets(graph, treatment, outcome),
        "frontoor": frontdoor.get_adjustment_set(graph, treatment, outcome),
        "do-calculus": do_calculus.get_adjustment_set(graph, treatment, outcome)
    }
