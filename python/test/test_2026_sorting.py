import pytest

from solutions.year_2026 import sorting

pytestmark = pytest.mark.sorting


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestBubbleSort:
    def test_simple(self):
        arr = [3, 1, 4, 1, 5]
        sorting.bubble_sort(arr)
        assert arr == [1, 1, 3, 4, 5]

    def test_already_sorted(self):
        arr = [1, 2, 3, 4, 5]
        sorting.bubble_sort(arr)
        assert arr == [1, 2, 3, 4, 5]

    def test_reverse_sorted(self):
        arr = [5, 4, 3, 2, 1]
        sorting.bubble_sort(arr)
        assert arr == [1, 2, 3, 4, 5]

    def test_single_element(self):
        arr = [42]
        sorting.bubble_sort(arr)
        assert arr == [42]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSelectionSort:
    def test_simple(self):
        arr = [3, 1, 4, 1, 5]
        sorting.selection_sort(arr)
        assert arr == [1, 1, 3, 4, 5]

    def test_with_negatives(self):
        arr = [3, -1, 4, -1, 5]
        sorting.selection_sort(arr)
        assert arr == [-1, -1, 3, 4, 5]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestInsertionSort:
    def test_simple(self):
        arr = [3, 1, 4, 1, 5]
        sorting.insertion_sort(arr)
        assert arr == [1, 1, 3, 4, 5]

    def test_nearly_sorted(self):
        arr = [1, 2, 4, 3, 5]
        sorting.insertion_sort(arr)
        assert arr == [1, 2, 3, 4, 5]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMergeSort:
    def test_simple(self):
        assert sorting.merge_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]

    def test_empty(self):
        assert sorting.merge_sort([]) == []

    def test_single(self):
        assert sorting.merge_sort([42]) == [42]

    def test_large(self):
        import random
        arr = [random.randint(0, 1000) for _ in range(100)]
        assert sorting.merge_sort(arr) == sorted(arr)


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestQuickSort:
    def test_simple(self):
        assert sorting.quick_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]

    def test_empty(self):
        assert sorting.quick_sort([]) == []

    def test_duplicates(self):
        assert sorting.quick_sort([5, 5, 5, 5]) == [5, 5, 5, 5]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestCountingSort:
    def test_simple(self):
        assert sorting.counting_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]

    def test_zeros(self):
        assert sorting.counting_sort([0, 0, 1, 0]) == [0, 0, 0, 1]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestRadixSort:
    def test_simple(self):
        assert sorting.radix_sort([170, 45, 75, 90, 802, 24, 2, 66]) == [2, 24, 45, 66, 75, 90, 170, 802]

    def test_single_digit(self):
        assert sorting.radix_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
