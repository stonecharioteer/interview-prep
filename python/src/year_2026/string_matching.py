"""String matching algorithms."""


def naive_pattern_search(text, pattern):
    """Return list of starting indices where pattern occurs in text."""
    raise NotImplementedError


def build_kmp_failure_function(pattern):
    """Return the failure function for KMP algorithm."""
    raise NotImplementedError


def kmp_search(text, pattern):
    """Return list of starting indices where pattern occurs using KMP."""
    raise NotImplementedError


def rabin_karp_search(text, pattern):
    """Return list of starting indices where pattern occurs using Rabin-Karp."""
    raise NotImplementedError
