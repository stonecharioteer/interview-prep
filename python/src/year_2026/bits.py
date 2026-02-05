"""Bit manipulation exercises."""


def is_power_of_two(n: int) -> bool:
    """Return True if n is a power of two, False otherwise. Handle n <= 0."""
    binary_value = f"{n:b}"
    if binary_value.startswith("1"):
        return "1" not in binary_value[1:]
    return False


def count_set_bits(n):
    """Return the number of 1 bits in the binary representation of n (Hamming weight)."""
    binary_value = f"{n:b}"
    return binary_value.count("1")


def single_number(nums):
    """Return the element that appears once when all others appear twice."""
    raise NotImplementedError


def get_bit(n, i):
    """Return the value of the i-th bit (0 or 1) in n. Rightmost bit is i=0."""
    raise NotImplementedError


def set_bit(n, i):
    """Return n with the i-th bit set to 1."""
    raise NotImplementedError


def clear_bit(n, i):
    """Return n with the i-th bit set to 0."""
    raise NotImplementedError


def subsets_bitmask(nums):
    """Generate all subsets of nums using bit manipulation."""
    raise NotImplementedError
