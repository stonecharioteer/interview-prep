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


def tree_is_balanced(root):
    """Return True if tree is height-balanced (left and right heights differ by at most 1)."""
    raise NotImplementedError


def tree_is_symmetric(root):
    """Return True if tree is symmetric around its center."""
    raise NotImplementedError


def tree_diameter(root):
    """Return diameter of tree (longest path between any two nodes)."""
    raise NotImplementedError


def serialize_tree(root):
    """Convert tree to a string representation."""
    raise NotImplementedError


def deserialize_tree(data):
    """Reconstruct tree from string representation."""
    raise NotImplementedError


# === Binary Search Tree (BST) operations ===


def bst_insert(root, value):
    """Insert value into BST, return root. BST property: left < root < right."""
    raise NotImplementedError


def bst_search(root, value):
    """Return node with value if found, None otherwise. Use BST property."""
    raise NotImplementedError


def bst_delete(root, value):
    """Delete node with value from BST, return root."""
    raise NotImplementedError


def bst_validate(root):
    """Return True if tree satisfies BST property."""
    raise NotImplementedError


def bst_inorder_successor(root, node):
    """Return the inorder successor of node in BST, None if no successor."""
    raise NotImplementedError


def bst_lowest_common_ancestor(root, p, q):
    """Return lowest common ancestor of nodes p and q in BST."""
    raise NotImplementedError
