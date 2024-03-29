import sample_dags
import utils
from src_py.causal_graph import NodeAttribute, parse_model_string, parse_edges, get_query_from_graph


class TestParsingOfEdges:
    def test_parse_simple_edge(self):
        edges = parse_edges("a->b")
        assert len(edges) == 1
        src, dst = edges[0]
        assert src == 'a'
        assert dst == 'b'

    def test_parse_edge_with_attributes(self):
        # attributes are kept with the node and are not further pared
        edges = parse_edges("a[T]->b[O]")
        assert len(edges) == 1
        src, dst = edges[0]
        assert src == 'a[T]'
        assert dst == 'b[O]'

    def test_parse_edge_with_meta_attribute(self):
        assert False

    def test_parse_single_edges_per_line(self):
        assert False

    def test_parse_multiple_edges_per_line(self):
        assert False

    def test_parse_edge_with_unobserved_confounding(self):
        assert False

    def test_parse_edge_inverse_direction(self):
        assert False

    def test_parse_edge_chain(self):
        assert False


class Test_BlockedPath:
    def test_simple_chain(self):
        model = parse_model_string(["x->b", "b->y"])
        path = utils.node_path_to_edge_path(["x", "b", "y"], model.graph)
        is_blocked = model.is_path_blocked(path)
        assert not is_blocked

    def test_long_chain(self):
        model = parse_model_string(["x->a", "a->b", "b->c", "c->d", "d->y"])
        path = utils.node_path_to_edge_path(["x", "a", "b", "c", "d", "y"], model.graph)
        is_blocked = model.is_path_blocked(path)
        assert not is_blocked

    def test_simple_fork(self):
        model = parse_model_string(["b->x", "b->y"])
        path = utils.node_path_to_edge_path(['x', 'b', 'y'], model.graph)
        is_blocked = model.is_path_blocked(path)
        assert not is_blocked

    def test_fork_chain_mix(self):
        model = parse_model_string(["x<-a", "a<-b", "c->b", "c->d", "d->y"])
        path = utils.node_path_to_edge_path(["x", "a", "b", "c", "d", "y"], model.graph)
        is_blocked = model.is_path_blocked(path)
        assert not is_blocked

    def test_simple_collider(self):
        model = parse_model_string(["x->b", "y->b"])
        path = utils.node_path_to_edge_path(['x', 'b', 'y'], model.graph)
        is_blocked = model.is_path_blocked(path)
        assert is_blocked

    def test_collider_descendant(self):
        model = parse_model_string(["x->b", "y->b", "b->c", "b->d"])
        path = [('x', 'b'), ('y', 'b')]

        is_blocked = model.is_path_blocked(path, conditioning_set={'c'})
        assert not is_blocked

    def test_m_bias(self):
        model = parse_model_string([
            "U₁[unobserved] -> Z",
            "U₁[unobserved] -> Y[outcome]",
            "U₂[unobserved] -> A[treatment]",
            "U₂[unobserved] -> Z",
            "A -> Y"
        ])
        path = utils.node_path_to_edge_path(["A", "U₂", "Z", "U₁", "Y"], model.graph)
        is_blocked = model.is_path_blocked(path, conditioning_set=None)
        assert is_blocked


class Test_DSeparation:
    def test_shries_platt_no_adjustment(self):
        model = parse_model_string(sample_dags.SHRIER_PLATT_2008)
        biasing_paths = model.get_biasing_paths()
        assert len(biasing_paths) == 3

    def test_shries_platt_coach_fitness(self):
        model = parse_model_string(sample_dags.SHRIER_PLATT_2008)
        model.update_node("Coach", NodeAttribute.ADJUSTED)
        model.update_node("Fitness Level", NodeAttribute.ADJUSTED)
        biasing_paths = model.get_biasing_paths(as_edge_list=True)
        assert len(biasing_paths) == 0


class TestQueryFromCausalGraph:
    def test_simple_collider(self):
        graph = parse_model_string([
            "X -> Y",
            "Z -> X",
            "Z -> Y"
        ])
        query = get_query_from_graph(graph, 'X', 'Y')
        assert query == "P(Y|do(X))"
