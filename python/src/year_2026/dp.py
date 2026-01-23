"""Dynamic programming problems - from basic 1D to advanced patterns."""


# === 1D DP ===


def fibonacci(n):
    """Return nth Fibonacci number."""
    raise NotImplementedError


def climbing_stairs(n):
    """Return number of ways to climb n stairs taking 1 or 2 steps at a time."""
    raise NotImplementedError


def house_robber(nums):
    """Return max money robbing non-adjacent houses. nums[i] is money in house i."""
    raise NotImplementedError


def min_cost_climbing_stairs(cost):
    """Return min cost to reach top. Can start at index 0 or 1. cost[i] is cost to step on i."""
    raise NotImplementedError


def coin_change(coins, amount):
    """Return min coins needed to make amount. -1 if impossible."""
    raise NotImplementedError


def coin_change_2(coins, amount):
    """Return number of combinations to make amount using coins."""
    raise NotImplementedError


def longest_increasing_subsequence(nums):
    """Return length of longest strictly increasing subsequence."""
    raise NotImplementedError


# === 2D Grid DP ===


def unique_paths(m, n):
    """Return number of paths from top-left to bottom-right in m x n grid. Only move right or down."""
    raise NotImplementedError


def unique_paths_with_obstacles(grid):
    """Return number of paths avoiding obstacles (1 = obstacle, 0 = free)."""
    raise NotImplementedError


def min_path_sum(grid):
    """Return min sum path from top-left to bottom-right. Only move right or down."""
    raise NotImplementedError


# === String DP ===


def longest_common_subsequence(text1, text2):
    """Return length of longest common subsequence of two strings."""
    raise NotImplementedError


def longest_palindromic_substring(s):
    """Return the longest palindromic substring in s."""
    raise NotImplementedError


def longest_palindromic_subsequence(s):
    """Return length of longest palindromic subsequence in s."""
    raise NotImplementedError


def edit_distance(word1, word2):
    """Return min operations (insert, delete, replace) to convert word1 to word2."""
    raise NotImplementedError


def word_break(s, word_dict):
    """Return True if s can be segmented into words from word_dict."""
    raise NotImplementedError


# === Tree DP ===


def house_robber_3(root):
    """Return max money robbing non-adjacent nodes in binary tree."""
    raise NotImplementedError


def max_path_sum(root):
    """Return max path sum in binary tree. Path can start and end at any node."""
    raise NotImplementedError


# === Classic Optimization DP ===


def knapsack_01(weights, values, capacity):
    """Return max value for 0/1 knapsack. Each item used at most once."""
    raise NotImplementedError


def partition_equal_subset_sum(nums):
    """Return True if nums can be partitioned into two subsets with equal sum."""
    raise NotImplementedError


# === Interval DP ===


def matrix_chain_multiplication(dims):
    """Return min scalar multiplications to multiply chain of matrices. dims[i] x dims[i+1] is matrix i."""
    raise NotImplementedError


def burst_balloons(nums):
    """Return max coins from bursting all balloons. Bursting i gives nums[i-1]*nums[i]*nums[i+1]."""
    raise NotImplementedError


# === Bitmask DP ===


def travelling_salesman(distances):
    """Return min cost to visit all cities exactly once and return. distances is n x n matrix."""
    raise NotImplementedError
