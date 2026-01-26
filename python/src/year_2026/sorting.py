"""Sorting algorithm implementations from basic to advanced."""

from typing import List


def bubble_sort(arr: List[int]) -> None:
    """Sort arr in-place using bubble sort."""
    # Iterate through the list until it's sorted
    for _ in range(len(arr)):
        for j in range(len(arr) - 1):
            if arr[j + 1] < arr[j]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def selection_sort(arr: List[int]) -> None:
    """Sort arr in-place using selection sort."""
    raise NotImplementedError


def insertion_sort(arr: List[int]):
    """Sort arr in-place using insertion sort.
    TIP: Insertion sort repeatedly swaps adjacent elements
    leftward until order is restored."""
    for i in range(len(arr)):
        for j in range(i, 0, -1):
            if arr[j - 1] > arr[j]:
                arr[j - 1], arr[j] = arr[j], arr[j - 1]
            else:
                break


def merge_sort(arr):
    """Return a new sorted list using merge sort."""
    raise NotImplementedError


def quick_sort(arr):
    """Return a new sorted list using quick sort."""
    raise NotImplementedError


def counting_sort(arr):
    """Return a new sorted list using counting sort. Only for non-negative integers."""
    raise NotImplementedError


def radix_sort(arr):
    """Return a new sorted list using radix sort."""
    raise NotImplementedError
