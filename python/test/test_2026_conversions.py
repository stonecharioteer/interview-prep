import pytest

from solutions.year_2026 import conversions
from solutions.year_2026.linked_list import Node


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestListToLinkedList:
    def test_simple_list(self):
        values = [1, 2, 3, 4, 5]
        root = conversions.list_to_linked_list(values)
        assert root.as_array() == values

    def test_single_element(self):
        root = conversions.list_to_linked_list([42])
        assert root.as_array() == [42]

    def test_empty_list(self):
        root = conversions.list_to_linked_list([])
        assert root is None

    def test_preserves_order(self):
        values = [5, 3, 8, 1, 9, 2]
        root = conversions.list_to_linked_list(values)
        assert root.as_array() == values

    def test_with_duplicates(self):
        values = [1, 2, 2, 3, 3, 3]
        root = conversions.list_to_linked_list(values)
        assert root.as_array() == values

    def test_with_negatives(self):
        values = [-1, 0, 1, -2, 2]
        root = conversions.list_to_linked_list(values)
        assert root.as_array() == values
