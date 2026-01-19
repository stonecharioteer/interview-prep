from __future__ import annotations
from dataclasses import dataclass
import random
from typing import Optional, List


@dataclass
class Node:
    value: int
    child: Optional[Node]

    def as_array(self) -> List[int]:
        current_node = self
        arr = []
        while True:
            if current_node is None:
                return arr
            arr.append(current_node.value)
            current_node = current_node.child


def get_random_linked_list(size: int = 50):
    root_node = Node(random.randint(0, 100), None)
    current_node = root_node
    for _ in range(size - 1):
        next_node = Node(random.randint(0, 100), None)
        current_node.child = next_node
        current_node = next_node
    return root_node


def print_linked_list(root_node: Node):
    current_node = root_node
    while True:
        if current_node is None:
            return
        print(current_node)
        current_node = current_node.child


def get_max_in_linked_list(root_node: Node) -> Optional[int]:
    current_node = root_node
    m = None
    while True:
        if current_node is None:
            return m
        if m is None or m < current_node.value:
            m = current_node.value
        current_node = current_node.child


def get_sum_of_linked_list(root_node: Node) -> int:
    current_node = root_node
    s = 0
    while True:
        if current_node is None:
            return s
        s += current_node.value
        current_node = current_node.child


def is_n_in_linked_list(root_node: Node, n: int) -> bool:
    current_node = root_node
    print(f"{n=}")
    while True:
        if current_node is None:
            return False
        if n == current_node.value:
            return True
        current_node = current_node.child


def get_min_in_linked_list(root_node: Node) -> Optional[int]:
    m = None
    current_node = root_node
    while True:
        if current_node is None:
            return m
        if m is None or m > current_node.value:
            m = current_node.value
        current_node = current_node.child


def get_length_of_linked_list(root_node: Node) -> int:
    length = 0
    current_node = root_node
    while True:
        if current_node is None:
            return length
        length += 1
        current_node = current_node.child


def get_average_of_linked_list(root_node: Node) -> float:
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
    count = 0
    current_node = root_node
    while True:
        if current_node is None:
            return count
        if current_node.value == n:
            count += 1
        current_node = current_node.child


def get_kth_item_in_linked_list(root_node: Node, k: int) -> Optional[int]:
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


if __name__ == "__main__":
    root_node = get_random_linked_list(10)
    array = root_node.as_array()
    print_linked_list(root_node)
    assert get_max_in_linked_list(root_node) == max(array)
    assert get_min_in_linked_list(root_node) == min(array)
    assert get_sum_of_linked_list(root_node) == sum(array)
    n = random.randint(0, 1000)
    assert is_n_in_linked_list(root_node, n) == (n in array)
    assert get_length_of_linked_list(root_node) == len(array)
    assert get_average_of_linked_list(root_node) == (sum(array) / len(array))
    assert count_instances_in_linked_list(root_node, n) == array.count(n)
    k = random.randint(0, len(array) - 1)
    assert get_kth_item_in_linked_list(root_node, k) == array[k]
