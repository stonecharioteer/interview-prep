import pytest
from interview_prep.linked_list import LinkedList
import random


def test_can_create_linked_list():
    """Tests that we can create a linked list."""
    linked_list = LinkedList()
    linked_list.insertHead(1)
    assert linked_list.head.val == 1
    assert linked_list.tail is linked_list.head
    assert linked_list.head.next_ is None


def test_can_insert_head_to_linked_list():
    linked_list = LinkedList()
    linked_list.insertHead(1)
    linked_list.insertHead(2)
    linked_list.insertHead(3)
    assert linked_list.head.val == 3
    assert linked_list.head.next_.val == 2
    assert linked_list.head.next_.next_.val == 1
    assert linked_list.tail is linked_list.head.next_.next_
    assert linked_list.head.next_.next_.next_ is None


def test_can_get_values_of_linked_list():
    linked_list = LinkedList()
    sample_data = [12, 2456, 345, 8996723, 453, 90, 467, 84, 42]
    for value in reversed(sample_data):
        linked_list.insertHead(value)
    values_data = linked_list.getValues()
    assert sample_data == values_data


def test_can_insert_tail_to_linked_list():
    linked_list = LinkedList()
    sample_data = [12, 2456, 345, 8996723, 453, 90, 467, 84, 42]
    linked_list.insertHead(sample_data[0])
    for value in sample_data[1:]:
        linked_list.insertTail(value)
    values_data = linked_list.getValues()
    assert sample_data == values_data


def test_can_get_value_at_index_of_linked_list():
    linked_list = LinkedList()
    sample_data = [12, 2456, 345, 8996723, 453, 90, 467, 84, 42]
    linked_list.insertHead(sample_data[0])
    for value in sample_data[1:]:
        linked_list.insertTail(value)
    for ix, value in enumerate(sample_data):
        assert linked_list.get(ix) == value


def test_can_return_when_getting_impossible_index_from_linked_list():
    linked_list = LinkedList()
    linked_list.insertHead(10)
    assert linked_list.get(1000) == -1

def test_can_return_from_getting_item_in_empty_linked_list():
    linked_list = LinkedList()
    assert linked_list.get(0) == -1


def test_can_remove_value_in_linked_list():
    linked_list = LinkedList()
    sample_data = [12, 2456, 345, 8996723, 453, 90, 467, 84, 42]
    linked_list.insertHead(sample_data[0])
    for value in sample_data[1:]:
        linked_list.insertTail(value)
    del sample_data[1]
    assert linked_list.remove(1) is True
    assert sample_data == [12, 345, 8996723, 453, 90, 467, 84, 42]
    assert linked_list.getValues() == sample_data
    del sample_data[4]
    assert linked_list.remove(4) is True
    assert sample_data == [12, 345, 8996723, 453, 467, 84, 42]
    assert linked_list.getValues() == sample_data
    del sample_data[2]
    assert linked_list.remove(2) is True
    assert sample_data == [12, 345, 453, 467, 84, 42]
    assert linked_list.getValues() == sample_data
    assert linked_list.remove(100) is False


def test_linked_list_testcase_1():
    linked_list = LinkedList()
    linked_list.insertTail(1)
    linked_list.insertTail(2)
    assert linked_list.get(1) == 2
    assert linked_list.remove(1) is True
    assert linked_list.getValues() == [1]
    linked_list.insertTail(2)
    assert linked_list.getValues() == [1, 2]
    assert linked_list.get(1) == 2
    assert linked_list.get(0) == 1
    _ = [
        "insertTail",
        1,
        "insertTail",
        2,
        "get",
        1,
        "remove",
        1,
        "insertTail",
        2,
        "get",
        1,
        "get",
        0,
    ]


def test_linked_list_testcase_2():
    _ = ["insertHead", 1, "remove", 2, "remove", 1]
    linked_list = LinkedList()
    linked_list.insertHead(1)
    assert linked_list.remove(2) is False
    assert linked_list.remove(1) is False

def test_can_reverse_linked_list():
    sample_data = [12, 2456, 345, 8996723, 453, 90, 467, 84, 42]
    linked_list = LinkedList.from_values(sample_data)
    linked_list.reverse()
    assert linked_list.get_values() == reversed(sample_data)

