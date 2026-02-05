"""Binary search variations beyond basic search."""


def find_first_occurrence(arr, target):
    """Return index of first (leftmost) occurrence of target in sorted arr, or -1 if not found."""
    left, right = 0, len(arr) - 1
    location = -1
    while left <= right:
        mid = (left + right) // 2
        if target > arr[mid]:
            left = mid + 1
        elif target < arr[mid]:
            right = mid - 1
        else:
            location = mid
            right = mid - 1
    return location


def find_last_occurrence(arr, target):
    """Return index of last (rightmost) occurrence of target in sorted arr, or -1 if not found."""
    left, right = 0, len(arr) - 1
    location = -1
    while left <= right:
        mid = (left + right) // 2
        if target > arr[mid]:
            left = mid + 1
        elif target < arr[mid]:
            right = mid - 1
        else:
            location = mid
            left = mid + 1
    return location


def search_insert_position(arr, target):
    """Return index where target is found, or where it would be inserted to keep arr sorted."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if target > arr[mid]:
            left = mid + 1
        elif target < arr[mid]:
            right = mid - 1
        else:
            return mid
    return left


def search_rotated_sorted_array(arr, target):
    """Find target in a sorted array that has been rotated. Return index or -1."""
    raise NotImplementedError


def find_min_rotated_sorted_array(arr):
    """Find the minimum element in a rotated sorted array (no duplicates)."""
    raise NotImplementedError


def find_peak_element(arr):
    """Return index of any peak element (greater than neighbors). Edges are -infinity."""
    raise NotImplementedError


def koko_eating_bananas(piles, h):
    """Return minimum eating speed k to finish all piles within h hours."""
    raise NotImplementedError


def capacity_to_ship_packages(weights, days):
    """Return minimum ship capacity to ship all packages within given days."""
    raise NotImplementedError
