import causal_graph
from src_py.causal_graph import parse_model_string


class Test_BlockedPath:
    def test_simple_chain(self):
        model = parse_model_string(["x->b", "b->y"])
        path = [('x', 'b'), ('b', 'y')]
        is_blocked = model.is_path_blocked(path)
        assert not is_blocked

    def test_simple_fork(self):
        model = parse_model_string(["b->x", "b->y"])
        path = [('b', 'x'), ('b', 'y')]
        is_blocked = model.is_path_blocked(path)
        assert not is_blocked

    def test_simple_collider(self):
        model = parse_model_string(["x->b", "y->b"])
        path = [('x', 'b'), ('y', 'b')]
        is_blocked = model.is_path_blocked(path)
        assert is_blocked

    def test_collider_descendant(self):
        model = parse_model_string(["x->b", "y->b", "b->c", "b->d"])
        path = [('x', 'b'), ('y', 'b')]
        is_blocked = model.is_path_blocked(path, conditioning_set={'c'})
        assert not is_blocked


