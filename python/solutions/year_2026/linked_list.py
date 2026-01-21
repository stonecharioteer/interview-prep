from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Optional, List


@dataclass
class Node:
    """A node in a singly linked list with a value and reference to next node."""

    value: int
    child: Optional[Node]

    def as_array(self) -> List[int]:
        """Convert the linked list to a Python list."""
        current_node = self
        arr = []
        while True:
            if current_node is None:
                return arr
            arr.append(current_node.value)
            current_node = current_node.child


def get_random_linked_list(size: int = 50):
    """Generate a linked list with random integer values between 0 and 100."""
    root_node = Node(random.randint(0, 100), None)
    current_node = root_node
    for _ in range(size - 1):
        next_node = Node(random.randint(0, 100), None)
        current_node.child = next_node
        current_node = next_node
    return root_node


def print_linked_list(root_node: Node):
    """Print each node in the linked list."""
    current_node = root_node
    while True:
        if current_node is None:
            return
        print(current_node)
        current_node = current_node.child


def get_max_in_linked_list(root_node: Node) -> Optional[int]:
    """Return the maximum value in the linked list."""
    current_node = root_node
    m = None
    while True:
        if current_node is None:
            return m
        if m is None or m < current_node.value:
            m = current_node.value
        current_node = current_node.child


def get_sum_of_linked_list(root_node: Node) -> int:
    """Return the sum of all values in the linked list."""
    current_node = root_node
    s = 0
    while True:
        if current_node is None:
            return s
        s += current_node.value
        current_node = current_node.child


def is_n_in_linked_list(root_node: Node, n: int) -> bool:
    """Check if n exists in the linked list."""
    current_node = root_node
    print(f"{n=}")
    while True:
        if current_node is None:
            return False
        if n == current_node.value:
            return True
        current_node = current_node.child


def get_min_in_linked_list(root_node: Node) -> Optional[int]:
    """Return the minimum value in the linked list."""
    m = None
    current_node = root_node
    while True:
        if current_node is None:
            return m
        if m is None or m > current_node.value:
            m = current_node.value
        current_node = current_node.child


def get_length_of_linked_list(root_node: Node) -> int:
    """Return the number of nodes in the linked list."""
    length = 0
    current_node = root_node
    while True:
        if current_node is None:
            return length
        length += 1
        current_node = current_node.child


def get_average_of_linked_list(root_node: Node) -> float:
    """Return the average of all values in the linked list."""
    sum = 0
    length = 0
    current_node = root_node
    while True:
        if current_node is None:
            return sum / length
        length += 1
        sum += current_node.value
        current_node = current_node.child


def count_instances_in_linked_list(root_node: Node, n: int) -> float:
    """Count how many times n appears in the linked list."""
    count = 0
    current_node = root_node
    while True:
        if current_node is None:
            return count
        if current_node.value == n:
            count += 1
        current_node = current_node.child


def get_kth_item_in_linked_list(root_node: Node, k: int) -> Optional[int]:
    """Return the value at index k (0-based), or None if out of bounds."""
    counter = 0
    item = None
    current_node = root_node
    while True:
        if current_node is None:
            return item
        if counter == k:
            return current_node.value
        counter += 1
        current_node = current_node.child


def append_to_linked_list(root_node: Node, value: int) -> Node:
    """Append a value to the end of the linked list, return root."""
    current_node = root_node
    while True:
        if current_node.child is None:
            current_node.child = Node(value=value, child=None)
            return root_node
        current_node = current_node.child


def prepend_to_linked_list(root_node: Optional[Node], value: int) -> Node:
    """Prepend a value to the start of the linked list, return new root."""
    if root_node is None:
        return Node(value=value, child=None)
    else:
        return Node(value=value, child=root_node)


def remove_first_in_linked_list(root_node: Node, value: int) -> Optional[Node]:
    """Remove first occurrence of value, return root (may be different if head removed)."""
    if root_node.value == value:
        return root_node.child
    else:
        parent_node = root_node
        current_node = root_node.child
        while True:
            if current_node is None:
                return root_node
            if current_node.value == value:
                parent_node.child = current_node.child
                return root_node
            parent_node = current_node
            current_node = current_node.child


def insert_at_index_in_linked_list(
    root_node: Optional[Node], index: int, value: int
) -> Node:
    """Insert value at given index, return root. Appends to end if index exceeds list length."""
    if root_node is None or index == 0:
        return Node(value=value, child=root_node)
    current_node = root_node
    for _ in range(index - 1):
        if current_node.child is None:
            break
        current_node = current_node.child
    current_node.child = Node(value=value, child=current_node.child)
    return root_node


def remove_at_index_in_linked_list(root_node: Node, index: int) -> Optional[Node]:
    """Remove node at given index, return root (may be different if head removed)."""
    raise NotImplementedError


def reverse_linked_list(root_node: Optional[Node]) -> Optional[Node]:
    """Reverse the linked list iteratively, return new root."""
    raise NotImplementedError


def get_middle_node(root_node: Node) -> Node:
    """Return the middle node (for even length, return the second middle)."""
    raise NotImplementedError


def detect_cycle_in_linked_list(root_node: Optional[Node]) -> bool:
    """Detect if the linked list has a cycle using Floyd's algorithm."""
    raise NotImplementedError


def merge_sorted_linked_lists(a: Optional[Node], b: Optional[Node]) -> Optional[Node]:
    """Merge two sorted linked lists into one sorted linked list."""
    raise NotImplementedError


def get_nth_from_end(root_node: Node, n: int) -> Optional[int]:
    """Get the nth node value from the end (1-indexed: n=1 is last node)."""
    raise NotImplementedError
