import pytest
import random
from copy import deepcopy

from solutions.year_2026 import arrays

pytestmark = pytest.mark.arrays


class TestGetRandomList:
    def test_returns_list_of_correct_size(self):
        for size in [1, 5, 10, 50, 100]:
            result = arrays.get_random_list(size)
            assert len(result) == size

    def test_values_are_within_expected_range(self):
        result = arrays.get_random_list(100)
        assert all(0 <= x <= 100 for x in result)


class TestGetMaxInList:
    @pytest.fixture
    def random_list(self):
        return [random.randint(-1000, 1000) for _ in range(random.randint(10, 100))]

    def test_finds_max_in_random_list(self, random_list):
        assert arrays.get_max_in_list(random_list) == max(random_list)

    def test_finds_max_with_single_element(self):
        assert arrays.get_max_in_list([42]) == 42

    def test_finds_max_with_negative_numbers(self):
        x = [-5, -10, -2, -100]
        assert arrays.get_max_in_list(x) == -2

    def test_finds_max_with_duplicates(self):
        x = [5, 10, 10, 3, 10]
        assert arrays.get_max_in_list(x) == 10

    def test_finds_max_at_different_positions(self):
        assert arrays.get_max_in_list([100, 1, 2, 3]) == 100  # max at start
        assert arrays.get_max_in_list([1, 2, 3, 100]) == 100  # max at end
        assert arrays.get_max_in_list([1, 100, 2, 3]) == 100  # max in middle


class TestGetMinInList:
    @pytest.fixture
    def random_list(self):
        return [random.randint(-1000, 1000) for _ in range(random.randint(10, 100))]

    def test_finds_min_in_random_list(self, random_list):
        assert arrays.get_min_in_list(random_list) == min(random_list)

    def test_finds_min_with_single_element(self):
        assert arrays.get_min_in_list([42]) == 42

    def test_finds_min_with_negative_numbers(self):
        x = [-5, -10, -2, -100]
        assert arrays.get_min_in_list(x) == -100

    def test_finds_min_with_duplicates(self):
        x = [5, 2, 10, 2, 10]
        assert arrays.get_min_in_list(x) == 2

    def test_finds_min_at_different_positions(self):
        assert arrays.get_min_in_list([1, 10, 20, 30]) == 1  # min at start
        assert arrays.get_min_in_list([10, 20, 30, 1]) == 1  # min at end
        assert arrays.get_min_in_list([10, 1, 20, 30]) == 1  # min in middle


class TestGetSumOfList:
    @pytest.fixture
    def random_list(self):
        return [random.randint(-1000, 1000) for _ in range(random.randint(10, 100))]

    def test_sums_random_list(self, random_list):
        assert arrays.get_sum_of_list(random_list) == sum(random_list)

    def test_sums_single_element(self):
        assert arrays.get_sum_of_list([42]) == 42

    def test_sums_with_negative_numbers(self):
        x = [-5, 10, -2, 3]
        assert arrays.get_sum_of_list(x) == 6

    def test_sums_to_zero(self):
        x = [5, -5, 10, -10]
        assert arrays.get_sum_of_list(x) == 0


class TestIsNInList:
    @pytest.fixture
    def sample_list(self):
        return [1, 5, 10, 20, 50, 100]

    def test_finds_existing_element(self, sample_list):
        for n in sample_list:
            assert arrays.is_n_in_list(sample_list, n) is True

    def test_does_not_find_missing_element(self, sample_list):
        assert arrays.is_n_in_list(sample_list, 999) is False
        assert arrays.is_n_in_list(sample_list, -1) is False

    def test_with_random_data(self):
        x = [random.randint(0, 100) for _ in range(50)]
        n = random.randint(0, 200)
        assert arrays.is_n_in_list(x, n) == (n in x)


class TestGetAverageOfList:
    def test_average_of_simple_list(self):
        x = [2, 4, 6, 8, 10]
        assert arrays.get_average_of_list(x) == 6.0

    def test_average_with_single_element(self):
        assert arrays.get_average_of_list([42]) == 42.0

    def test_average_with_floats_result(self):
        x = [1, 2, 3, 4]
        assert arrays.get_average_of_list(x) == 2.5

    def test_average_matches_builtin(self):
        x = [random.randint(-100, 100) for _ in range(50)]
        assert arrays.get_average_of_list(x) == sum(x) / len(x)


