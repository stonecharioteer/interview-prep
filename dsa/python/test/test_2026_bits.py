import pytest

from src.year_2026 import bits

pytestmark = pytest.mark.bits


class TestIsPowerOfTwo:
    def test_powers_of_two(self):
        assert bits.is_power_of_two(1) is True
        assert bits.is_power_of_two(2) is True
        assert bits.is_power_of_two(4) is True
        assert bits.is_power_of_two(1024) is True

    def test_not_powers_of_two(self):
        assert bits.is_power_of_two(0) is False
        assert bits.is_power_of_two(3) is False
        assert bits.is_power_of_two(6) is False
        assert bits.is_power_of_two(-4) is False


class TestCountSetBits:
    def test_simple(self):
        assert bits.count_set_bits(7) == 3  # 111
        assert bits.count_set_bits(8) == 1  # 1000
        assert bits.count_set_bits(0) == 0

    def test_larger(self):
        assert bits.count_set_bits(255) == 8  # 11111111


class TestSingleNumber:
    def test_simple(self):
        assert bits.single_number([2, 2, 1]) == 1

    def test_larger(self):
        assert bits.single_number([4, 1, 2, 1, 2]) == 4

    def test_single(self):
        assert bits.single_number([1]) == 1


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestGetBit:
    def test_get_bit(self):
        assert bits.get_bit(5, 0) == 1  # 101, rightmost
        assert bits.get_bit(5, 1) == 0  # 101, second from right
        assert bits.get_bit(5, 2) == 1  # 101, third from right


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSetBit:
    def test_set_bit(self):
        assert bits.set_bit(5, 1) == 7  # 101 -> 111


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestClearBit:
    def test_clear_bit(self):
        assert bits.clear_bit(7, 1) == 5  # 111 -> 101


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSubsetsBitmask:
    def test_simple(self):
        result = bits.subsets_bitmask([1, 2])
        assert len(result) == 4
        assert [] in result
        assert [1] in result
        assert [2] in result
        assert [1, 2] in result

    def test_empty(self):
        assert bits.subsets_bitmask([]) == [[]]
