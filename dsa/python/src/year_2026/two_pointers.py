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
    """Return max water area between two vertical lines.

    Given an array where each element represents the height of a vertical line,
    find two lines that together with the x-axis form a container that can
    hold the most water.

    The area between two lines at indices i and j is:
        area = (j - i) * min(heights[i], heights[j])

    The width is the horizontal distance between the lines (j - i).
    The height is limited by the shorter of the two lines.

    Approach: two pointers starting at the ends. At each step, the shorter
    line limits the area, so move it inward hoping to find a taller line.
    The taller line can never produce a larger area with the current pair
    since width is already maximal, so moving it inward is safe to skip.
    """
    left = 0
    right = len(heights) - 1
    best_seen = 0
    while left < right:
        area = (right - left) * min(heights[left], heights[right])
        if area > best_seen:
            best_seen = area
        if heights[left] < heights[right]:
            left += 1  # move left wall inwards
        elif heights[right] < heights[left]:
            right -= 1
        else:
            left += 1
            right -= 1
    return best_seen
