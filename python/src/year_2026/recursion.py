"""Basic recursion exercises to build comfort with recursive thinking."""

from typing import Dict, List, Optional


def factorial(n: int) -> int:
    """Return n! (n factorial). Base case: 0! = 1."""
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def factorial_memo(n: int, memo: Optional[Dict[int, int]] = None) -> int:
    """Return n! using memoization. Same behavior as factorial, different implementation."""
    if memo is None:
        memo = {0: 1}
    if n in memo.keys():
        return memo[n]
    else:
        fact = n * factorial_memo(n - 1, memo)
        memo[n] = fact
        return fact


def sum_array_recursive(arr: List[int]) -> int:
    """Return the sum of all elements in arr using recursion, no loops."""
    if len(arr) == 0:
        return 0
    elif len(arr) == 1:
        return arr[0]
    else:
        return arr[0] + sum_array_recursive(arr[1:])


def reverse_string_recursive(s: str) -> str:
    """Return the reversed string using recursion, no loops or slicing tricks."""
    if len(s) == 0:
        return s
    elif len(s) == 1:
        return s
    else:
        return reverse_string_recursive(s[1:]) + s[0]


def power(base: int, exp: int) -> int:
    """Return base raised to exp using recursion. Assume exp >= 0."""
    if exp == 0:
        return 1
    elif exp == 1:
        return base
    else:
        return base * power(base, exp - 1)


def power_memo(base: int, exp: int, memo: Optional[Dict[int, int]] = None):
    """Return base raised to exp using memoization. Same behavior as power, different implementation."""
    if memo is None:
        memo = {0: 1, 1: base}
    if exp in memo.keys():
        return memo[exp]
    else:
        memo[exp] = base * power_memo(base, exp - 1, memo)
        return memo[exp]


def fibonacci_recursive(n: int) -> int:
    """Return nth Fibonacci number using naive recursion."""
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n >= 2:
        return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)


def fibonacci_memo(n: int, memo: Optional[Dict[int, int]] = None) -> int:
    """Return nth Fibonacci number using memoization. Same behavior, different implementation."""
    if memo is None:
        memo = {0: 0, 1: 1}
    if n in memo.keys():
        return memo[n]
    else:
        n_1 = fibonacci_memo(n - 1, memo)
        n_2 = fibonacci_memo(n - 2, memo)
        memo[n] = n_1 + n_2
        return memo[n]
