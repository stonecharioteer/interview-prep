import pytest
import random

from solutions.year_2026.linked_list import (
    Node,
    get_random_linked_list,
    get_max_in_linked_list,
    get_min_in_linked_list,
    get_sum_of_linked_list,
    is_n_in_linked_list,
    get_length_of_linked_list,
    get_average_of_linked_list,
    count_instances_in_linked_list,
    get_kth_item_in_linked_list,
)


@pytest.fixture
def simple_linked_list():
    """Creates a linked list: 1 -> 2 -> 3 -> 4 -> 5"""
    values = [1, 2, 3, 4, 5]
    root = Node(values[0], None)
    current = root
    for val in values[1:]:
        current.child = Node(val, None)
        current = current.child
    return root, values


@pytest.fixture
def random_linked_list():
    """Creates a random linked list and returns both the list and its array representation."""
    size = random.randint(10, 50)
    root = get_random_linked_list(size)
    return root, root.as_array()


@pytest.fixture
def single_node_list():
    """Creates a linked list with a single node."""
    return Node(42, None), [42]


@pytest.fixture
def list_with_duplicates():
    """Creates a linked list with duplicate values: 5 -> 3 -> 5 -> 7 -> 5 -> 3"""
    values = [5, 3, 5, 7, 5, 3]
    root = Node(values[0], None)
    current = root
    for val in values[1:]:
        current.child = Node(val, None)
        current = current.child
    return root, values


@pytest.fixture
def list_with_negatives():
    """Creates a linked list with negative values: -10 -> 5 -> -3 -> 0 -> -7"""
    values = [-10, 5, -3, 0, -7]
    root = Node(values[0], None)
    current = root
    for val in values[1:]:
        current.child = Node(val, None)
        current = current.child
    return root, values


def linked_list_from_values(values):
    """Helper to create a linked list from a list of values."""
    if not values:
        return None
    root = Node(values[0], None)
    current = root
    for val in values[1:]:
        current.child = Node(val, None)
        current = current.child
    return root


class TestNode:
    def test_node_creation(self):
        node = Node(10, None)
        assert node.value == 10
        assert node.child is None

    def test_node_with_child(self):
        child = Node(20, None)
        parent = Node(10, child)
        assert parent.value == 10
        assert parent.child is child
        assert parent.child.value == 20

    def test_as_array_single_node(self):
        node = Node(42, None)
        assert node.as_array() == [42]

    def test_as_array_multiple_nodes(self, simple_linked_list):
        root, values = simple_linked_list
        assert root.as_array() == values


class TestGetRandomLinkedList:
    def test_creates_list_of_correct_size(self):
        for size in [1, 5, 10, 50]:
            root = get_random_linked_list(size)
            assert get_length_of_linked_list(root) == size

    def test_values_are_within_expected_range(self):
        root = get_random_linked_list(100)
        values = root.as_array()
        assert all(0 <= v <= 100 for v in values)


class TestGetMaxInLinkedList:
    def test_finds_max_in_simple_list(self, simple_linked_list):
        root, values = simple_linked_list
        assert get_max_in_linked_list(root) == max(values)

    def test_finds_max_in_random_list(self, random_linked_list):
        root, values = random_linked_list
        assert get_max_in_linked_list(root) == max(values)

    def test_finds_max_in_single_node(self, single_node_list):
        root, values = single_node_list
        assert get_max_in_linked_list(root) == 42

    def test_finds_max_with_negatives(self, list_with_negatives):
        root, values = list_with_negatives
        assert get_max_in_linked_list(root) == max(values)

    def test_finds_max_with_duplicates(self, list_with_duplicates):
        root, values = list_with_duplicates
        assert get_max_in_linked_list(root) == max(values)

    def test_max_at_different_positions(self):
        # Max at start
        root = linked_list_from_values([100, 1, 2, 3])
        assert get_max_in_linked_list(root) == 100

        # Max at end
        root = linked_list_from_values([1, 2, 3, 100])
        assert get_max_in_linked_list(root) == 100

        # Max in middle
        root = linked_list_from_values([1, 100, 2, 3])
        assert get_max_in_linked_list(root) == 100


class TestGetMinInLinkedList:
    def test_finds_min_in_simple_list(self, simple_linked_list):
        root, values = simple_linked_list
        assert get_min_in_linked_list(root) == min(values)

    def test_finds_min_in_random_list(self, random_linked_list):
        root, values = random_linked_list
        assert get_min_in_linked_list(root) == min(values)

    def test_finds_min_in_single_node(self, single_node_list):
        root, values = single_node_list
        assert get_min_in_linked_list(root) == 42

    def test_finds_min_with_negatives(self, list_with_negatives):
        root, values = list_with_negatives
        assert get_min_in_linked_list(root) == min(values)

    def test_finds_min_with_duplicates(self, list_with_duplicates):
        root, values = list_with_duplicates
        assert get_min_in_linked_list(root) == min(values)

    def test_min_at_different_positions(self):
        # Min at start
        root = linked_list_from_values([1, 10, 20, 30])
        assert get_min_in_linked_list(root) == 1

        # Min at end
        root = linked_list_from_values([10, 20, 30, 1])
        assert get_min_in_linked_list(root) == 1

        # Min in middle
        root = linked_list_from_values([10, 1, 20, 30])
        assert get_min_in_linked_list(root) == 1


