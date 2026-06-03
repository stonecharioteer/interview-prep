"""Graph data structure and graph algorithms."""


class Graph:
    """Graph data structure."""

    def __init__(self, directed=False):
        raise NotImplementedError

    def add_edge(self, u, v, weight=1):
        """Add edge from u to v (and v to u if undirected)."""
        raise NotImplementedError

    def has_edge(self, u, v):
        """Return True if edge exists from u to v."""
        raise NotImplementedError

    def neighbors(self, node):
        """Return list of neighbors of the given node."""
        raise NotImplementedError

    def nodes(self):
        """Return list of all nodes in the graph."""
        raise NotImplementedError


def dfs_traversal(graph, start):
    """Return list of nodes in DFS order starting from start."""
    raise NotImplementedError


def bfs_traversal(graph, start):
    """Return list of nodes in BFS order starting from start."""
    raise NotImplementedError


def is_connected(graph):
    """Return True if undirected graph is connected (all nodes reachable from any node)."""
    raise NotImplementedError


def count_connected_components(graph):
    """Return number of connected components in undirected graph."""
    raise NotImplementedError


def detect_cycle_directed(graph):
    """Return True if directed graph contains a cycle."""
    raise NotImplementedError


def detect_cycle_undirected(graph):
    """Return True if undirected graph contains a cycle."""
    raise NotImplementedError


def shortest_path_unweighted(graph, start, end):
    """Return shortest path (list of nodes) from start to end. None if no path."""
    raise NotImplementedError


def shortest_path_dijkstra(graph, start, end):
    """Return shortest path in weighted graph. None if no path."""
    raise NotImplementedError


def all_pairs_shortest_path(graph):
    """Return matrix of shortest distances between all pairs."""
    raise NotImplementedError


def topological_sort_kahn(graph):
    """Return topological ordering. None if cycle exists."""
    raise NotImplementedError


def topological_sort_dfs(graph):
    """Return topological ordering. None if cycle exists."""
    raise NotImplementedError


def is_bipartite(graph):
    """Return True if graph can be 2-colored (bipartite)."""
    raise NotImplementedError


def kruskals_mst(graph):
    """Return edges of minimum spanning tree using Kruskal's algorithm."""
    raise NotImplementedError


def prims_mst(graph):
    """Return edges of minimum spanning tree using Prim's algorithm."""
    raise NotImplementedError
