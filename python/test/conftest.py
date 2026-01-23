"""Pytest configuration and shared fixtures for interview prep tests."""

import pytest


def pytest_configure(config):
    """Register custom markers for test organization."""
    # Data structures
    config.addinivalue_line("markers", "arrays: array manipulation exercises")
    config.addinivalue_line("markers", "linked_list: linked list exercises")
    config.addinivalue_line("markers", "maps: hashmap/dictionary exercises")
    config.addinivalue_line("markers", "trees: tree traversal and manipulation")
    config.addinivalue_line("markers", "stack: stack data structure exercises")
    config.addinivalue_line("markers", "queue: queue data structure exercises")
    config.addinivalue_line("markers", "heap: heap/priority queue exercises")
    config.addinivalue_line("markers", "trie: trie data structure exercises")
    config.addinivalue_line("markers", "graph: graph algorithms")
    config.addinivalue_line("markers", "union_find: union-find/disjoint set exercises")

    # Techniques
    config.addinivalue_line("markers", "recursion: recursive problem solving")
    config.addinivalue_line("markers", "sorting: sorting algorithms")
    config.addinivalue_line("markers", "binary_search: binary search variations")
    config.addinivalue_line("markers", "two_pointers: two pointer technique")
    config.addinivalue_line("markers", "sliding_window: sliding window technique")
    config.addinivalue_line("markers", "monotonic_stack: monotonic stack problems")
    config.addinivalue_line("markers", "backtracking: backtracking exercises")
    config.addinivalue_line("markers", "greedy: greedy algorithm exercises")
    config.addinivalue_line("markers", "dp: dynamic programming exercises")

    # Other
    config.addinivalue_line("markers", "bits: bit manipulation exercises")
    config.addinivalue_line("markers", "math: mathematical operations")
    config.addinivalue_line("markers", "string_matching: string matching algorithms")
    config.addinivalue_line("markers", "conversions: data structure conversions")

    # Meta markers
    config.addinivalue_line("markers", "slow: tests that take longer to run")
