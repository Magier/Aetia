from typing import List, Optional, Set
from itertools import combinations
import pandas as pd

import numpy as np

from causal_graph import CausalGraph


def identify_backdoor(graph: CausalGraph, treatment: str, outcome: str,
        conditioning_set: Optional[Set[str]] = None) -> None:
    pass


def check_backdoor_criterion(graph: CausalGraph, treatment: str, outcome: str,
        conditioning_set: Optional[Set[str]] = None) -> bool:
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


def get_adjustment_sets(graph: CausalGraph, treatment: str = None, outcome: str = None, only_minimal_set: bool = True) -> List[
    Set[str]]:
    """

    :param graph:
    :param treatment:
    :param outcome:
    :param only_minimal_set:
    :return:
    """
    if treatment is None:
        treatment = graph.treatment
    if outcome is None:
        outcome = graph.outcome

    # get all backdoor paths
    # for every path, iterate over all node combinations
    backdoor_paths = graph.get_backdoor_paths(treatment, outcome)

    except_nodes = {treatment, outcome}.union(graph.get_unobserved_nodes())
    valid_adjustment_sets = []
    n_min_set = np.inf

    for p in backdoor_paths:
        intermediary_nodes = set(p) - except_nodes
        max_n = len(intermediary_nodes)
        for n, adjustment_set in [(n, set(comb)) for n in range(max_n + 1) for comb in
                                  combinations(intermediary_nodes, n)]:
            if n > n_min_set:  # stop search after having found all minimal sets for the smallest set size
                break
            is_satisfied = check_backdoor_criterion(graph, treatment, outcome, adjustment_set)
            if is_satisfied and adjustment_set not in valid_adjustment_sets:
                valid_adjustment_sets.append(adjustment_set)
                if only_minimal_set and n < n_min_set:
                    n_min_set = n

    return valid_adjustment_sets


def adjust_backdoor(df: pd.DataFrame, graph: CausalGraph) -> CausalGraph:
    """
    Leverage the information of the causal structure to adjust backdoor paths.
    :param df: the dataframe for which the causal effect will be adusted.
    :param graph:
    :return:
    """
    # P(Y|do(X)) = \sum_z P(Y|X, Z=z)P(Z=z)
    z = graph.adjusted
    y = graph.outcome
    x = graph.treatment

    # from Paul Hühnermunds course:   ... for binary values
    # mean(y[x==1 & z==1] * mean(z==1) + mean(y[x==1 & z==0])*mean(z==0)
    s_adj = df[df[x]].groupby(list(z))[y].agg("mean")
    return s_adj.sum()
