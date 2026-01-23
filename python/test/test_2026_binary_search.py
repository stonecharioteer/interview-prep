import pytest

from src.year_2026 import binary_search

pytestmark = pytest.mark.binary_search


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestFindFirstOccurrence:
    def test_multiple_occurrences(self):
        assert binary_search.find_first_occurrence([1, 2, 2, 2, 3], 2) == 1

    def test_single_occurrence(self):
        assert binary_search.find_first_occurrence([1, 2, 3, 4, 5], 3) == 2

    def test_not_found(self):
        assert binary_search.find_first_occurrence([1, 2, 3], 5) == -1

    def test_at_start(self):
        assert binary_search.find_first_occurrence([2, 2, 2, 3], 2) == 0


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestFindLastOccurrence:
    def test_multiple_occurrences(self):
        assert binary_search.find_last_occurrence([1, 2, 2, 2, 3], 2) == 3

    def test_at_end(self):
        assert binary_search.find_last_occurrence([1, 2, 3, 3, 3], 3) == 4


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSearchInsertPosition:
    def test_found(self):
        assert binary_search.search_insert_position([1, 3, 5, 6], 5) == 2

    def test_insert_middle(self):
        assert binary_search.search_insert_position([1, 3, 5, 6], 2) == 1

    def test_insert_end(self):
        assert binary_search.search_insert_position([1, 3, 5, 6], 7) == 4

    def test_insert_start(self):
        assert binary_search.search_insert_position([1, 3, 5, 6], 0) == 0


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSearchRotatedSortedArray:
    def test_found_left(self):
        assert binary_search.search_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 0) == 4

    def test_found_right(self):
        assert binary_search.search_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 5) == 1

    def test_not_found(self):
        assert binary_search.search_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 3) == -1


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestFindMinRotatedSortedArray:
    def test_rotated(self):
        assert binary_search.find_min_rotated_sorted_array([3, 4, 5, 1, 2]) == 1

    def test_not_rotated(self):
        assert binary_search.find_min_rotated_sorted_array([1, 2, 3, 4, 5]) == 1

    def test_single(self):
        assert binary_search.find_min_rotated_sorted_array([1]) == 1


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestFindPeakElement:
    def test_single_peak(self):
        result = binary_search.find_peak_element([1, 2, 3, 1])
        assert result == 2

    def test_ascending(self):
        result = binary_search.find_peak_element([1, 2, 3, 4])
        assert result == 3  # last element is peak

    def test_descending(self):
        result = binary_search.find_peak_element([4, 3, 2, 1])
        assert result == 0  # first element is peak


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestKokoEatingBananas:
    def test_simple(self):
        assert binary_search.koko_eating_bananas([3, 6, 7, 11], 8) == 4

    def test_tight(self):
        assert binary_search.koko_eating_bananas([30, 11, 23, 4, 20], 5) == 30


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestCapacityToShipPackages:
    def test_simple(self):
        assert (
            binary_search.capacity_to_ship_packages([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5)
            == 15
        )

    def test_one_day(self):
        assert binary_search.capacity_to_ship_packages([1, 2, 3, 1, 1], 1) == 8
