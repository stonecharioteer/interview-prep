"""Heap (priority queue) data structure and heap-based problems."""


class MinHeap:
    """Min-heap where parent is always smaller than children."""

    def __init__(self):
        raise NotImplementedError

    def insert(self, value):
        """Add value to the heap, maintaining heap property."""
        raise NotImplementedError

    def extract_min(self):
        """Remove and return the minimum value. Return None if empty."""
        raise NotImplementedError

    def peek(self):
        """Return the minimum value without removing it. Return None if empty."""
        raise NotImplementedError

    def size(self):
        """Return the number of elements in the heap."""
        raise NotImplementedError


class MaxHeap:
    """Max-heap where parent is always larger than children."""

    def __init__(self):
        raise NotImplementedError

    def insert(self, value):
        """Add value to the heap, maintaining heap property."""
        raise NotImplementedError

    def extract_max(self):
        """Remove and return the maximum value. Return None if empty."""
        raise NotImplementedError

    def peek(self):
        """Return the maximum value without removing it. Return None if empty."""
        raise NotImplementedError

    def size(self):
        """Return the number of elements in the heap."""
        raise NotImplementedError


def heapify(arr):
    """Convert arr into a min-heap in-place."""
    raise NotImplementedError


def heap_sort(arr):
    """Return a new sorted list using heap sort."""
    raise NotImplementedError


def kth_largest(arr, k):
    """Return the kth largest element in arr. k=1 is the maximum."""
    raise NotImplementedError


def kth_smallest(arr, k):
    """Return the kth smallest element in arr. k=1 is the minimum."""
    raise NotImplementedError


def merge_k_sorted_lists(lists):
    """Merge k sorted lists into one sorted list."""
    raise NotImplementedError


def top_k_frequent(nums, k):
    """Return the k most frequent elements in nums."""
    raise NotImplementedError


def sliding_window_maximum(nums, k):
    """Return max value in each sliding window of size k."""
    raise NotImplementedError