class TestCountInstances:
    def test_counts_existing_element(self):
        x = [1, 2, 3, 2, 4, 2, 5]
        assert arrays.count_instances(x, 2) == 3

    def test_counts_missing_element(self):
        x = [1, 2, 3, 4, 5]
        assert arrays.count_instances(x, 99) == 0

    def test_counts_single_occurrence(self):
        x = [1, 2, 3, 4, 5]
        assert arrays.count_instances(x, 3) == 1

    def test_counts_all_same_elements(self):
        x = [7, 7, 7, 7, 7]
        assert arrays.count_instances(x, 7) == 5

    def test_matches_builtin_count(self):
        x = [random.randint(0, 10) for _ in range(50)]
        n = random.randint(0, 10)
        assert arrays.count_instances(x, n) == x.count(n)


class TestFindIndex:
    def test_finds_first_occurrence(self):
        x = [10, 20, 30, 20, 40]
        assert arrays.find_index(x, 20) == 1

    def test_returns_none_for_missing(self):
        x = [1, 2, 3, 4, 5]
        assert arrays.find_index(x, 99) is None

    def test_finds_at_start(self):
        x = [10, 20, 30]
        assert arrays.find_index(x, 10) == 0

    def test_finds_at_end(self):
        x = [10, 20, 30]
        assert arrays.find_index(x, 30) == 2

    def test_matches_builtin_for_existing(self):
        x = [random.randint(0, 100) for _ in range(50)]
        if x:
            n = x[random.randint(0, len(x) - 1)]
            assert arrays.find_index(x, n) == x.index(n)


class TestFindAllIndicies:
    def test_finds_all_occurrences(self):
        x = [1, 2, 3, 2, 4, 2, 5]
        assert arrays.find_all_indicies(x, 2) == [1, 3, 5]

    def test_returns_empty_for_missing(self):
        x = [1, 2, 3, 4, 5]
        assert arrays.find_all_indicies(x, 99) == []

    def test_finds_single_occurrence(self):
        x = [1, 2, 3, 4, 5]
        assert arrays.find_all_indicies(x, 3) == [2]

    def test_finds_all_for_same_elements(self):
        x = [7, 7, 7]
        assert arrays.find_all_indicies(x, 7) == [0, 1, 2]


class TestArrayReversed:
    def test_reverses_simple_list(self):
        x = [1, 2, 3, 4, 5]
        assert arrays.array_reversed(x) == [5, 4, 3, 2, 1]

    def test_reverses_single_element(self):
        x = [42]
        assert arrays.array_reversed(x) == [42]

    def test_reverses_two_elements(self):
        x = [1, 2]
        assert arrays.array_reversed(x) == [2, 1]

    def test_matches_builtin_reversed(self):
        x = [random.randint(0, 100) for _ in range(50)]
        assert arrays.array_reversed(x) == list(reversed(x))

    def test_does_not_modify_original(self):
        x = [1, 2, 3, 4, 5]
        original = x.copy()
        _ = arrays.array_reversed(x)
        assert x == original


class TestArrayReversedInPlace:
    def test_reverses_simple_list(self):
        x = [1, 2, 3, 4, 5]
        arrays.array_reversed_in_place(x)
        assert x == [5, 4, 3, 2, 1]

    def test_reverses_single_element(self):
        x = [42]
        arrays.array_reversed_in_place(x)
        assert x == [42]

    def test_reverses_two_elements(self):
        x = [1, 2]
        arrays.array_reversed_in_place(x)
        assert x == [2, 1]

    def test_reverses_even_length_list(self):
        x = [1, 2, 3, 4]
        arrays.array_reversed_in_place(x)
        assert x == [4, 3, 2, 1]

    def test_reverses_odd_length_list(self):
        x = [1, 2, 3, 4, 5]
        arrays.array_reversed_in_place(x)
        assert x == [5, 4, 3, 2, 1]

    def test_modifies_original_list(self):
        x = [1, 2, 3, 4, 5]
        original_id = id(x)
        arrays.array_reversed_in_place(x)
        assert id(x) == original_id  # same object

    def test_matches_builtin_reversed(self):
        x = [random.randint(0, 100) for _ in range(50)]
        expected = list(reversed(x))
        arrays.array_reversed_in_place(x)
        assert x == expected

    def test_in_place_vs_copy_behavior(self):
        """Verify array_reversed creates a copy while array_reversed_in_place modifies in place."""
        original = [1, 2, 3, 4, 5]
        x_copy = original.copy()
        x_in_place = original.copy()

        # array_reversed should return new list, not modify original
        result = arrays.array_reversed(x_copy)
        assert x_copy == original  # original unchanged
        assert result == [5, 4, 3, 2, 1]
        assert result is not x_copy  # different object

        # array_reversed_in_place should modify the list
        arrays.array_reversed_in_place(x_in_place)
        assert x_in_place == [5, 4, 3, 2, 1]  # original changed


