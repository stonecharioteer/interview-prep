"""Trie (prefix tree) data structure for efficient string operations."""


class TrieNode:
    """A node in the trie."""

    def __init__(self):
        raise NotImplementedError


class Trie:
    """Trie data structure for storing and searching strings by prefix."""

    def __init__(self):
        raise NotImplementedError

    def insert(self, word):
        """Insert a word into the trie."""
        raise NotImplementedError

    def search(self, word):
        """Return True if word is in the trie (exact match)."""
        raise NotImplementedError

    def starts_with(self, prefix):
        """Return True if any word in trie starts with the given prefix."""
        raise NotImplementedError

    def delete(self, word):
        """Remove word from trie. No-op if word doesn't exist."""
        raise NotImplementedError

    def count_words_with_prefix(self, prefix):
        """Return count of words that start with the given prefix."""
        raise NotImplementedError

    def autocomplete(self, prefix):
        """Return list of all words that start with the given prefix."""
        raise NotImplementedError

    def count_total_words(self):
        """Return total number of words stored in the trie."""
        raise NotImplementedError


def longest_common_prefix(words):
    """Return the longest common prefix of all words."""
    raise NotImplementedError
