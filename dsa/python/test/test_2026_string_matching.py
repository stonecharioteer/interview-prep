import pytest

from src.year_2026 import string_matching

pytestmark = pytest.mark.string_matching


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestNaivePatternSearch:
    def test_single_match(self):
        assert string_matching.naive_pattern_search("hello world", "world") == [6]

    def test_multiple_matches(self):
        assert string_matching.naive_pattern_search("ababab", "ab") == [0, 2, 4]

    def test_no_match(self):
        assert string_matching.naive_pattern_search("hello", "xyz") == []

    def test_overlapping(self):
        assert string_matching.naive_pattern_search("aaa", "aa") == [0, 1]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestBuildKmpFailureFunction:
    def test_simple(self):
        result = string_matching.build_kmp_failure_function("ababaca")
        assert result == [0, 0, 1, 2, 3, 0, 1]

    def test_no_prefix(self):
        result = string_matching.build_kmp_failure_function("abcd")
        assert result == [0, 0, 0, 0]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestKmpSearch:
    def test_single_match(self):
        assert string_matching.kmp_search("hello world", "world") == [6]

    def test_multiple_matches(self):
        assert string_matching.kmp_search("ababab", "ab") == [0, 2, 4]

    def test_no_match(self):
        assert string_matching.kmp_search("hello", "xyz") == []


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestRabinKarpSearch:
    def test_single_match(self):
        assert string_matching.rabin_karp_search("hello world", "world") == [6]

    def test_multiple_matches(self):
        assert string_matching.rabin_karp_search("ababab", "ab") == [0, 2, 4]

    def test_no_match(self):
        assert string_matching.rabin_karp_search("hello", "xyz") == []
