import pytest

from src.year_2026 import greedy

pytestmark = pytest.mark.greedy


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestJumpGame:
    def test_can_reach(self):
        assert greedy.jump_game([2, 3, 1, 1, 4]) is True

    def test_cannot_reach(self):
        assert greedy.jump_game([3, 2, 1, 0, 4]) is False

    def test_single_element(self):
        assert greedy.jump_game([0]) is True


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestJumpGame2:
    def test_simple(self):
        assert greedy.jump_game_2([2, 3, 1, 1, 4]) == 2

    def test_single_jump(self):
        assert greedy.jump_game_2([2, 1]) == 1


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMergeIntervals:
    def test_overlapping(self):
        result = greedy.merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]])
        assert result == [[1, 6], [8, 10], [15, 18]]

    def test_all_overlap(self):
        result = greedy.merge_intervals([[1, 4], [2, 3]])
        assert result == [[1, 4]]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestInsertInterval:
    def test_middle(self):
        result = greedy.insert_interval([[1, 3], [6, 9]], [2, 5])
        assert result == [[1, 5], [6, 9]]

    def test_no_overlap(self):
        result = greedy.insert_interval([[1, 2], [5, 6]], [3, 4])
        assert result == [[1, 2], [3, 4], [5, 6]]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMeetingRooms:
    def test_can_attend(self):
        assert greedy.meeting_rooms([[0, 30], [35, 50]]) is True

    def test_cannot_attend(self):
        assert greedy.meeting_rooms([[0, 30], [5, 10], [15, 20]]) is False


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMeetingRooms2:
    def test_two_rooms(self):
        assert greedy.meeting_rooms_2([[0, 30], [5, 10], [15, 20]]) == 2

    def test_one_room(self):
        assert greedy.meeting_rooms_2([[7, 10], [2, 4]]) == 1


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestGasStation:
    def test_possible(self):
        assert greedy.gas_station([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3

    def test_impossible(self):
        assert greedy.gas_station([2, 3, 4], [3, 4, 3]) == -1


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestActivitySelection:
    def test_simple(self):
        activities = [
            (1, 4),
            (3, 5),
            (0, 6),
            (5, 7),
            (3, 9),
            (5, 9),
            (6, 10),
            (8, 11),
            (8, 12),
            (2, 14),
            (12, 16),
        ]
        assert greedy.activity_selection(activities) == 4


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestFractionalKnapsack:
    def test_simple(self):
        result = greedy.fractional_knapsack([10, 20, 30], [60, 100, 120], 50)
        assert abs(result - 240.0) < 0.001
