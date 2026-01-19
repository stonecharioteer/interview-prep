import pytest

from solutions.year_2026 import maps


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestGetOrDefault:
    def test_key_exists(self):
        d = {"a": 1, "b": 2}
        assert maps.get_or_default(d, "a", 0) == 1

    def test_key_missing(self):
        d = {"a": 1, "b": 2}
        assert maps.get_or_default(d, "c", 99) == 99

    def test_empty_dict(self):
        assert maps.get_or_default({}, "a", 42) == 42

    def test_none_value(self):
        d = {"a": None}
        assert maps.get_or_default(d, "a", 99) is None

    def test_zero_value(self):
        d = {"a": 0}
        assert maps.get_or_default(d, "a", 99) == 0


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestIncrementCount:
    def test_increment_existing(self):
        d = {"a": 5}
        result = maps.increment_count(d, "a")
        assert result["a"] == 6

    def test_increment_new_key(self):
        d = {"a": 5}
        result = maps.increment_count(d, "b")
        assert result["b"] == 1

    def test_increment_empty_dict(self):
        result = maps.increment_count({}, "a")
        assert result["a"] == 1

    def test_increment_multiple_times(self):
        d = {}
        d = maps.increment_count(d, "a")
        d = maps.increment_count(d, "a")
        d = maps.increment_count(d, "a")
        assert d["a"] == 3


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMergeCounts:
    def test_merge_disjoint(self):
        a = {"x": 1, "y": 2}
        b = {"z": 3}
        result = maps.merge_counts(a, b)
        assert result == {"x": 1, "y": 2, "z": 3}

    def test_merge_overlapping(self):
        a = {"x": 1, "y": 2}
        b = {"y": 3, "z": 4}
        result = maps.merge_counts(a, b)
        assert result == {"x": 1, "y": 5, "z": 4}

    def test_merge_with_empty(self):
        a = {"x": 1}
        assert maps.merge_counts(a, {}) == {"x": 1}
        assert maps.merge_counts({}, a) == {"x": 1}

    def test_merge_both_empty(self):
        assert maps.merge_counts({}, {}) == {}


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMostCommon:
    def test_single_max(self):
        d = {"a": 1, "b": 5, "c": 3}
        assert maps.most_common(d) == "b"

    def test_empty_dict(self):
        assert maps.most_common({}) is None

    def test_single_element(self):
        assert maps.most_common({"a": 10}) == "a"

    def test_tie_returns_any(self):
        d = {"a": 5, "b": 5}
        result = maps.most_common(d)
        assert result in ["a", "b"]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestInvertMapping:
    def test_simple_invert(self):
        d = {"a": 1, "b": 2, "c": 3}
        result = maps.invert_mapping(d)
        assert result == {1: ["a"], 2: ["b"], 3: ["c"]}

    def test_invert_with_collision(self):
        d = {"a": 1, "b": 1, "c": 2}
        result = maps.invert_mapping(d)
        assert set(result[1]) == {"a", "b"}
        assert result[2] == ["c"]

    def test_invert_empty(self):
        assert maps.invert_mapping({}) == {}


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestFirstNonRepeating:
    def test_first_non_repeating(self):
        # Ordered dict behavior expected
        d = {"a": 2, "b": 1, "c": 3, "d": 1}
        result = maps.first_non_repeating(d)
        assert result in ["b", "d"]  # either is valid

    def test_all_repeating(self):
        d = {"a": 2, "b": 3, "c": 2}
        assert maps.first_non_repeating(d) is None

    def test_empty_dict(self):
        assert maps.first_non_repeating({}) is None

    def test_single_element(self):
        assert maps.first_non_repeating({"a": 1}) == "a"

    def test_single_element_repeating(self):
        assert maps.first_non_repeating({"a": 5}) is None