class TestIsSorted:
    def test_sorted_ascending(self):
        assert arrays.is_sorted([1, 2, 3, 4, 5]) is True

    def test_sorted_with_duplicates(self):
        assert arrays.is_sorted([1, 2, 2, 3, 4]) is True

    def test_unsorted(self):
        assert arrays.is_sorted([1, 3, 2, 4, 5]) is False

    def test_single_element(self):
        assert arrays.is_sorted([42]) is True

    def test_two_elements_sorted(self):
        assert arrays.is_sorted([1, 2]) is True

    def test_two_elements_unsorted(self):
        assert arrays.is_sorted([2, 1]) is False

    def test_descending_is_not_sorted(self):
        assert arrays.is_sorted([5, 4, 3, 2, 1]) is False

    def test_all_same_elements(self):
        assert arrays.is_sorted([7, 7, 7, 7]) is True


class TestBinarySearch:
    def test_finds_element_in_middle(self):
        assert arrays.binary_search([1, 2, 3, 4, 5], 3) == 2

    def test_finds_element_at_start(self):
        assert arrays.binary_search([1, 2, 3, 4, 5], 1) == 0

    def test_finds_element_at_end(self):
        assert arrays.binary_search([1, 2, 3, 4, 5], 5) == 4

    def test_returns_none_for_missing(self):
        assert arrays.binary_search([1, 2, 3, 4, 5], 99) is None

    def test_single_element_found(self):
        assert arrays.binary_search([42], 42) == 0

    def test_single_element_not_found(self):
        assert arrays.binary_search([42], 10) is None

    def test_finds_in_larger_list(self):
        x = list(range(0, 1000, 2))  # [0, 2, 4, ..., 998]
        assert arrays.binary_search(x, 500) == 250


