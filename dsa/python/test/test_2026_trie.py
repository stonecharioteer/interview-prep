import pytest

from src.year_2026 import trie

pytestmark = pytest.mark.trie


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTrieNode:
    def test_create_node(self):
        node = trie.TrieNode()
        assert hasattr(node, "children") or hasattr(node, "chars")


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTrie:
    def test_insert_search(self):
        t = trie.Trie()
        t.insert("apple")
        assert t.search("apple") is True
        assert t.search("app") is False

    def test_starts_with(self):
        t = trie.Trie()
        t.insert("apple")
        assert t.starts_with("app") is True
        assert t.starts_with("banana") is False

    def test_delete(self):
        t = trie.Trie()
        t.insert("apple")
        t.delete("apple")
        assert t.search("apple") is False

    def test_count_words_with_prefix(self):
        t = trie.Trie()
        t.insert("apple")
        t.insert("app")
        t.insert("application")
        assert t.count_words_with_prefix("app") == 3
        assert t.count_words_with_prefix("apple") == 1

    def test_autocomplete(self):
        t = trie.Trie()
        t.insert("apple")
        t.insert("app")
        t.insert("application")
        result = t.autocomplete("app")
        assert sorted(result) == ["app", "apple", "application"]

    def test_count_total_words(self):
        t = trie.Trie()
        t.insert("a")
        t.insert("b")
        t.insert("c")
        assert t.count_total_words() == 3


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestLongestCommonPrefix:
    def test_simple(self):
        assert trie.longest_common_prefix(["flower", "flow", "flight"]) == "fl"

    def test_no_common(self):
        assert trie.longest_common_prefix(["dog", "racecar", "car"]) == ""

    def test_all_same(self):
        assert trie.longest_common_prefix(["test", "test", "test"]) == "test"
