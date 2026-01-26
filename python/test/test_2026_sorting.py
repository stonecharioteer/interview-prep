import random

import pytest

from src.year_2026 import sorting

pytestmark = pytest.mark.sorting


class TestBubbleSort:
    def test_simple(self):
        length = random.randint(5, 20)
        arr = [random.randint(-100, 100) for _ in range(length)]
        expected = sorted(arr)
        sorting.bubble_sort(arr)
        assert arr == expected

    def test_already_sorted(self):
        length = random.randint(5, 20)
        arr = sorted([random.randint(-100, 100) for _ in range(length)])
        expected = list(arr)
        sorting.bubble_sort(arr)
        assert arr == expected

    def test_reverse_sorted(self):
        length = random.randint(5, 20)
        arr = sorted([random.randint(-100, 100) for _ in range(length)], reverse=True)
        expected = sorted(arr)
        sorting.bubble_sort(arr)
        assert arr == expected

    def test_single_element(self):
        value = random.randint(-1000, 1000)
        arr = [value]
        sorting.bubble_sort(arr)
        assert arr == [value]

    def test_random(self):
        length = random.randint(10, 100)
        arr = [random.randint(-1000, 1000) for _ in range(length)]
        expected = sorted(arr)
        sorting.bubble_sort(arr)
        assert arr == expected


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSelectionSort:
    def test_simple(self):
        length = random.randint(5, 20)
        arr = [random.randint(-100, 100) for _ in range(length)]
        expected = sorted(arr)
        sorting.selection_sort(arr)
        assert arr == expected

    def test_with_negatives(self):
        length = random.randint(5, 20)
        arr = [
            random.randint(-100, -1) if i % 2 == 0 else random.randint(1, 100)
            for i in range(length)
        ]
        expected = sorted(arr)
        sorting.selection_sort(arr)
        assert arr == expected

    def test_random(self):
        length = random.randint(10, 100)
        arr = [random.randint(-1000, 1000) for _ in range(length)]
        expected = sorted(arr)
        sorting.selection_sort(arr)
        assert arr == expected


class TestInsertionSort:
    def test_simple(self):
        length = random.randint(5, 20)
        arr = [random.randint(-100, 100) for _ in range(length)]
        expected = sorted(arr)
        sorting.insertion_sort(arr)
        assert arr == expected

    def test_nearly_sorted(self):
        length = random.randint(10, 30)
        arr = sorted([random.randint(-100, 100) for _ in range(length)])
        # Swap a few adjacent pairs to make it nearly sorted
        swaps = random.randint(1, max(1, length // 5))
        for _ in range(swaps):
            i = random.randint(0, length - 2)
            arr[i], arr[i + 1] = arr[i + 1], arr[i]
        expected = sorted(arr)
        sorting.insertion_sort(arr)
        assert arr == expected

    def test_random(self):
        length = random.randint(10, 100)
        arr = [random.randint(-1000, 1000) for _ in range(length)]
        expected = sorted(arr)
        sorting.insertion_sort(arr)
        assert arr == expected


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMergeSort:
    def test_simple(self):
        length = random.randint(5, 20)
        arr = [random.randint(-100, 100) for _ in range(length)]
        assert sorting.merge_sort(arr) == sorted(arr)

    def test_empty(self):
        assert sorting.merge_sort([]) == []

    def test_single(self):
        value = random.randint(-1000, 1000)
        assert sorting.merge_sort([value]) == [value]

    def test_random(self):
        length = random.randint(10, 100)
        arr = [random.randint(-1000, 1000) for _ in range(length)]
        assert sorting.merge_sort(arr) == sorted(arr)


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestQuickSort:
    def test_simple(self):
        length = random.randint(5, 20)
        arr = [random.randint(-100, 100) for _ in range(length)]
        assert sorting.quick_sort(arr) == sorted(arr)

    def test_empty(self):
        assert sorting.quick_sort([]) == []

    def test_duplicates(self):
        length = random.randint(5, 20)
        value = random.randint(-100, 100)
        arr = [value] * length
        assert sorting.quick_sort(arr) == arr

    def test_random(self):
        length = random.randint(10, 100)
        arr = [random.randint(-1000, 1000) for _ in range(length)]
        assert sorting.quick_sort(arr) == sorted(arr)


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestCountingSort:
    def test_simple(self):
        length = random.randint(5, 20)
        arr = [random.randint(0, 100) for _ in range(length)]
        assert sorting.counting_sort(arr) == sorted(arr)

    def test_zeros(self):
        length = random.randint(5, 20)
        arr = [
            0 if random.random() < 0.5 else random.randint(1, 10) for _ in range(length)
        ]
        assert sorting.counting_sort(arr) == sorted(arr)

    def test_random(self):
        length = random.randint(10, 100)
        arr = [random.randint(0, 1000) for _ in range(length)]
        assert sorting.counting_sort(arr) == sorted(arr)


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestRadixSort:
    def test_simple(self):
        length = random.randint(5, 20)
        arr = [random.randint(0, 1000) for _ in range(length)]
        assert sorting.radix_sort(arr) == sorted(arr)

    def test_single_digit(self):
        length = random.randint(5, 20)
        arr = [random.randint(0, 9) for _ in range(length)]
        assert sorting.radix_sort(arr) == sorted(arr)

    def test_random(self):
        length = random.randint(10, 100)
        arr = [random.randint(0, 10000) for _ in range(length)]
        assert sorting.radix_sort(arr) == sorted(arr)
