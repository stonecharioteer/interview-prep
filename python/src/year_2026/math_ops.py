"""Mathematical operations and number theory basics."""


def gcd(a, b):
    """Return the greatest common divisor of a and b."""
    raise NotImplementedError


def lcm(a, b):
    """Return the least common multiple of a and b."""
    raise NotImplementedError


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
