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


def insertion_sort(arr):
    """Sort arr in-place using insertion sort."""
    sorted_index = 0
    while sorted_index < len(arr) - 1:
        for ix, i in enumerate(arr[sorted_index + 1 :]):
            if arr[sorted_index] <= arr[ix]:
                sorted_index = i


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
