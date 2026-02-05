"""Mathematical operations and number theory basics."""


def gcd(a, b):
    """Return the greatest common divisor of a and b."""
    gcd = 1
    possible_range = range(2, b + 1) if a > b else range(1, a + 1)
    for i in possible_range:
        if b % i == 0 and a % i == 0:
            gcd = i
    return gcd


def lcm(a, b):
    """Return the least common multiple of a and b."""
    return a * b / gcd(a, b)


def is_prime(n):
    """Return True if n is prime, False otherwise. Handle n < 2."""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def sieve_of_eratosthenes(n):
    """Return list of all primes up to n (inclusive)."""
    raise NotImplementedError


def fast_exponentiation(base, exp, mod):
    """Return (base^exp) % mod efficiently."""
    raise NotImplementedError
