import pytest

from src.year_2026 import queue_ds

pytestmark = pytest.mark.queue


class TestQueue:
    def test_enqueue_dequeue(self):
        q = queue_ds.Queue()
        q.enqueue(1)
        q.enqueue(2)
        assert q.dequeue() == 1
        assert q.dequeue() == 2

    def test_peek(self):
        q = queue_ds.Queue()
        q.enqueue(42)
        assert q.peek() == 42
        assert q.peek() == 42  # still there

    def test_is_empty(self):
        q = queue_ds.Queue()
        assert q.is_empty() is True
        q.enqueue(1)
        assert q.is_empty() is False

    def test_dequeue_empty(self):
        q = queue_ds.Queue()
        assert q.dequeue() is None


@pytest.mark.xfail(reason="Not implemented yet", raises=NotImplementedError)
class TestQueueUsingStacks:
    def test_fifo_order(self):
        q = queue_ds.QueueUsingStacks()
        q.enqueue(1)
        q.enqueue(2)
        q.enqueue(3)
        assert q.dequeue() == 1
        assert q.dequeue() == 2
        assert q.dequeue() == 3

    def test_interleaved(self):
        q = queue_ds.QueueUsingStacks()
        q.enqueue(1)
        q.enqueue(2)
        assert q.dequeue() == 1
        q.enqueue(3)
        assert q.dequeue() == 2
        assert q.dequeue() == 3

    def test_empty(self):
        q = queue_ds.QueueUsingStacks()
        assert q.dequeue() is None
