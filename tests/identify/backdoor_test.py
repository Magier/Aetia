from src_py.identify.backdoor import get_adjustment_sets, check_backdoor_criterion, adjust_backdoor
from src_py.causal_graph import NodeAttribute, parse_model_string
from src_py.sample_dags import SAMPLE_DAGS
from src_py.utils import generate_colliderapp_data, generate_confounder_data


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

    def test_eco(self):
        model_str = SAMPLE_DAGS["College Wage Premium"]
        model = parse_model_string(model_str)
        adj_sets = get_adjustment_sets(model)
        assert len(adj_sets) == 1
        assert adj_sets[0] == {'E'}


class TestBackdoorAdjustment:
    def test_collider_app_example(self):
        model_str = SAMPLE_DAGS["ColliderApp"]
        model = parse_model_string(model_str)
        model.update_node("age", NodeAttribute.ADJUSTED)

        df = generate_colliderapp_data(n=1000, seed=777, beta1=1.05, alpha1=0.5, alpha2=0.5)
        res = adjust_backdoor(df, model)
        a = 55
        assert False

    def test_canonical_collider(self):
        model_str = SAMPLE_DAGS["Confounder"]
        model = parse_model_string(model_str)
        model.update_node("Z", NodeAttribute.ADJUSTED)

        df, true_effect = generate_confounder_data(n=10000)
        res = adjust_backdoor(df, model)

        a = 5

        assert False
