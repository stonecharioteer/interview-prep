import pytest

from solutions.year_2026 import trees

pytestmark = pytest.mark.trees


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTreeNode:
    def test_can_create_node(self):
        node = trees.TreeNode(10)
        assert node.value == 10

    def test_node_has_left_right(self):
        node = trees.TreeNode(10)
        assert node.left is None
        assert node.right is None

    def test_can_build_tree(self):
        #       1
        #      / \
        #     2   3
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        assert root.value == 1
        assert root.left.value == 2
        assert root.right.value == 3


# Note: All tree tests below depend on TreeNode being implemented first.
# They will xfail until TreeNode is complete.


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestPreorderTraversal:
    def test_simple_tree(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        assert trees.preorder_traversal(root) == [1, 2, 3]

    def test_left_skewed(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.left.left = trees.TreeNode(3)
        assert trees.preorder_traversal(root) == [1, 2, 3]

    def test_single_node(self):
        root = trees.TreeNode(42)
        assert trees.preorder_traversal(root) == [42]

    def test_empty_tree(self):
        assert trees.preorder_traversal(None) == []


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestInorderTraversal:
    def test_simple_tree(self):
        root = trees.TreeNode(2)
        root.left = trees.TreeNode(1)
        root.right = trees.TreeNode(3)
        assert trees.inorder_traversal(root) == [1, 2, 3]

    def test_left_skewed(self):
        root = trees.TreeNode(3)
        root.left = trees.TreeNode(2)
        root.left.left = trees.TreeNode(1)
        assert trees.inorder_traversal(root) == [1, 2, 3]

    def test_single_node(self):
        root = trees.TreeNode(42)
        assert trees.inorder_traversal(root) == [42]

    def test_empty_tree(self):
        assert trees.inorder_traversal(None) == []


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestPostorderTraversal:
    def test_simple_tree(self):
        root = trees.TreeNode(3)
        root.left = trees.TreeNode(1)
        root.right = trees.TreeNode(2)
        assert trees.postorder_traversal(root) == [1, 2, 3]

    def test_left_skewed(self):
        root = trees.TreeNode(3)
        root.left = trees.TreeNode(2)
        root.left.left = trees.TreeNode(1)
        assert trees.postorder_traversal(root) == [1, 2, 3]

    def test_single_node(self):
        root = trees.TreeNode(42)
        assert trees.postorder_traversal(root) == [42]

    def test_empty_tree(self):
        assert trees.postorder_traversal(None) == []


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestLevelOrderTraversal:
    def test_simple_tree(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        root.left.left = trees.TreeNode(4)
        root.left.right = trees.TreeNode(5)
        assert trees.level_order_traversal(root) == [1, 2, 3, 4, 5]

    def test_single_node(self):
        root = trees.TreeNode(42)
        assert trees.level_order_traversal(root) == [42]

    def test_empty_tree(self):
        assert trees.level_order_traversal(None) == []


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTreeSize:
    def test_simple_tree(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        assert trees.tree_size(root) == 3

    def test_single_node(self):
        root = trees.TreeNode(42)
        assert trees.tree_size(root) == 1

    def test_empty_tree(self):
        assert trees.tree_size(None) == 0

    def test_larger_tree(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        root.left.left = trees.TreeNode(4)
        root.left.right = trees.TreeNode(5)
        assert trees.tree_size(root) == 5


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTreeHeight:
    def test_single_node(self):
        root = trees.TreeNode(42)
        assert trees.tree_height(root) == 1

    def test_empty_tree(self):
        assert trees.tree_height(None) == 0

    def test_balanced_tree(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        assert trees.tree_height(root) == 2

    def test_left_skewed(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.left.left = trees.TreeNode(3)
        assert trees.tree_height(root) == 3


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTreeContains:
    def test_contains_root(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        assert trees.tree_contains(root, 1) is True

    def test_contains_leaf(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        assert trees.tree_contains(root, 3) is True

    def test_not_contains(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        assert trees.tree_contains(root, 99) is False

    def test_empty_tree(self):
        assert trees.tree_contains(None, 1) is False


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTreeMin:
    def test_simple_tree(self):
        root = trees.TreeNode(5)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(8)
        assert trees.tree_min(root) == 2

    def test_single_node(self):
        root = trees.TreeNode(42)
        assert trees.tree_min(root) == 42

    def test_empty_tree(self):
        assert trees.tree_min(None) is None

    def test_with_negatives(self):
        root = trees.TreeNode(0)
        root.left = trees.TreeNode(-5)
        root.right = trees.TreeNode(5)
        assert trees.tree_min(root) == -5


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTreeMax:
    def test_simple_tree(self):
        root = trees.TreeNode(5)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(8)
        assert trees.tree_max(root) == 8

    def test_single_node(self):
        root = trees.TreeNode(42)
        assert trees.tree_max(root) == 42

    def test_empty_tree(self):
        assert trees.tree_max(None) is None


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTreeSum:
    def test_simple_tree(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        assert trees.tree_sum(root) == 6

    def test_single_node(self):
        root = trees.TreeNode(42)
        assert trees.tree_sum(root) == 42

    def test_empty_tree(self):
        assert trees.tree_sum(None) == 0

    def test_with_negatives(self):
        root = trees.TreeNode(10)
        root.left = trees.TreeNode(-5)
        root.right = trees.TreeNode(5)
        assert trees.tree_sum(root) == 10


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTreeAverage:
    def test_simple_tree(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        assert trees.tree_average(root) == 2.0

    def test_single_node(self):
        root = trees.TreeNode(42)
        assert trees.tree_average(root) == 42.0

    def test_empty_tree(self):
        assert trees.tree_average(None) is None


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTreeCountOf:
    def test_count_existing(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(2)
        assert trees.tree_count_of(root, 2) == 2

    def test_count_root(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        assert trees.tree_count_of(root, 1) == 1

    def test_count_nonexistent(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        assert trees.tree_count_of(root, 99) == 0

    def test_empty_tree(self):
        assert trees.tree_count_of(None, 1) == 0


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTreeIsBalanced:
    def test_balanced(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        assert trees.tree_is_balanced(root) is True

    def test_unbalanced(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.left.left = trees.TreeNode(3)
        assert trees.tree_is_balanced(root) is False

    def test_empty(self):
        assert trees.tree_is_balanced(None) is True


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTreeIsSymmetric:
    def test_symmetric(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(2)
        assert trees.tree_is_symmetric(root) is True

    def test_not_symmetric(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        assert trees.tree_is_symmetric(root) is False


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestTreeDiameter:
    def test_simple(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        root.left.left = trees.TreeNode(4)
        root.left.right = trees.TreeNode(5)
        assert trees.tree_diameter(root) == 3


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestSerializeDeserialize:
    def test_round_trip(self):
        root = trees.TreeNode(1)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(3)
        serialized = trees.serialize_tree(root)
        restored = trees.deserialize_tree(serialized)
        assert restored.value == 1
        assert restored.left.value == 2
        assert restored.right.value == 3


# === BST Tests ===


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestBstInsert:
    def test_insert_to_empty(self):
        root = trees.bst_insert(None, 5)
        assert root.value == 5

    def test_insert_smaller(self):
        root = trees.TreeNode(5)
        root = trees.bst_insert(root, 3)
        assert root.left.value == 3

    def test_insert_larger(self):
        root = trees.TreeNode(5)
        root = trees.bst_insert(root, 7)
        assert root.right.value == 7


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestBstSearch:
    def test_found(self):
        root = trees.TreeNode(5)
        root.left = trees.TreeNode(3)
        root.right = trees.TreeNode(7)
        assert trees.bst_search(root, 3).value == 3

    def test_not_found(self):
        root = trees.TreeNode(5)
        assert trees.bst_search(root, 10) is None


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestBstDelete:
    def test_delete_leaf(self):
        root = trees.TreeNode(5)
        root.left = trees.TreeNode(3)
        root = trees.bst_delete(root, 3)
        assert root.left is None

    def test_delete_root(self):
        root = trees.TreeNode(5)
        root.left = trees.TreeNode(3)
        root.right = trees.TreeNode(7)
        root = trees.bst_delete(root, 5)
        assert root.value in [3, 7]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestBstValidate:
    def test_valid_bst(self):
        root = trees.TreeNode(5)
        root.left = trees.TreeNode(3)
        root.right = trees.TreeNode(7)
        assert trees.bst_validate(root) is True

    def test_invalid_bst(self):
        root = trees.TreeNode(5)
        root.left = trees.TreeNode(10)  # violates BST
        assert trees.bst_validate(root) is False


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestBstInorderSuccessor:
    def test_has_right_child(self):
        root = trees.TreeNode(5)
        root.left = trees.TreeNode(3)
        root.right = trees.TreeNode(7)
        root.right.left = trees.TreeNode(6)
        successor = trees.bst_inorder_successor(root, root)
        assert successor.value == 6


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestBstLowestCommonAncestor:
    def test_lca(self):
        root = trees.TreeNode(6)
        root.left = trees.TreeNode(2)
        root.right = trees.TreeNode(8)
        root.left.left = trees.TreeNode(0)
        root.left.right = trees.TreeNode(4)
        lca = trees.bst_lowest_common_ancestor(root, root.left, root.right)
        assert lca.value == 6