class TestMergeSorted:
    def test_merge_two_lists(self):
        assert arrays.merge_sorted([1, 3, 5], [2, 4, 6]) == [1, 2, 3, 4, 5, 6]

    def test_merge_with_empty_first(self):
        assert arrays.merge_sorted([], [1, 2, 3]) == [1, 2, 3]

    def test_merge_with_empty_second(self):
        assert arrays.merge_sorted([1, 2, 3], []) == [1, 2, 3]

    def test_merge_both_empty(self):
        assert arrays.merge_sorted([], []) == []

    def test_merge_with_duplicates(self):
        assert arrays.merge_sorted([1, 2, 2], [2, 3, 3]) == [1, 2, 2, 2, 3, 3]

    def test_merge_first_all_smaller(self):
        assert arrays.merge_sorted([1, 2, 3], [10, 20, 30]) == [1, 2, 3, 10, 20, 30]

    def test_merge_second_all_smaller(self):
        assert arrays.merge_sorted([10, 20, 30], [1, 2, 3]) == [1, 2, 3, 10, 20, 30]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestRotateK:
    def test_rotate_by_one(self):
        assert arrays.rotate_k([1, 2, 3, 4, 5], 1) == [5, 1, 2, 3, 4]

    def test_rotate_by_two(self):
        assert arrays.rotate_k([1, 2, 3, 4, 5], 2) == [4, 5, 1, 2, 3]

    def test_rotate_by_zero(self):
        assert arrays.rotate_k([1, 2, 3, 4, 5], 0) == [1, 2, 3, 4, 5]

    def test_rotate_by_length(self):
        assert arrays.rotate_k([1, 2, 3, 4, 5], 5) == [1, 2, 3, 4, 5]

    def test_rotate_by_more_than_length(self):
        assert arrays.rotate_k([1, 2, 3, 4, 5], 7) == [4, 5, 1, 2, 3]

    def test_rotate_single_element(self):
        assert arrays.rotate_k([42], 5) == [42]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTwoSum:
    def test_finds_pair(self):
        result = arrays.two_sum([2, 7, 11, 15], 9)
        assert result in [(0, 1), (1, 0)]

    def test_finds_pair_at_end(self):
        result = arrays.two_sum([1, 2, 3, 4], 7)
        assert result in [(2, 3), (3, 2)]

    def test_returns_none_when_no_pair(self):
        assert arrays.two_sum([1, 2, 3], 100) is None

    def test_does_not_use_same_element_twice(self):
        # [3, 3] with target 6 should return (0, 1) not use index 0 twice
        result = arrays.two_sum([3, 3], 6)
        assert result in [(0, 1), (1, 0)]

    def test_single_element_returns_none(self):
        assert arrays.two_sum([5], 10) is None

    def test_with_negative_numbers(self):
        result = arrays.two_sum([-1, -2, 3, 4], 2)
        assert result in [(0, 2), (2, 0)]  # -1 + 3 = 2


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestRemoveDuplicatesSorted:
    def test_removes_duplicates(self):
        assert arrays.remove_duplicates_sorted([1, 1, 2, 2, 3]) == [1, 2, 3]

    def test_no_duplicates(self):
        assert arrays.remove_duplicates_sorted([1, 2, 3, 4, 5]) == [1, 2, 3, 4, 5]

    def test_all_duplicates(self):
        assert arrays.remove_duplicates_sorted([7, 7, 7, 7]) == [7]

    def test_single_element(self):
        assert arrays.remove_duplicates_sorted([42]) == [42]

    def test_empty_list(self):
        assert arrays.remove_duplicates_sorted([]) == []

    def test_consecutive_duplicates(self):
        assert arrays.remove_duplicates_sorted([1, 1, 1, 2, 2, 3, 3, 3, 3]) == [1, 2, 3]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestPartitionByPivot:
    def test_partition_simple(self):
        result = arrays.partition_by_pivot([3, 1, 4, 1, 5, 9, 2, 6], 5)
        # All elements < 5 should come before elements >= 5
        pivot_idx = None
        for i, val in enumerate(result):
            if val >= 5:
                pivot_idx = i
                break
        if pivot_idx is not None:
            assert all(v < 5 for v in result[:pivot_idx])
            assert all(v >= 5 for v in result[pivot_idx:])

    def test_partition_all_smaller(self):
        result = arrays.partition_by_pivot([1, 2, 3], 10)
        assert all(v < 10 for v in result)

    def test_partition_all_larger(self):
        result = arrays.partition_by_pivot([10, 20, 30], 5)
        assert all(v >= 5 for v in result)

    def test_partition_preserves_elements(self):
        original = [3, 1, 4, 1, 5, 9, 2, 6]
        result = arrays.partition_by_pivot(original.copy(), 5)
        assert sorted(result) == sorted(original)


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSlidingWindowSum:
    def test_window_size_3(self):
        assert arrays.sliding_window_sum([1, 2, 3, 4, 5], 3) == [6, 9, 12]

    def test_window_size_1(self):
        assert arrays.sliding_window_sum([1, 2, 3, 4, 5], 1) == [1, 2, 3, 4, 5]

    def test_window_size_equals_length(self):
        assert arrays.sliding_window_sum([1, 2, 3, 4, 5], 5) == [15]

    def test_window_size_2(self):
        assert arrays.sliding_window_sum([1, 2, 3, 4], 2) == [3, 5, 7]

    def test_with_negative_numbers(self):
        assert arrays.sliding_window_sum([1, -1, 2, -2, 3], 2) == [0, 1, 0, 1]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMaxSubarraySum:
    def test_simple_case(self):
        assert arrays.max_subarray_sum([1, 2, 3, 4, 5]) == 15

    def test_with_negative_prefix(self):
        assert (
            arrays.max_subarray_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
        )  # [4, -1, 2, 1]

    def test_all_negative(self):
        assert arrays.max_subarray_sum([-1, -2, -3, -4]) == -1

    def test_single_element(self):
        assert arrays.max_subarray_sum([42]) == 42

    def test_single_negative(self):
        assert arrays.max_subarray_sum([-5]) == -5

    def test_alternating(self):
        assert arrays.max_subarray_sum([2, -1, 2, -1, 2]) == 4


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestLongestConsecutiveSequence:
    def test_simple(self):
        assert arrays.longest_consecutive_sequence([100, 4, 200, 1, 3, 2]) == 4

    def test_with_duplicates(self):
        assert arrays.longest_consecutive_sequence([1, 2, 0, 1]) == 3

    def test_empty(self):
        assert arrays.longest_consecutive_sequence([]) == 0

    def test_single(self):
        assert arrays.longest_consecutive_sequence([5]) == 1
