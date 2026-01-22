import pytest

from solutions.year_2026 import union_find

pytestmark = pytest.mark.union_find


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestUnionFind:
    def test_initial_components(self):
        uf = union_find.UnionFind(5)
        assert uf.count_components() == 5

    def test_union(self):
        uf = union_find.UnionFind(5)
        uf.union(0, 1)
        assert uf.connected(0, 1) is True
        assert uf.count_components() == 4

    def test_transitive(self):
        uf = union_find.UnionFind(5)
        uf.union(0, 1)
        uf.union(1, 2)
        assert uf.connected(0, 2) is True

    def test_not_connected(self):
        uf = union_find.UnionFind(5)
        uf.union(0, 1)
        assert uf.connected(0, 3) is False

    def test_find(self):
        uf = union_find.UnionFind(5)
        uf.union(0, 1)
        assert uf.find(0) == uf.find(1)


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestDetectCycleUndirectedUF:
    def test_has_cycle(self):
        edges = [(0, 1), (1, 2), (2, 0)]
        assert union_find.detect_cycle_undirected_uf(edges, 3) is True

    def test_no_cycle(self):
        edges = [(0, 1), (1, 2)]
        assert union_find.detect_cycle_undirected_uf(edges, 3) is False

    def test_tree(self):
        edges = [(0, 1), (0, 2), (1, 3), (1, 4)]
        assert union_find.detect_cycle_undirected_uf(edges, 5) is False
