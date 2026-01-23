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
    append_to_linked_list,
    prepend_to_linked_list,
    remove_first_in_linked_list,
    insert_at_index_in_linked_list,
    remove_at_index_in_linked_list,
    reverse_linked_list,
    get_middle_node,
    detect_cycle_in_linked_list,
    merge_sorted_linked_lists,
    get_nth_from_end,
)

pytestmark = pytest.mark.linked_list


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


class TestAppendToLinkedList:
    def test_append_to_single_node(self):
        root = Node(1, None)
        root = append_to_linked_list(root, 2)
        assert root.as_array() == [1, 2]

    def test_append_multiple(self):
        root = Node(1, None)
        root = append_to_linked_list(root, 2)
        root = append_to_linked_list(root, 3)
        assert root.as_array() == [1, 2, 3]

    def test_append_preserves_existing(self):
        root = linked_list_from_values([1, 2, 3])
        root = append_to_linked_list(root, 4)
        assert root.as_array() == [1, 2, 3, 4]


class TestPrependToLinkedList:
    def test_prepend_to_single_node(self):
        root = Node(2, None)
        root = prepend_to_linked_list(root, 1)
        assert root.as_array() == [1, 2]

    def test_prepend_to_none(self):
        root = prepend_to_linked_list(None, 1)
        assert root.as_array() == [1]

    def test_prepend_multiple(self):
        root = Node(3, None)
        root = prepend_to_linked_list(root, 2)
        root = prepend_to_linked_list(root, 1)
        assert root.as_array() == [1, 2, 3]


class TestRemoveFirstInLinkedList:
    def test_remove_from_middle(self):
        root = linked_list_from_values([1, 2, 3, 4, 5])
        root = remove_first_in_linked_list(root, 3)
        assert root.as_array() == [1, 2, 4, 5]

    def test_remove_from_head(self):
        root = linked_list_from_values([1, 2, 3])
        root = remove_first_in_linked_list(root, 1)
        assert root.as_array() == [2, 3]

    def test_remove_from_tail(self):
        root = linked_list_from_values([1, 2, 3])
        root = remove_first_in_linked_list(root, 3)
        assert root.as_array() == [1, 2]

    def test_remove_only_first_occurrence(self):
        root = linked_list_from_values([1, 2, 2, 3])
        root = remove_first_in_linked_list(root, 2)
        assert root.as_array() == [1, 2, 3]

    def test_remove_nonexistent_returns_unchanged(self):
        root = linked_list_from_values([1, 2, 3])
        root = remove_first_in_linked_list(root, 99)
        assert root.as_array() == [1, 2, 3]


class TestInsertAtIndexInLinkedList:
    def test_insert_at_start(self):
        root = linked_list_from_values([2, 3, 4])
        root = insert_at_index_in_linked_list(root, 0, 1)
        assert root.as_array() == [1, 2, 3, 4]

    def test_insert_at_middle(self):
        root = linked_list_from_values([1, 2, 4, 5])
        root = insert_at_index_in_linked_list(root, 2, 3)
        assert root.as_array() == [1, 2, 3, 4, 5]

    def test_insert_at_end(self):
        root = linked_list_from_values([1, 2, 3])
        root = insert_at_index_in_linked_list(root, 3, 4)
        assert root.as_array() == [1, 2, 3, 4]

    def test_insert_into_empty(self):
        root = insert_at_index_in_linked_list(None, 0, 1)
        assert root.as_array() == [1]


class TestRemoveAtIndexInLinkedList:
    def test_remove_at_start(self):
        root = linked_list_from_values([1, 2, 3])
        root = remove_at_index_in_linked_list(root, 0)
        assert root.as_array() == [2, 3]

    def test_remove_at_middle(self):
        root = linked_list_from_values([1, 2, 3, 4])
        root = remove_at_index_in_linked_list(root, 2)
        assert root.as_array() == [1, 2, 4]

    def test_remove_at_end(self):
        root = linked_list_from_values([1, 2, 3])
        root = remove_at_index_in_linked_list(root, 2)
        assert root.as_array() == [1, 2]

    def test_remove_single_element(self):
        root = Node(1, None)
        root = remove_at_index_in_linked_list(root, 0)
        assert root is None


