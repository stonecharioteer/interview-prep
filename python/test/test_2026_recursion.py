import pytest

from solutions.year_2026 import recursion

pytestmark = pytest.mark.recursion


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestFactorial:
    def test_factorial_zero(self):
        assert recursion.factorial(0) == 1

    def test_factorial_one(self):
        assert recursion.factorial(1) == 1

    def test_factorial_five(self):
        assert recursion.factorial(5) == 120

    def test_factorial_ten(self):
        assert recursion.factorial(10) == 3_628_800


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestFactorialMemo:
    """Same tests as TestFactorial - memoized version should behave identically."""

    def test_factorial_zero(self):
        assert recursion.factorial_memo(0) == 1

    def test_factorial_one(self):
        assert recursion.factorial_memo(1) == 1

    def test_factorial_five(self):
        assert recursion.factorial_memo(5) == 120

    def test_factorial_ten(self):
        assert recursion.factorial_memo(10) == 3_628_800


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSumArrayRecursive:
    def test_sum_simple(self):
        assert recursion.sum_array_recursive([1, 2, 3, 4, 5]) == 15

    def test_sum_single(self):
        assert recursion.sum_array_recursive([42]) == 42

    def test_sum_empty(self):
        assert recursion.sum_array_recursive([]) == 0

    def test_sum_negative(self):
        assert recursion.sum_array_recursive([-1, -2, 3]) == 0


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestReverseStringRecursive:
    def test_reverse_simple(self):
        assert recursion.reverse_string_recursive("hello") == "olleh"

    def test_reverse_single(self):
        assert recursion.reverse_string_recursive("a") == "a"

    def test_reverse_empty(self):
        assert recursion.reverse_string_recursive("") == ""

    def test_reverse_palindrome(self):
        assert recursion.reverse_string_recursive("radar") == "radar"


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestPower:
    def test_power_base_case(self):
        assert recursion.power(2, 0) == 1

    def test_power_simple(self):
        assert recursion.power(2, 3) == 8

    def test_power_one(self):
        assert recursion.power(5, 1) == 5

    def test_power_larger(self):
        assert recursion.power(2, 10) == 1024


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestPowerMemo:
    """Same tests as TestPower - memoized version should behave identically."""

    def test_power_base_case(self):
        assert recursion.power_memo(2, 0) == 1

    def test_power_simple(self):
        assert recursion.power_memo(2, 3) == 8

    def test_power_one(self):
        assert recursion.power_memo(5, 1) == 5

    def test_power_larger(self):
        assert recursion.power_memo(2, 10) == 1024


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestFibonacciRecursive:
    def test_base_cases(self):
        assert recursion.fibonacci_recursive(0) == 0
        assert recursion.fibonacci_recursive(1) == 1

    def test_simple(self):
        assert recursion.fibonacci_recursive(10) == 55


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestFibonacciMemo:
    """Same tests as TestFibonacciRecursive - memoized version should behave identically."""

    def test_base_cases(self):
        assert recursion.fibonacci_memo(0) == 0
        assert recursion.fibonacci_memo(1) == 1

    def test_simple(self):
        assert recursion.fibonacci_memo(10) == 55

    def test_larger(self):
        # Memoized version can handle larger inputs efficiently
        assert recursion.fibonacci_memo(30) == 832_040
