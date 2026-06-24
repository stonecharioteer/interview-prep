"""Heap (priority queue) data structure and heap-based problems."""


class MinHeap:
    """Min-heap where parent is always smaller than children."""

    def __init__(self):
        self._data = []

    def _parent(self, i):
        """Returns the parent of a node"""
        return (i - 1) // 2

    def insert(self, value):
        """Add value to the heap, maintaining heap property."""
        self._data.append(value)
        index = len(self._data) - 1

        while index > 0:
            if self._data[self._parent(index)] <= self._data[index]:
                break

            self._data[self._parent(index)], self._data[index] = (
                self._data[index],
                self._data[self._parent(index)],
            )
            index = self._parent(index)

    def extract_min(self):
        """Remove and return the minimum value. Return None if empty."""
        if not self._data:
            return None
        min_value = self._data[0]
        if len(self._data) == 1:
            _ = self._data.pop()
            return min_value
        self._data[0] = self._data.pop()
        self._sift_down(0)
        return min_value

    def _sift_down(self, position):
        "moves a value down to its position"
        while True:
            left, right = self._children(position)
            smallest = position
            if self.size() > left and self._data[left] < self._data[smallest]:
                smallest = left
            if self.size() > right and self._data[right] < self._data[smallest]:
                smallest = right
            if smallest == position:
                break
            self._data[position], self._data[smallest] = (
                self._data[smallest],
                self._data[position],
            )
            position = smallest

    def _children(self, position):
        left = 2 * position + 1
        right = left + 1
        return left, right

    def peek(self):
        """Return the minimum value without removing it. Return None if empty."""

        return self._data[0] if self._data else None

    def size(self):
        """Return the number of elements in the heap."""
        return len(self._data)


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
    i = len(arr) - 1
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
