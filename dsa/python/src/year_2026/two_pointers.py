"""Two pointer technique problems."""

from typing_extensions import Optional, Tuple


def two_sum_sorted(arr: list[int], target: int) -> Optional[Tuple[int, int]]:
    """Find two indices in sorted arr whose values sum to target. Return tuple or None. O(1) space."""
    left, right = 0, len(arr) - 1
    while left < right:
        if target > arr[left] + arr[right]:
            left += 1
        elif target < arr[left] + arr[right]:
            right -= 1
        else:
            return left, right


def three_sum(arr):
    """Find all unique triplets that sum to zero. Return list of triplets."""
    raise NotImplementedError


def container_with_most_water(heights):
    """Return max water area between two vertical lines. Width * min(heights)."""
    raise NotImplementedError
