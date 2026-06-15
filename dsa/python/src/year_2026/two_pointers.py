"""Two pointer technique problems."""

from typing_extensions import Optional, Tuple, List


def two_sum_sorted(arr: List[int], target: int) -> Optional[Tuple[int, int]]:
    """Find two indices in sorted arr whose values sum to target. Return tuple or None. O(1) space."""
    left, right = 0, len(arr) - 1
    while left < right:
        if target > arr[left] + arr[right]:
            left += 1
        elif target < arr[left] + arr[right]:
            right -= 1
        else:
            return left, right


def three_sum(arr: List[int]) -> List[List[int]]:
    """Find all unique triplets that sum to zero. Return list of triplets."""
    n = len(arr)
    arr = sorted(arr)
    result = []
    for ix in range(n):
        if ix > 0 and arr[ix] == arr[ix - 1]:
            continue
        left, right = ix + 1, n - 1
        while left < right:
            s = arr[ix] + arr[left] + arr[right]
            if s == 0:
                result.append([arr[ix], arr[left], arr[right]])
                left += 1
                right -= 1
                while left < right and arr[left] == arr[left - 1]:
                    left += 1
                while left < right and arr[right] == arr[right + 1]:
                    right -= 1

            elif s > 0:
                right -= 1
            elif s < 0:
                left += 1
    return result


def container_with_most_water(heights):
    """Return max water area between two vertical lines. Width * min(heights)."""
    raise NotImplementedError
