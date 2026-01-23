from typing import Dict, TypeVar


T = TypeVar("T")
V = TypeVar("V")


def get_or_default(d: Dict[T, V], key: T, default: V) -> V:
    """Get value for key, return default if key not found."""
    return d.get(key, default)


def increment_count(d, key):
    """Increment count for key (initialize to 1 if not present), return dict."""
    raise NotImplementedError


def merge_counts(a, b):
    """Merge two count dicts, summing values for common keys."""
    raise NotImplementedError


def most_common(d):
    """Return the key with the highest count, None if dict is empty."""
    raise NotImplementedError


def invert_mapping(d):
    """Invert mapping: values become keys, keys become lists of original keys."""
    raise NotImplementedError


def first_non_repeating(d):
    """Return the first key with count of 1, None if all repeat or dict is empty."""
    raise NotImplementedError
