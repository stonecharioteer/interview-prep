import pytest

from src.year_2026 import sliding_window

pytestmark = pytest.mark.sliding_window


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMaxSumSubarraySizeK:
    def test_simple(self):
        assert sliding_window.max_sum_subarray_size_k([2, 1, 5, 1, 3, 2], 3) == 9

    def test_all_same(self):
        assert sliding_window.max_sum_subarray_size_k([1, 1, 1, 1], 2) == 2


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestLongestSubstringKDistinct:
    def test_simple(self):
        assert sliding_window.longest_substring_k_distinct("eceba", 2) == 3  # "ece"

    def test_one_char(self):
        assert sliding_window.longest_substring_k_distinct("aa", 1) == 2


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestLongestSubstringWithoutRepeating:
    def test_simple(self):
        assert sliding_window.longest_substring_without_repeating("abcabcbb") == 3

    def test_all_same(self):
        assert sliding_window.longest_substring_without_repeating("bbbbb") == 1

    def test_all_unique(self):
        assert sliding_window.longest_substring_without_repeating("abcdef") == 6

    def test_empty(self):
        assert sliding_window.longest_substring_without_repeating("") == 0


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMinimumWindowSubstring:
    def test_simple(self):
        assert sliding_window.minimum_window_substring("ADOBECODEBANC", "ABC") == "BANC"

    def test_exact(self):
        assert sliding_window.minimum_window_substring("a", "a") == "a"

    def test_impossible(self):
        assert sliding_window.minimum_window_substring("a", "aa") == ""