class TestGetSumOfLinkedList:
    def test_sums_simple_list(self, simple_linked_list):
        root, values = simple_linked_list
        assert get_sum_of_linked_list(root) == sum(values)

    def test_sums_random_list(self, random_linked_list):
        root, values = random_linked_list
        assert get_sum_of_linked_list(root) == sum(values)

    def test_sums_single_node(self, single_node_list):
        root, values = single_node_list
        assert get_sum_of_linked_list(root) == 42

    def test_sums_with_negatives(self, list_with_negatives):
        root, values = list_with_negatives
        assert get_sum_of_linked_list(root) == sum(values)

    def test_sum_to_zero(self):
        root = linked_list_from_values([5, -5, 10, -10])
        assert get_sum_of_linked_list(root) == 0


class TestIsNInLinkedList:
    def test_finds_existing_element(self, simple_linked_list):
        root, values = simple_linked_list
        for n in values:
            assert is_n_in_linked_list(root, n) is True

    def test_does_not_find_missing_element(self, simple_linked_list):
        root, values = simple_linked_list
        assert is_n_in_linked_list(root, 999) is False
        assert is_n_in_linked_list(root, -1) is False

    def test_with_random_data(self, random_linked_list):
        root, values = random_linked_list
        n = random.randint(0, 200)
        assert is_n_in_linked_list(root, n) == (n in values)

    def test_finds_in_single_node(self, single_node_list):
        root, values = single_node_list
        assert is_n_in_linked_list(root, 42) is True
        assert is_n_in_linked_list(root, 0) is False


class TestGetLengthOfLinkedList:
    def test_length_of_simple_list(self, simple_linked_list):
        root, values = simple_linked_list
        assert get_length_of_linked_list(root) == len(values)

    def test_length_of_random_list(self, random_linked_list):
        root, values = random_linked_list
        assert get_length_of_linked_list(root) == len(values)

    def test_length_of_single_node(self, single_node_list):
        root, values = single_node_list
        assert get_length_of_linked_list(root) == 1

    @pytest.mark.parametrize("size", [1, 5, 10, 50, 100])
    def test_length_for_various_sizes(self, size):
        root = get_random_linked_list(size)
        assert get_length_of_linked_list(root) == size


class TestGetAverageOfLinkedList:
    def test_average_of_simple_list(self, simple_linked_list):
        root, values = simple_linked_list
        assert get_average_of_linked_list(root) == sum(values) / len(values)

    def test_average_of_random_list(self, random_linked_list):
        root, values = random_linked_list
        assert get_average_of_linked_list(root) == sum(values) / len(values)

    def test_average_of_single_node(self, single_node_list):
        root, values = single_node_list
        assert get_average_of_linked_list(root) == 42.0

    def test_average_with_negatives(self, list_with_negatives):
        root, values = list_with_negatives
        assert get_average_of_linked_list(root) == sum(values) / len(values)


class TestCountInstancesInLinkedList:
    def test_counts_existing_element(self, list_with_duplicates):
        root, values = list_with_duplicates
        assert count_instances_in_linked_list(root, 5) == 3
        assert count_instances_in_linked_list(root, 3) == 2
        assert count_instances_in_linked_list(root, 7) == 1

    def test_counts_missing_element(self, simple_linked_list):
        root, values = simple_linked_list
        assert count_instances_in_linked_list(root, 99) == 0

    def test_counts_in_single_node(self, single_node_list):
        root, values = single_node_list
        assert count_instances_in_linked_list(root, 42) == 1
        assert count_instances_in_linked_list(root, 0) == 0

    def test_matches_array_count(self, random_linked_list):
        root, values = random_linked_list
        n = random.randint(0, 100)
        assert count_instances_in_linked_list(root, n) == values.count(n)


class TestGetKthItemInLinkedList:
    def test_gets_items_at_valid_indices(self, simple_linked_list):
        root, values = simple_linked_list
        for k in range(len(values)):
            assert get_kth_item_in_linked_list(root, k) == values[k]

    def test_gets_first_item(self, simple_linked_list):
        root, values = simple_linked_list
        assert get_kth_item_in_linked_list(root, 0) == values[0]

    def test_gets_last_item(self, simple_linked_list):
        root, values = simple_linked_list
        assert get_kth_item_in_linked_list(root, len(values) - 1) == values[-1]

    def test_returns_none_for_out_of_bounds(self, simple_linked_list):
        root, values = simple_linked_list
        assert get_kth_item_in_linked_list(root, 100) is None

    def test_gets_item_in_single_node(self, single_node_list):
        root, values = single_node_list
        assert get_kth_item_in_linked_list(root, 0) == 42
        assert get_kth_item_in_linked_list(root, 1) is None

    def test_matches_array_indexing(self, random_linked_list):
        root, values = random_linked_list
        k = random.randint(0, len(values) - 1)
        assert get_kth_item_in_linked_list(root, k) == values[k]
