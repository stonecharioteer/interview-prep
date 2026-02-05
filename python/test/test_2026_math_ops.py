import pytest

from src.year_2026 import math_ops

pytestmark = pytest.mark.math


class TestGcd:
    def test_simple(self):
        assert math_ops.gcd(12, 8) == 4

    def test_coprime(self):
        assert math_ops.gcd(17, 13) == 1

    def test_same(self):
        assert math_ops.gcd(5, 5) == 5

    def test_one_is_multiple(self):
        assert math_ops.gcd(10, 5) == 5


class TestLcm:
    def test_simple(self):
        assert math_ops.lcm(4, 6) == 12

    def test_coprime(self):
        assert math_ops.lcm(3, 5) == 15

    def test_same(self):
        assert math_ops.lcm(7, 7) == 7


class TestIsPrime:
    def test_primes(self):
        assert math_ops.is_prime(2) is True
        assert math_ops.is_prime(3) is True
        assert math_ops.is_prime(17) is True
        assert math_ops.is_prime(97) is True

    def test_not_primes(self):
        assert math_ops.is_prime(0) is False
        assert math_ops.is_prime(1) is False
        assert math_ops.is_prime(4) is False
        assert math_ops.is_prime(100) is False


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSieveOfEratosthenes:
    def test_small(self):
        assert math_ops.sieve_of_eratosthenes(10) == [2, 3, 5, 7]

    def test_prime_limit(self):
        assert math_ops.sieve_of_eratosthenes(7) == [2, 3, 5, 7]

    def test_one(self):
        assert math_ops.sieve_of_eratosthenes(1) == []


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestFastExponentiation:
    def test_simple(self):
        assert math_ops.fast_exponentiation(2, 10, 1000) == 24

    def test_large(self):
        assert math_ops.fast_exponentiation(2, 100, 1_000_000_007) == 976371285

    def test_base_case(self):
        assert math_ops.fast_exponentiation(5, 0, 100) == 1
