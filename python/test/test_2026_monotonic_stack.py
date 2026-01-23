import pytest

from src.year_2026 import monotonic_stack

pytestmark = pytest.mark.monotonic_stack


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestNextGreaterElement:
    def test_simple(self):
        assert monotonic_stack.next_greater_element([2, 1, 2, 4, 3]) == [
            4,
            2,
            4,
            -1,
            -1,
        ]

    def test_descending(self):
        assert monotonic_stack.next_greater_element([5, 4, 3, 2, 1]) == [
            -1,
            -1,
            -1,
            -1,
            -1,
        ]

    def test_ascending(self):
        assert monotonic_stack.next_greater_element([1, 2, 3, 4, 5]) == [2, 3, 4, 5, -1]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestNextSmallerElement:
    def test_simple(self):
        assert monotonic_stack.next_smaller_element([4, 8, 5, 2, 25]) == [
            2,
            5,
            2,
            -1,
            -1,
        ]

    def test_ascending(self):
        assert monotonic_stack.next_smaller_element([1, 2, 3, 4, 5]) == [
            -1,
            -1,
            -1,
            -1,
            -1,
        ]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestDailyTemperatures:
    def test_simple(self):
        assert monotonic_stack.daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [
            1,
            1,
            4,
            2,
            1,
            1,
            0,
            0,
        ]

    def test_decreasing(self):
        assert monotonic_stack.daily_temperatures([5, 4, 3, 2, 1]) == [0, 0, 0, 0, 0]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestLargestRectangleHistogram:
    def test_simple(self):
        assert monotonic_stack.largest_rectangle_histogram([2, 1, 5, 6, 2, 3]) == 10

    def test_ascending(self):
        assert monotonic_stack.largest_rectangle_histogram([1, 2, 3, 4, 5]) == 9

    def test_single(self):
        assert monotonic_stack.largest_rectangle_histogram([5]) == 5


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTrappingRainWater:
    def test_simple(self):
        assert (
            monotonic_stack.trapping_rain_water([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1])
            == 6
        )

    def test_no_trap(self):
        assert monotonic_stack.trapping_rain_water([1, 2, 3, 4, 5]) == 0

    def test_v_shape(self):
        assert monotonic_stack.trapping_rain_water([3, 0, 3]) == 3
