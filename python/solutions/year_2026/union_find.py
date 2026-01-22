"""Union-Find (Disjoint Set Union) data structure."""


class UnionFind:
    """Union-Find (Disjoint Set Union) data structure."""

    def __init__(self, n):
        """Initialize n elements (0 to n-1)."""
        raise NotImplementedError

    def find(self, x):
        """Return the representative of the set containing x."""
        raise NotImplementedError

    def union(self, x, y):
        """Merge the sets containing x and y. Return True if they were different sets."""
        raise NotImplementedError

    def connected(self, x, y):
        """Return True if x and y are in the same set."""
        raise NotImplementedError

    def count_components(self):
        """Return the number of disjoint sets."""
        raise NotImplementedError


def detect_cycle_undirected_uf(edges, n):
    """Detect cycle in undirected graph using Union-Find. edges is list of (u, v) tuples."""
    raise NotImplementedError
