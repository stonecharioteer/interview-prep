"""Bit manipulation exercises."""


def is_power_of_two(n: int) -> bool:
    """Return True if n is a power of two, False otherwise. Handle n <= 0."""
    if n == 0:
        return False
    return (n & (n - 1)) == 0


def count_set_bits(n: int) -> int:
    """Return the number of 1 bits in the binary representation of n (Hamming weight)."""
    count = 0
    while n > 0:
        count += n & 1
        n = n >> 1
    return count


def single_number(nums):
    """Return the element that appears once when all others appear twice."""
    result = 0
    for i in nums:
        result ^= i
    # This works because 1 ^ 1 ^ 2 = 2 and 0 ^ 1 = 1
    return result


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
