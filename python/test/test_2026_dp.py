import pytest

from solutions.year_2026 import dp

pytestmark = pytest.mark.dp


# === 1D DP Tests ===

@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestFibonacci:
    def test_base_cases(self):
        assert dp.fibonacci(0) == 0
        assert dp.fibonacci(1) == 1

    def test_simple(self):
        assert dp.fibonacci(10) == 55


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestClimbingStairs:
    def test_simple(self):
        assert dp.climbing_stairs(2) == 2
        assert dp.climbing_stairs(3) == 3

    def test_larger(self):
        assert dp.climbing_stairs(5) == 8


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestHouseRobber:
    def test_simple(self):
        assert dp.house_robber([1, 2, 3, 1]) == 4

    def test_larger(self):
        assert dp.house_robber([2, 7, 9, 3, 1]) == 12


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMinCostClimbingStairs:
    def test_simple(self):
        assert dp.min_cost_climbing_stairs([10, 15, 20]) == 15

    def test_larger(self):
        assert dp.min_cost_climbing_stairs([1, 100, 1, 1, 1, 100, 1, 1, 100, 1]) == 6


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestCoinChange:
    def test_simple(self):
        assert dp.coin_change([1, 2, 5], 11) == 3

    def test_impossible(self):
        assert dp.coin_change([2], 3) == -1


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestCoinChange2:
    def test_simple(self):
        assert dp.coin_change_2([1, 2, 5], 5) == 4


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestLongestIncreasingSubsequence:
    def test_simple(self):
        assert dp.longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]) == 4


# === 2D Grid DP Tests ===

@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestUniquePaths:
    def test_simple(self):
        assert dp.unique_paths(3, 7) == 28
        assert dp.unique_paths(3, 2) == 3


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestUniquePathsWithObstacles:
    def test_no_obstacles(self):
        assert dp.unique_paths_with_obstacles([[0, 0, 0], [0, 0, 0], [0, 0, 0]]) == 6

    def test_with_obstacle(self):
        assert dp.unique_paths_with_obstacles([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMinPathSum:
    def test_simple(self):
        assert dp.min_path_sum([[1, 3, 1], [1, 5, 1], [4, 2, 1]]) == 7


# === String DP Tests ===

@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestLongestCommonSubsequence:
    def test_simple(self):
        assert dp.longest_common_subsequence("abcde", "ace") == 3

    def test_no_common(self):
        assert dp.longest_common_subsequence("abc", "def") == 0


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestLongestPalindromicSubstring:
    def test_simple(self):
        result = dp.longest_palindromic_substring("babad")
        assert result in ["bab", "aba"]

    def test_all_same(self):
        assert dp.longest_palindromic_substring("aaaa") == "aaaa"


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestLongestPalindromicSubsequence:
    def test_simple(self):
        assert dp.longest_palindromic_subsequence("bbbab") == 4


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestEditDistance:
    def test_simple(self):
        assert dp.edit_distance("horse", "ros") == 3

    def test_same(self):
        assert dp.edit_distance("abc", "abc") == 0


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestWordBreak:
    def test_can_break(self):
        assert dp.word_break("leetcode", ["leet", "code"]) is True

    def test_cannot_break(self):
        assert dp.word_break("catsandog", ["cats", "dog", "sand", "and", "cat"]) is False


# === Classic Optimization DP Tests ===

@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestKnapsack01:
    def test_simple(self):
        assert dp.knapsack_01([1, 2, 3], [10, 15, 40], 6) == 65


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestPartitionEqualSubsetSum:
    def test_can_partition(self):
        assert dp.partition_equal_subset_sum([1, 5, 11, 5]) is True

    def test_cannot_partition(self):
        assert dp.partition_equal_subset_sum([1, 2, 3, 5]) is False


# === Interval DP Tests ===

@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMatrixChainMultiplication:
    def test_simple(self):
        assert dp.matrix_chain_multiplication([10, 20, 30, 40, 30]) == 30_000


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestBurstBalloons:
    def test_simple(self):
        assert dp.burst_balloons([3, 1, 5, 8]) == 167


# === Bitmask DP Tests ===

@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTravellingSalesman:
    def test_simple(self):
        distances = [
            [0, 10, 15, 20],
            [10, 0, 35, 25],
            [15, 35, 0, 30],
            [20, 25, 30, 0],
        ]
        assert dp.travelling_salesman(distances) == 80
