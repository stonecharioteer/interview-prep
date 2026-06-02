import pytest

from src.year_2026 import two_pointers

pytestmark = pytest.mark.two_pointers


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTwoSumSorted:
    def test_simple(self):
        result = two_pointers.two_sum_sorted([2, 7, 11, 15], 9)
        assert result == (0, 1)

    def test_not_found(self):
        assert two_pointers.two_sum_sorted([1, 2, 3], 100) is None

    def test_at_ends(self):
        result = two_pointers.two_sum_sorted([1, 2, 3, 4, 5], 6)
        assert result == (0, 4)


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestThreeSum:
    def test_simple(self):
        result = two_pointers.three_sum([-1, 0, 1, 2, -1, -4])
        assert sorted([sorted(t) for t in result]) == sorted([[-1, -1, 2], [-1, 0, 1]])

    def test_no_solution(self):
        assert two_pointers.three_sum([1, 2, 3]) == []

    def test_all_zeros(self):
        result = two_pointers.three_sum([0, 0, 0])
        assert result == [[0, 0, 0]]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestContainerWithMostWater:
    def test_simple(self):
        assert two_pointers.container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49

    def test_two_elements(self):
        assert two_pointers.container_with_most_water([1, 1]) == 1

    def test_ascending(self):
        assert two_pointers.container_with_most_water([1, 2, 3, 4, 5]) == 6
