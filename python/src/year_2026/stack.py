"""Stack data structure and stack-based problems."""

from __future__ import annotations
from typing import Generic, Iterable, List, Optional, TypeVar

T = TypeVar("T")


class Stack(Generic[T]):
    """Basic stack with push, pop, peek, and is_empty operations."""

    def __init__(self) -> None:
        self._stack = []

    def push(self, value: T) -> None:
        """Add value to the top of the stack."""
        self._stack.append(value)

    def pop(self) -> Optional[T]:
        """Remove and return the top value. Return None if empty."""
        if self.is_empty():
            return None
        return self._stack.pop()

    def peek(self) -> Optional[T]:
        """Return the top value without removing it. Return None if empty."""
        if self.is_empty():
            return None
        return self._stack[-1]

    def is_empty(self) -> bool:
        """Return True if stack has no elements."""
        return len(self._stack) == 0

    def __repr__(self) -> str:
        return "<Stack@{} = `{}`>".format(id(self), self._stack)


def valid_parentheses(s) -> bool:
    """Return True if s has balanced brackets: (), [], {}. Handle nesting."""
    starts = "[{("
    ends = "]})"
    stack = Stack()
    for c in s:
        if c in starts:
            stack.push(c)
        elif c in ends:
            last = stack.pop()
            if last is None:
                return False
            if last in ends:
                stack.push(last)
                stack.push(c)
            elif starts.index(last) != ends.index(c):
                stack.push(last)
                stack.push(c)
    return stack.is_empty()


def evaluate_postfix(tokens: Iterable[str]) -> Optional[int | float]:
    """Evaluate a postfix (reverse Polish) expression. Tokens are numbers or operators (+, , *, /).

    Example: 3 4 + 2 * 4 /
    """
    stack = Stack()
    for token in tokens:
        if token.isnumeric():
            stack.push(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if a is None or b is None:
                raise ValueError
            if token == "+":
                stack.push(a + b)
            elif token == "-":
                stack.push(a - b)
            elif token == "/":
                stack.push(a/b)
            elif token == "*":
                stack.push(a*b)
            else:
                raise ValueError
    return stack.pop()




class MinStack:
    """Stack that supports push, pop, peek, and get_min all in O(1) time."""

    def __init__(self):
        raise NotImplementedError

    def push(self, value):
        """Add value to the stack."""
        raise NotImplementedError

    def pop(self):
        """Remove and return the top value."""
        raise NotImplementedError

    def peek(self):
        """Return the top value without removing it."""
        raise NotImplementedError

    def get_min(self):
        """Return the minimum value in the stack in O(1) time."""
        raise NotImplementedError
