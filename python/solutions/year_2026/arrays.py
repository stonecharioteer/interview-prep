import random
from typing import List, Optional


def get_random_list(n: int = 50):
    """Generate a list of n random integers between 0 and 100."""
    return [random.randint(0, 100) for _ in range(n)]


def print_a_list(x: List[int]):
    """Print each element of the list on a separate line."""
    for i in x:
        print(i)


def get_max_in_list(x: List[int]):
    """Return the maximum value in the list."""
    m = None
    for i in x:
        if m is None or i > m:
            m = i
    return m


def get_sum_of_list(x: List[int]):
    """Return the sum of all elements in the list."""
    s = 0
    for i in x:
        s += i
    return s


def is_n_in_list(x: List[int], n: int):
    """Check if n exists in the list."""
    print(f"{n=}")
    for i in x:
        if i == n:
            return True
    return False


def get_min_in_list(x: List[int]):
    """Return the minimum value in the list."""
    m = None
    for i in x:
        if m is None or m > i:
            m = i
    return m


def get_average_of_list(x: List[int]) -> float:
    """Return the average of all elements in the list."""
    s = 0
    for i in x:
        s += i
    return s / len(x)


def count_instances(x: List[int], n: int) -> int:
    """Count how many times n appears in the list."""
    counter = 0
    for i in x:
        if i == n:
            counter += 1
    return counter


def find_index(x: List[int], n: int) -> Optional[int]:
    """Return the index of the first occurrence of n, or None if not found."""
    for ix, i in enumerate(x):
        if i == n:
            return ix


def find_all_indicies(x: List[int], n: int) -> List:
    """Return a list of all indices where n appears."""
    indices = []
    for ix, i in enumerate(x):
        if i == n:
            indices.append(ix)
    return indices


def array_reversed(x: List[int]) -> List[int]:
    """Return a new list with elements in reverse order."""
    return x[::-1]


def array_reversed_in_place(x: List[int]):
    """Reverse the list in place, modifying the original list."""
    for ix in range(len(x) // 2):
        x[len(x) - 1 - ix], x[ix] = x[ix], x[len(x) - 1 - ix]


def is_sorted(x: List[int]) -> bool:
    """Check if the list is sorted in ascending order."""
    raise NotImplementedError


def binary_search(x: List[int], target: int) -> Optional[int]:
    """Find index of target in sorted list, return None if not found."""
    raise NotImplementedError


def merge_sorted(a: List[int], b: List[int]) -> List[int]:
    """Merge two sorted lists into a single sorted list."""
    raise NotImplementedError


def rotate_k(x: List[int], k: int) -> List[int]:
    """Rotate list to the right by k positions."""
    raise NotImplementedError


def two_sum(x: List[int], target: int) -> Optional[tuple[int, int]]:
    """Find two indices whose values sum to target, return None if not found."""
    raise NotImplementedError


def remove_duplicates_sorted(x: List[int]) -> List[int]:
    """Remove duplicates from a sorted list, return new list."""
    raise NotImplementedError


def partition_by_pivot(x: List[int], pivot: int) -> List[int]:
    """Partition list so elements < pivot come before elements >= pivot."""
    raise NotImplementedError


def sliding_window_sum(x: List[int], k: int) -> List[int]:
    """Return list of sums of each sliding window of size k."""
    raise NotImplementedError


def max_subarray_sum(x: List[int]) -> int:
    """Find the maximum sum of any contiguous subarray (Kadane's algorithm)."""
    raise NotImplementedError
