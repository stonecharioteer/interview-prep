from __future__ import annotations


class TreeNode:
    """Binary tree node. Implement __init__ to accept value, left, and right."""

    def __init__(self, value, left=None, right=None):
        raise NotImplementedError


def preorder_traversal(root):
    """Return list of values in preorder (root, left, right)."""
    raise NotImplementedError


def inorder_traversal(root):
    """Return list of values in inorder (left, root, right)."""
    raise NotImplementedError


def postorder_traversal(root):
    """Return list of values in postorder (left, right, root)."""
    raise NotImplementedError


def level_order_traversal(root):
    """Return list of values in level order (breadth-first)."""
    raise NotImplementedError


def tree_size(root):
    """Return the number of nodes in the tree."""
    raise NotImplementedError


def tree_height(root):
    """Return the height of the tree (empty tree has height 0, single node has height 1)."""
    raise NotImplementedError


def tree_contains(root, value):
    """Check if the tree contains the given value."""
    raise NotImplementedError


def tree_min(root):
    """Return the minimum value in the tree, None if empty."""
    raise NotImplementedError


def tree_max(root):
    """Return the maximum value in the tree, None if empty."""
    raise NotImplementedError


def tree_sum(root):
    """Return the sum of all values in the tree."""
    raise NotImplementedError


def tree_average(root):
    """Return the average of all values in the tree, None if empty."""
    raise NotImplementedError


def tree_count_of(root, value):
    """Return the count of nodes with the given value."""
    raise NotImplementedError
