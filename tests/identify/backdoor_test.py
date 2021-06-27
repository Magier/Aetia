from src_py.identify.backdoor import get_adjustment_sets, check_backdoor_criterion
from src_py.causal_graph import parse_model_string
from src_py.sample_dags import SAMPLE_DAGS


class TestFrontdoorCriterionCheck:
    def test_simple_collider(self):
        model_str = SAMPLE_DAGS["Collider"]
        model = parse_model_string(model_str)
        is_valid = check_backdoor_criterion(model, treatment="X", outcome="Y", conditioning_set={"Z"})
        assert is_valid

    def test_canonical_frontdoor(self):
        model_str = SAMPLE_DAGS["canonical_frontdoor"]
        model = parse_model_string(model_str)
        is_valid = check_backdoor_criterion(model, treatment="X", outcome="Y", conditioning_set={"Z"})
        assert not is_valid


class TestBackdoorAdjustmentSetIdentification:
    def test_simple_collider_backdoor(self):
        model = parse_model_string(["x[T]->y[O]", "w->x", "w->y"])
        adj_sets = get_adjustment_sets(model, treatment="x", outcome="y")
        assert adj_sets == [set("w")]

    def test_m_bias(self):
        model_str = SAMPLE_DAGS["M-bias"]
        model = parse_model_string(model_str)
        adj_sets = get_adjustment_sets(model)
        assert len(adj_sets) == 1
        assert adj_sets[0] == set()  # no adjustment must be performed

    def test_big_m(self):
        model_str = SAMPLE_DAGS["big-M"]
        model = parse_model_string(model_str)
        adj_sets = get_adjustment_sets(model)
        assert len(adj_sets) == 4
        assert all("Z₁" in s for s in adj_sets)

    def test_schrier_and_platt_2008(self):
        model_str = SAMPLE_DAGS["Shrier&Platt, 2008"]
        model = parse_model_string(model_str)
        adj_sets = get_adjustment_sets(model)
        assert len(adj_sets) == 7

    def test_canonical_frontdoor(self):
        model_str = SAMPLE_DAGS["canonical_frontdoor"]
        model = parse_model_string(model_str)
        adj_sets = get_adjustment_sets(model)
        # front door can't be identified using backdoor adjustment
        assert len(adj_sets) == 0
