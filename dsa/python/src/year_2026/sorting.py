"""Sorting algorithm implementations from basic to advanced."""

from typing import List
from year_2026.types import Comparable


def bubble_sort(arr: List[Comparable]) -> None:
    """Sort arr in-place using bubble sort."""
    # Iterate through the list until it's sorted
    for _ in range(len(arr)):
        for j in range(len(arr) - 1):
            if arr[j + 1] < arr[j]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


def selection_sort(arr: List[Comparable]) -> None:
    """Sort arr in-place using selection sort."""
    for ix in range(len(arr) - 1):
        min_val = arr[ix]
        min_index = ix
        for jx in range(ix + 1, len(arr)):
            if arr[jx] < min_val:
                min_val = arr[jx]
                min_index = jx
        arr[ix], arr[min_index] = arr[min_index], arr[ix]


def insertion_sort(arr: List[Comparable]):
    """Sort arr in-place using insertion sort.
    TIP: Insertion sort repeatedly swaps adjacent elements
    leftward until order is restored."""
    for i in range(len(arr)):
        for j in range(i, 0, -1):
            if arr[j - 1] > arr[j]:
                arr[j - 1], arr[j] = arr[j], arr[j - 1]
            else:
                break


def merge_sort(arr: List[Comparable]) -> List[Comparable]:
    """Return a new sorted list using merge sort."""

    def merge_sorted_array(
        x: List[Comparable], y: List[Comparable]
    ) -> List[Comparable]:
        ix = 0
        iy = 0
        merged = []
        while ix < (len(x)) and iy < (len(y)):
            if x[ix] < y[iy]:
                merged.append(x[ix])
                ix += 1
            elif y[iy] < x[ix]:
                merged.append(y[iy])
                iy += 1
            else:
                merged.append(y[iy])
                merged.append(x[ix])
                ix += 1
                iy += 1
        if ix < len(x):
            merged.extend(x[ix:])
        if iy < len(y):
            merged.extend(y[iy:])
        return merged

    if len(arr) <= 1:
        return arr
    else:
        mid = len(arr) // 2
        a, b = arr[:mid], arr[mid:]
        return merge_sorted_array(merge_sort(a), merge_sort(b))


def quick_sort(arr):
    """Return a new sorted list using quick sort."""
    raise NotImplementedError


def counting_sort(arr):
    """Return a new sorted list using counting sort. Only for non-negative integers."""
    raise NotImplementedError


def radix_sort(arr):
    """Return a new sorted list using radix sort."""
    raise NotImplementedError
