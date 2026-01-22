import pytest

from solutions.year_2026 import conversions
from solutions.year_2026.linked_list import Node

pytestmark = pytest.mark.conversions


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


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestBstToSortedArray:
    def test_simple(self):
        from solutions.year_2026.trees import TreeNode
        root = TreeNode(2)
        root.left = TreeNode(1)
        root.right = TreeNode(3)
        assert conversions.bst_to_sorted_array(root) == [1, 2, 3]

    def test_empty(self):
        assert conversions.bst_to_sorted_array(None) == []


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSortedArrayToBalancedBst:
    def test_simple(self):
        root = conversions.sorted_array_to_balanced_bst([1, 2, 3, 4, 5])
        # Root should be middle element
        assert root.value == 3
        # Should be balanced
        assert root.left is not None
        assert root.right is not None

    def test_empty(self):
        assert conversions.sorted_array_to_balanced_bst([]) is None


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestAdjacencyListToMatrix:
    def test_simple(self):
        adj_list = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
        matrix = conversions.adjacency_list_to_matrix(adj_list, 3)
        assert matrix[0][1] == 1
        assert matrix[0][2] == 1
        assert matrix[0][0] == 0


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestAdjacencyMatrixToList:
    def test_simple(self):
        matrix = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        adj_list = conversions.adjacency_matrix_to_list(matrix)
        assert sorted(adj_list[0]) == [1, 2]
        assert sorted(adj_list[1]) == [0, 2]
