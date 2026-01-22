import pytest

from solutions.year_2026 import graph

pytestmark = pytest.mark.graph


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestGraph:
    def test_add_edge_undirected(self):
        g = graph.Graph(directed=False)
        g.add_edge(1, 2)
        assert g.has_edge(1, 2) is True
        assert g.has_edge(2, 1) is True

    def test_add_edge_directed(self):
        g = graph.Graph(directed=True)
        g.add_edge(1, 2)
        assert g.has_edge(1, 2) is True
        assert g.has_edge(2, 1) is False

    def test_neighbors(self):
        g = graph.Graph()
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        assert sorted(g.neighbors(1)) == [2, 3]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestDfsTraversal:
    def test_simple(self):
        g = graph.Graph()
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g.add_edge(2, 4)
        result = graph.dfs_traversal(g, 1)
        assert 1 in result
        assert len(result) == 4


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestBfsTraversal:
    def test_simple(self):
        g = graph.Graph()
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g.add_edge(2, 4)
        result = graph.bfs_traversal(g, 1)
        assert result[0] == 1  # start node first
        assert len(result) == 4


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestIsConnected:
    def test_connected(self):
        g = graph.Graph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        assert graph.is_connected(g) is True

    def test_disconnected(self):
        g = graph.Graph()
        g.add_edge(1, 2)
        g.add_edge(3, 4)
        assert graph.is_connected(g) is False


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestCountConnectedComponents:
    def test_two_components(self):
        g = graph.Graph()
        g.add_edge(1, 2)
        g.add_edge(3, 4)
        assert graph.count_connected_components(g) == 2


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestDetectCycleDirected:
    def test_has_cycle(self):
        g = graph.Graph(directed=True)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)
        assert graph.detect_cycle_directed(g) is True

    def test_no_cycle(self):
        g = graph.Graph(directed=True)
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        assert graph.detect_cycle_directed(g) is False


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestDetectCycleUndirected:
    def test_has_cycle(self):
        g = graph.Graph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)
        assert graph.detect_cycle_undirected(g) is True


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestShortestPathUnweighted:
    def test_simple(self):
        g = graph.Graph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(1, 3)
        path = graph.shortest_path_unweighted(g, 1, 3)
        assert path == [1, 3]

    def test_no_path(self):
        g = graph.Graph()
        g.add_edge(1, 2)
        g.add_edge(3, 4)
        assert graph.shortest_path_unweighted(g, 1, 4) is None


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTopologicalSortKahn:
    def test_simple(self):
        g = graph.Graph(directed=True)
        g.add_edge(1, 2)
        g.add_edge(1, 3)
        g.add_edge(2, 4)
        g.add_edge(3, 4)
        result = graph.topological_sort_kahn(g)
        assert result.index(1) < result.index(2)
        assert result.index(1) < result.index(3)
        assert result.index(2) < result.index(4)


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestIsBipartite:
    def test_bipartite(self):
        g = graph.Graph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 4)
        g.add_edge(4, 1)
        assert graph.is_bipartite(g) is True

    def test_not_bipartite(self):
        g = graph.Graph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)
        assert graph.is_bipartite(g) is False
