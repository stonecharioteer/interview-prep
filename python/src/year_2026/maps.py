from typing import Any, Dict, List, TypeVar


T = TypeVar("T")
V = TypeVar("V")


def get_or_default(d: Dict[T, V], key: T, default: V) -> V:
    """Get value for key, return default if key not found."""
    return d.get(key, default)


def increment_count(d, key):
    """Increment count for key (initialize to 1 if not present), return dict."""
    d[key] = d.get(key, 0) + 1
    return d


def merge_counts(a, b):
    """Merge two count dicts, summing values for common keys."""
    c = {}
    all_keys = set(a.keys()).union(b.keys())
    for key in all_keys:
        c[key] = a.get(key, 0) + b.get(key, 0)
    return c


def most_common(d):
    """Return the key with the highest count, None if dict is empty."""
    most_common_key = None
    for key in d:
        value = d[key]
        if most_common_key is None or value > d[most_common_key]:
            most_common_key = key
    return most_common_key


def invert_mapping(d: Dict[Any, Any]) -> Dict[Any, List[Any]]:
    """Invert mapping: values become keys, keys become lists of original keys."""
    d1 = {}
    for key, value in d.items():
        d1[value] = d1.get(value, []) + [key]

    return d1


def first_non_repeating(d):
    """Return the first key with count of 1, None if all repeat or dict is empty."""
    for key, value in d.items():
        if value == 1:
            return key
    return None
