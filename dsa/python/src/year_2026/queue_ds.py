"""Queue data structure and queue-based problems."""

from typing import Generic, Optional, TypeVar


T = TypeVar("T")


class Queue(Generic[T]):
    """Basic queue with enqueue, dequeue, peek, and is_empty operations."""

    def __init__(self) -> None:
        self._queue = []

    def __repr__(self) -> str:
        return "<Queue@{} : {}>".format(id(self), (self._queue))

    def enqueue(self, value: T) -> None:
        """Add value to the back of the queue."""
        self._queue.append(value)
        print(self)

    def dequeue(self) -> Optional[T]:
        """Remove and return the front value. Return None if empty."""
        if self.is_empty():
            return None
        val = self._queue.pop(0)
        print(self)
        return val

    def peek(self) -> Optional[T]:
        """Return the front value without removing it. Return None if empty."""
        if self.is_empty():
            return None
        return self._queue[0]

    def is_empty(self) -> bool:
        """Return True if queue has no elements."""
        return len(self._queue) == 0


class QueueUsingStacks:
    """Implement a queue using two stacks. Support enqueue and dequeue."""

    def __init__(self):
        self._in_stack = []
        self._out_stack = []

    def __repr__(self):
        return "<QueueUsingStacks@{} : in:`{}` out: `{}`".format(
            id(self), self._in_stack, self._out_stack
        )

    def enqueue(self, value):
        """Add value to the queue."""
        self._in_stack.append(value)
        print(f"Enqueued {value}, Current: {self}")

    def dequeue(self):
        """Remove and return the front value. Return None if empty."""
        if len(self._out_stack) > 0:
            return self._out_stack.pop()
        elif len(self._in_stack) == 0:
            return None
        else:
            while len(self._in_stack) > 0:
                self._out_stack.append(self._in_stack.pop())
            return self.dequeue()
