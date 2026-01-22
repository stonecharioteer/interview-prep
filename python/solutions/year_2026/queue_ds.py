"""Queue data structure and queue-based problems."""


class Queue:
    """Basic queue with enqueue, dequeue, peek, and is_empty operations."""

    def __init__(self):
        raise NotImplementedError

    def enqueue(self, value):
        """Add value to the back of the queue."""
        raise NotImplementedError

    def dequeue(self):
        """Remove and return the front value. Return None if empty."""
        raise NotImplementedError

    def peek(self):
        """Return the front value without removing it. Return None if empty."""
        raise NotImplementedError

    def is_empty(self):
        """Return True if queue has no elements."""
        raise NotImplementedError


class QueueUsingStacks:
    """Implement a queue using two stacks. Support enqueue and dequeue."""

    def __init__(self):
        raise NotImplementedError

    def enqueue(self, value):
        """Add value to the queue."""
        raise NotImplementedError

    def dequeue(self):
        """Remove and return the front value. Return None if empty."""
        raise NotImplementedError
