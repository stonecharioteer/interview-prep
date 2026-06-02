import pytest

from src.year_2026 import heap

pytestmark = pytest.mark.heap


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMinHeap:
    def test_insert_extract(self):
        h = heap.MinHeap()
        h.insert(5)
        h.insert(3)
        h.insert(7)
        assert h.extract_min() == 3
        assert h.extract_min() == 5
        assert h.extract_min() == 7

    def test_peek(self):
        h = heap.MinHeap()
        h.insert(10)
        h.insert(5)
        assert h.peek() == 5
        assert h.peek() == 5  # still there

    def test_size(self):
        h = heap.MinHeap()
        assert h.size() == 0
        h.insert(1)
        assert h.size() == 1

    def test_empty(self):
        h = heap.MinHeap()
        assert h.extract_min() is None
        assert h.peek() is None


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMaxHeap:
    def test_insert_extract(self):
        h = heap.MaxHeap()
        h.insert(5)
        h.insert(3)
        h.insert(7)
        assert h.extract_max() == 7
        assert h.extract_max() == 5
        assert h.extract_max() == 3


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestHeapify:
    def test_simple(self):
        arr = [5, 3, 7, 1, 4]
        heap.heapify(arr)
        # After heapify, arr[0] should be minimum
        assert arr[0] == 1


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestHeapSort:
    def test_simple(self):
        assert heap.heap_sort([3, 1, 4, 1, 5, 9, 2, 6]) == [1, 1, 2, 3, 4, 5, 6, 9]

    def test_empty(self):
        assert heap.heap_sort([]) == []


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestKthLargest:
    def test_simple(self):
        assert heap.kth_largest([3, 2, 1, 5, 6, 4], 2) == 5

    def test_k_equals_one(self):
        assert heap.kth_largest([3, 2, 1, 5, 6, 4], 1) == 6


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestKthSmallest:
    def test_simple(self):
        assert heap.kth_smallest([3, 2, 1, 5, 6, 4], 2) == 2


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTopKFrequent:
    def test_simple(self):
        result = heap.top_k_frequent([1, 1, 1, 2, 2, 3], 2)
        assert sorted(result) == [1, 2]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSlidingWindowMaximum:
    def test_simple(self):
        assert heap.sliding_window_maximum([1, 3, -1, -3, 5, 3, 6, 7], 3) == [
            3,
            3,
            5,
            5,
            6,
            7,
        ]
