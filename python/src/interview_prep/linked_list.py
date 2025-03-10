from typing import List

class ListNode:
    def __init__(self, val, next_=None):
        self.val: int = val
        self.next_ = next_


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def get(self, index: int) -> int:
        current = self.head
        counter = 0
        while counter < index:
            if current is None:
                return -1
            counter += 1
            current = current.next_
        if current is None:
            return -1
        else:
            return current.val

    def insertHead(self, val: int) -> None:
        previous_head = self.head
        self.head = ListNode(val=val, next_=previous_head)
        if previous_head is None:
            self.tail = self.head

    def insertTail(self, val: int) -> None:
        if self.head is None:
            self.head = self.tail = ListNode(val=val)
        else:
            self.tail.next_ = ListNode(val=val)
            self.tail = self.tail.next_

    def remove(self, index: int) -> bool:
        current = self.head
        counter = 0
        if index == 0:
            if self.head is not None:
                self.head = self.head.next_
                return True
            else:
                return False
        while counter < (index - 1):
            if current is None:
                return False
            current = current.next_
            counter += 1
        if current is None or current.next_ is None:
            return False
        deleted_node = current.next_
        node_after_deleted_node = deleted_node.next_
        current.next_ = node_after_deleted_node
        if current.next_ is None:
            self.tail = current
        return True

    def getValues(self) -> List[int]:
        values = []
        current = self.head
        while current is not None:
            values.append(current.val)
            current = current.next_
        return values

    @classmethod
    def from_values(cls, values: List[int]):
        linked_list = cls()
        if len(values) >= 1:
            linked_list.insertHead(values[0])
        if len(values) > 1:
            for value in values[1:]:
                linked_list.insertTail(value)
        return linked_list

    def reverse(self):
        """Reverses a linked list"""
        current = self.head
        previous = None
        if current and current.next_:
            # only operate if there are more than 2 items in the linkedlist
            length = len(self.getValues())
            counter = 0
            while current is not None:
                counter += 1
                if previous is None:
                    # this is the erstwhile head node
                    previous = current
                else:
                    current.next_ = previous
                next_node = current.next_
                previous = current
                current = next_node
                if counter >= length:
                    raise Exception("Infinite loop")