class TestReverseLinkedList:
    def test_reverse_simple(self):
        root = linked_list_from_values([1, 2, 3, 4, 5])
        root = reverse_linked_list(root)
        assert root.as_array() == [5, 4, 3, 2, 1]

    def test_reverse_two_elements(self):
        root = linked_list_from_values([1, 2])
        root = reverse_linked_list(root)
        assert root.as_array() == [2, 1]

    def test_reverse_single_element(self):
        root = Node(42, None)
        root = reverse_linked_list(root)
        assert root.as_array() == [42]

    def test_reverse_empty(self):
        root = reverse_linked_list(None)
        assert root is None


class TestGetMiddleNode:
    def test_middle_odd_length(self):
        root = linked_list_from_values([1, 2, 3, 4, 5])
        middle = get_middle_node(root)
        assert middle.value == 3

    def test_middle_even_length(self):
        root = linked_list_from_values([1, 2, 3, 4])
        middle = get_middle_node(root)
        assert middle.value == 3  # second middle

    def test_middle_two_elements(self):
        root = linked_list_from_values([1, 2])
        middle = get_middle_node(root)
        assert middle.value == 2

    def test_middle_single_element(self):
        root = Node(42, None)
        middle = get_middle_node(root)
        assert middle.value == 42


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestDetectCycleInLinkedList:
    def test_no_cycle(self):
        root = linked_list_from_values([1, 2, 3, 4, 5])
        assert detect_cycle_in_linked_list(root) is False

    def test_cycle_to_head(self):
        root = linked_list_from_values([1, 2, 3])
        # Create cycle: 3 -> 1
        current = root
        while current.child:
            current = current.child
        current.child = root
        assert detect_cycle_in_linked_list(root) is True

    def test_cycle_to_middle(self):
        root = linked_list_from_values([1, 2, 3, 4])
        # Create cycle: 4 -> 2
        second = root.child
        current = root
        while current.child:
            current = current.child
        current.child = second
        assert detect_cycle_in_linked_list(root) is True

    def test_single_node_no_cycle(self):
        root = Node(1, None)
        assert detect_cycle_in_linked_list(root) is False

    def test_single_node_self_cycle(self):
        root = Node(1, None)
        root.child = root
        assert detect_cycle_in_linked_list(root) is True

    def test_empty_list(self):
        assert detect_cycle_in_linked_list(None) is False


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestMergeSortedLinkedLists:
    def test_merge_two_lists(self):
        a = linked_list_from_values([1, 3, 5])
        b = linked_list_from_values([2, 4, 6])
        merged = merge_sorted_linked_lists(a, b)
        assert merged.as_array() == [1, 2, 3, 4, 5, 6]

    def test_merge_with_empty_first(self):
        b = linked_list_from_values([1, 2, 3])
        merged = merge_sorted_linked_lists(None, b)
        assert merged.as_array() == [1, 2, 3]

    def test_merge_with_empty_second(self):
        a = linked_list_from_values([1, 2, 3])
        merged = merge_sorted_linked_lists(a, None)
        assert merged.as_array() == [1, 2, 3]

    def test_merge_both_empty(self):
        merged = merge_sorted_linked_lists(None, None)
        assert merged is None

    def test_merge_with_duplicates(self):
        a = linked_list_from_values([1, 2, 2])
        b = linked_list_from_values([2, 3, 3])
        merged = merge_sorted_linked_lists(a, b)
        assert merged.as_array() == [1, 2, 2, 2, 3, 3]


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestGetNthFromEnd:
    def test_first_from_end(self):
        root = linked_list_from_values([1, 2, 3, 4, 5])
        assert get_nth_from_end(root, 1) == 5

    def test_second_from_end(self):
        root = linked_list_from_values([1, 2, 3, 4, 5])
        assert get_nth_from_end(root, 2) == 4

    def test_last_from_end(self):
        root = linked_list_from_values([1, 2, 3, 4, 5])
        assert get_nth_from_end(root, 5) == 1

    def test_out_of_bounds(self):
        root = linked_list_from_values([1, 2, 3])
        assert get_nth_from_end(root, 10) is None

    def test_single_element(self):
        root = Node(42, None)
        assert get_nth_from_end(root, 1) == 42
